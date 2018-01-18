#!/usr/bin/env python3
# swiss tournament implementation

import psycopg2
from random import shuffle


def connect():
    """Connect to the postgresql DB, returns DB and cursor for operations """
    db = psycopg2.connect("dbname=swiss")
    cur = db.cursor()
    return db, cur


def create_player(name):
    """ Register player to the tournament DB
    Args: player name
    Returns: players unique ID (int)
    """
    query = ("""INSERT INTO players (name)
			 VALUES (%s)
			 RETURNING id""")
    params = (name,)

    db, cur = connect()
    cur.execute(query, params)
    id = cur.fetchall()[0][0]
    db.commit()
    db.close()
    return id


def create_tournament(name):
    """Creation of new tournament
    Args: Tournament name
    Returns: tournament unique ID (int)
    """
    query = ("""INSERT INTO tournaments (name)
			 VALUES (%s)
			 RETURNING id""")
    params = (name,)

    db, cur = connect()
    cur.execute(query, params)
    id = cur.fetchall()[0][0]
    db.commit()
    db.close()
    return id


def register_player(tour, player):
    """Registers existing player to existing tournament
    Args: Tournament unique ID
              player unique ID
    """
    query = ("""INSERT INTO registration (player,tournament)
			 VALUES (%s, %s)"""
             )
    params = (player, tour,)

    db, cur = connect()
    cur.execute(query, params)
    db.commit()
    db.close()


def report_match(tournament, winner, loser, draw=False):
    """Report match between two players
    Args: Tournament unique ID
              Winner - Player unique ID
              Loser - Player unique ID 
              Draw - default FALSE
    """
    query = ("""INSERT INTO matches (tournament, winner, loser, draw)
			 VALUES (%s, %s, %s, %s)"""
             )
    params = (tournament, winner, loser, draw,)

    db, cur = connect()
    cur.execute(query, params)
    db.commit()
    db.close()


def already_played(tour, player1, player2):
    """Checks if two players already played in tournament
    Args: Tournament unique ID
              player1 unique ID
              player2 unique ID
    Returns: True if already played else False
    """
    query = ("""SELECT count(*)
			 FROM matches
			 WHERE tournament = %s
			 AND ((winner = %s AND loser = %s) OR (winner = %s AND loser = %s))
			 """
             )
    params = (tour, player1, player2, player2, player1)

    db, cur = connect()
    cur.execute(query, params)
    played = cur.fetchall()[0][0]
    db.close()

    return played > 0


def playerStandings(tour):
    """Returns list of players and they tournament records
    Players are sorted 1st is best player or player tied to first place
    Args: Tournament unique ID
    """
    query = ("""SELECT players.id, players.name, score, OWR, wins, losses, draws, played 
			 FROM players, standings 
			 WHERE players.id = standings.player AND standings.tournament = %s"""
             )
    params = (tour,)

    db, cur = connect()
    cur.execute(query, params)
    standings = cur.fetchall()
    db.close()

    return standings


def swissPairings(tour):
    """Returns list of tuples containing pairs of players for next round
    There must be even number of players
    Players can't play more than one time together

    Args: Tournament unique ID
    Returns: A list of tuples each containing player1.ID, player1.name, player2.ID, player2.name
    """
    standings = playerStandings(tour)
    pairings = []

    # first round, make random standings
    if standings[0][7] == 0:
        shuffle(standings)
        for i in range(0, len(standings), 2):
            pairings.append((standings[i][0], standings[i][1], standings[
                            i + 1][0], standings[i + 1][1]))
        return pairings

    # creation of pairs
    for i in range(0, len(standings), 2):
        j, k = 0, 1
        while already_played(tour, standings[j][0], standings[k][0]):
            k = k + 1
        pairings.append((standings[j][0], standings[j][
                        1], standings[k][0], standings[k][1]))
        standings.pop(k)
        standings.pop(j)

    return pairings


def delete_tour(tour):
    """Deletes tournament from db.
    deletes player registration and matches recorded for this tournament
    Args: tournament unique ID
    """
    queries = []
    queries.append(("""
					DELETE FROM matches
					WHERE tournament = %s
					"""))
    queries.append(("""
					DELETE FROM registration
					WHERE tournament = %s
					"""))
    queries.append(("""
					DELETE FROM tournaments
					WHERE tournament = %s
					"""))
    params = (tour,)
    db, cur = connect()
    for query in queries:
        cur.execute(query, params)
    db.close()
