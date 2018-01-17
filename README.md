# swiss tournament module

Python app that uses PostgreSQL for hosting swiss style tournament

Currently designed for even number of players.

Win - 3 points , draw - 1 point

Author: Milan Prochazka

Python3.4

## Getting started

###### launch psql

###### load database structures:

`\i swiss.sql `

###### quit psql interactive:

`\q`

## Use

##### 1.import module in python interpreter

`from swiss import *`

##### 2.create players

`playerID = create_player('name')`

##### 3.create tournament

`tournamentID = create_tournament('name')`

##### 4.register player for tournament

`register_player(tournamentID,playerID)`

##### 5.get pairings for next round, function return list of tuples containing (player1ID, player1Name, player2ID, player2Name)

`swissPairings(tournamentID)`
`[(player1ID, player1Name, player2ID, player2Name),.....]`

##### 6.report results, draw is defaultly false if not specified

`report_match(tournamentID, winnerID, loserID, draw = False)`

##### 7.check standings

`playerStandings(tournamentID)`

##### 8.get pairings for next round








