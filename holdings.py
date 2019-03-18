import pandas as pd
import numpy as np

class Calcutta():
    def __init__(self, playins, field, teams, entries, pool):
        self.playins = playins
        self.field = field
        self.teams = teams
        self.entries = entries
        self.pool = pool

class Entry():
    def __init__(self, bracket):
        self.array = np.zeros(68)
        self.teams = teams
        self.index = dict(zip(bracket['TeamID'], bracket.index))
        self.teams = []
    def add(self, teams, weight=1):
        if isinstance(teams, str):
            teams = [teams]
        self.teams += teams
        teams = pd.DataFrame(teams, columns=['Team'])
        teams['TeamID'] = teams.apply(getID, axis=1)
        for ID in teams['TeamID']:
            self.array[self.index[ID]] = weight
