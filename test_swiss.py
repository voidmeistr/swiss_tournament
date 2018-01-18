#!/usr/bin/env python3
# test cases for swiss.py
from swiss import *

players = ['player1', 'player2', 'player3', 'player4', 'player5', 'player6']
playerIDs = []

# player creation
for player in players:
    playerIDs.append(create_player(player))

# tournament creation
tournament = create_tournament("tournament")

# player registration
for player in playerIDs:
    register_player(tournament, player)


standings = playerStandings(tournament)

if len(standings) != 6:
    raise ValueError(
        "Incorrect number of players in standings after registration.")
print("1.Number of players after registration test passed.")

# match between player 1 and player 2
report_match(tournament, playerIDs[0], playerIDs[1])
# function already_played tests
if not already_played(tournament, playerIDs[0], playerIDs[1]):
    raise ValueError(
        "Function already_played returned FALSE for players who played together.")
if already_played(tournament, playerIDs[0], playerIDs[3]):
    raise ValueError(
        "Function already_played returned TRUE for players who haven't played with each other yet.")
print("2.Function already_played passed tests.")

# rest of round 1
report_match(tournament, playerIDs[2], playerIDs[3])
report_match(tournament, playerIDs[4], playerIDs[5], True)
# round 1:
# WINNER  |  LOSER
# player1 | player2
# player3 | player4
# -----------------
# player5 | player6 - DRAW

# round 2:
report_match(tournament, playerIDs[0], playerIDs[2])
report_match(tournament, playerIDs[3], playerIDs[5])
report_match(tournament, playerIDs[1], playerIDs[4], True)
# round 1:
# WINNER  |  LOSER
# player1 | player3
# player4 | player6
# -----------------
# player2 | player5 - DRAW

expected_standingIDs = [1, 3, 4, 5, 2, 6]
expected_score = [6, 3, 3, 2, 1, 1]

standings = playerStandings(tournament)
# checks for player order, player score and played matches
for i in range(len(standings)):
    if standings[i][0] != expected_standingIDs[i]:
        raise ValueError("Returned standings are incorrect.")
    if standings[i][2] != expected_score[i]:
        raise ValueError(
            "Returned standings contain incorrect score for players")
    if standings[i][7] != 2:
        raise ValueError("Played matches in standings are incorrect.")

print("3.Returned standings adter two rounds return correct player order.")
print("4.Returned standings after two rounds return correct score for each player.")

pairings = swissPairings(tournament)
if len(pairings) != len(standings) / 2:
    raise ValueError("Incorrect number of pairs for next round.")

print("5.Correct number of pairs for next round.")
# because 1 and 3 already played together
expected_pairings = [(1, 4), (3, 5), (2, 6)]
# checks pairs
for i in range(len(pairings)):
    if pairings[i][0] != expected_pairings[i][0] or pairings[i][2] != expected_pairings[i][1]:
        raise ValueError("Returned pairs are incorrect.")
print("6.Returned pairings are correct.")
print("All tests passed!")
