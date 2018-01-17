-- postgresql table and views definitions for tournament project
-- Milan Prochazka project
-- \i tournament.sql for installation

--delete previous tournament DB if it exists
DROP DATABASE IF EXISTS swiss;

--create DB
CREATE DATABASE swiss;

-- Connection
\c swiss

-- tables

-- player representation
CREATE TABLE players (
	id serial PRIMARY KEY,
	name text
	);

-- torunament
CREATE TABLE tournaments (
	id serial PRIMARY KEY,
	name text
	);

-- registration
CREATE TABLE registration (
	player int REFERENCES players(id),
	tournament int REFERENCES tournaments(id),
	PRIMARY KEY (player,tournament)
	);

-- match
CREATE TABLE matches (
	id serial PRIMARY KEY,
	tournament int REFERENCES tournaments(id),
	winner int REFERENCES players(id),
	loser int REFERENCES players(id),
	draw boolean DEFAULT false
	);

-- views

CREATE VIEW enrolledPlayers AS
	SELECT tournaments.name AS tournament, count(registration.player) AS NoPlayers
	FROM tournaments, registration
	WHERE tournaments.id = registration.tournament
	GROUP BY tournaments.name;

CREATE VIEW matchesPlayed AS
	SELECT players.name, tournaments.name AS tournament, count(matches.id) AS played
	FROM tournaments, players, matches
	WHERE tournaments.id = matches.tournament
	AND ( players.id = matches.loser OR players.id = matches.winner)
	GROUP BY players.name, tournaments.name;

CREATE VIEW playerWins AS
	SELECT registration.player, registration.tournament, count(matches.winner) AS wins
	FROM registration LEFT JOIN matches
	ON registration.tournament = matches.tournament
	AND registration.player = matches.winner
	AND matches.draw = false
	GROUP BY registration.player, registration.tournament;

CREATE VIEW playerLoses AS
	SELECT registration.player, registration.tournament, count(matches.loser) AS losses
	FROM registration LEFT JOIN matches
	ON registration.tournament = matches.tournament
	AND registration.player = matches.loser
	AND matches.draw = false
	GROUP BY registration.player, registration.tournament;

CREATE VIEW playerDraws AS
	SELECT registration.player, registration.tournament, count(matches.draw) AS draws
	FROM registration LEFT JOIN matches
	ON registration.tournament = matches.tournament
	AND matches.draw = true
	AND (registration.player = matches.loser OR registration.player = matches.winner)
	GROUP BY registration.player, registration.tournament;

CREATE VIEW winRate AS
	SELECT playerWins.player, playerWins.tournament, round(((wins + draws * 0.5) / (wins+draws+losses)),3) AS winRate
	FROM playerWins JOIN playerLoses
	ON playerWins.player = playerLoses.player AND playerWins.tournament = playerLoses.tournament
	JOIN playerDraws
	ON playerWins.player = playerDraws.player AND playerWins.tournament = playerDraws.tournament;

CREATE VIEW playerOpponents AS
	SELECT * FROM
	(SELECT registration.player, registration.tournament, matches.loser AS opponent
	FROM registration LEFT JOIN matches
	ON registration.tournament = matches.tournament
	AND registration.player = matches.winner
	UNION
	SELECT registration.player, registration.tournament, matches.winner AS opponent
	FROM registration LEFT JOIN matches
	ON registration.tournament = matches.tournament
	AND registration.player = matches.loser
	) AS opponents
	ORDER BY opponents.player;

CREATE VIEW opponentsWinRate AS
	SELECT playeropponents.player, playeropponents.tournament, round(sum(winrate)/count(winrate),3) AS OWR
	FROM playeropponents LEFT JOIN winrate
	ON playeropponents.opponent = winrate.player
	GROUP BY playeropponents.player, playeropponents.tournament;

CREATE VIEW standings AS
	SELECT playerWins.tournament, playerWins.player, (wins*3 + draws) AS score,
	OWR, wins, losses, draws, wins + losses + draws AS played
	FROM playerWins JOIN playerLoses
	ON playerWins.player = playerLoses.player AND playerWins.tournament = playerLoses.tournament
		JOIN playerDraws
		ON playerWins.player = playerDraws.player AND playerWins.tournament = playerDraws.tournament
			JOIN opponentsWInRate
			ON playerWins.player = opponentsWInRate.player AND playerWins.tournament = opponentsWInRate.tournament
			ORDER BY score DESC, OWR DESC;





