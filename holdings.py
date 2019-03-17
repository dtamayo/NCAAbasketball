import pandas as pd
import numpy as np

class Holdings():
    def __init__(self, playins, field, teams):
        self.array = np.zeros(68)
        self.playins = playins
        self.field = field
        self.teams = teams
        self.index = dict(zip(teams['TeamID'], teams.index))
        self.team = []
    def add(self, teams, weight=1):
        if isinstance(teams, str):
            teams = [teams]
        expteams = []
        if 'field' in teams or 'Field' in teams:
            expteams += list(self.field['Team'].values)
        if 'Playin2' in teams:
            expteams += list(self.playins.iloc[2:4]['Team'].values)
        if 'Playin3' in teams:
            expteams += list(self.playins.iloc[4:6]['Team'].values)
        expteams += [team for team in teams if team != 'field' and team != 'Field' and team != 'Playin2' and team != 'Playin3']  
        self.team += expteams
        expteams = pd.DataFrame(expteams, columns=['Team'])
        expteams['TeamID'] = expteams.apply(getID, axis=1)
        for ID in expteams['TeamID']:
            self.array[self.index[ID]] = weight
