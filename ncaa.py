import numpy as np
import types

# column indexes
MATCH_Season = 0
MATCH_Daynum = 1
MATCH_Wteam = 2
MATCH_Wscore = 3
MATCH_Lteam = 4
MATCH_Lscore = 5
MATCH_Wloc = 6
MATCH_Numot = 7
MATCH_Wfgm = 8
MATCH_Wfga = 9
MATCH_Wfgm3 = 10
MATCH_Wfga3 = 11
MATCH_Wftm = 12
MATCH_Wfta = 13
MATCH_Wor = 14
MATCH_Wdr = 15
MATCH_Wast = 16
MATCH_Wto = 17
MATCH_Wstl = 18
MATCH_Wblk = 19
MATCH_Wpf = 20
MATCH_Lfgm = 21
MATCH_Lfga = 22
MATCH_Lfgm3 = 23
MATCH_Lfga3 = 24
MATCH_Lftm = 25
MATCH_Lfta = 26
MATCH_Lor = 27
MATCH_Ldr = 28
MATCH_Last = 29
MATCH_Lto = 30
MATCH_Lstl = 31
MATCH_Lblk = 32
MATCH_Lpf = 33

TEAM_NR = 364

regular_all = np.genfromtxt('data/RegularSeasonDetailedResults.csv', delimiter=',',
    dtype=types.StringType, skip_header=1)

tourney_all = np.genfromtxt('data/TourneyDetailedResults.csv', delimiter=',',
    dtype=types.StringType, skip_header=1)
regular = {}
tourney = {}

for i in range(1985, 2016):
    regular[i] = np.array(filter(lambda x: x[MATCH_Season] == str(i), regular_all))
    tourney[i] = np.array(filter(lambda x: x[MATCH_Season] == str(i), tourney_all))

# TODO: generate submission file
# get_score: (team1, team2) -> probability of team1 beating team2
# def gen_submission(get_score):
    
