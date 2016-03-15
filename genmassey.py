import numpy as np
import pandas as pd
import sys

dfnum = sys.argv[1]

class FeatureAdder(object):
    def __init__(self, df):
        self.df = df

    def feature01(self, feature):
        def mod(game):
            f0 = team_features_df.loc[(team_features_df['Team_Id'] == game['team0']) & in_season[game['Season']], feature.__name__].values[0]
            f1 = team_features_df.loc[(team_features_df['Team_Id'] == game['team1']) & in_season[game['Season']], feature.__name__].values[0]
            return pd.Series({feature.__name__+'0':f0, feature.__name__+'1':f1})
        return mod

    def massey(self):
        self.massey_init()
        self.df = pd.concat([self.df, self.df.apply(self.massey_game, axis=1)], axis=1)

    def massey_init(self):
        self.massey_df = pd.read_csv('data/massey_ordinals_2003-2015.csv')

    # Create dictionaries for boolean masks

        self.massey_seasons = self.massey_df['season'].unique()
        self.in_massey_season = dict(zip(self.massey_seasons, [self.massey_df['season'] == i for i in self.massey_seasons]))

        self.massey_day_nums = self.massey_df['rating_day_num'].unique()
        self.is_massey_day_num = dict(zip(self.massey_day_nums, [self.massey_df['rating_day_num'] == i for i in self.massey_day_nums]))

        self.massey_teams = self.massey_df['team'].unique()
        self.is_massey_team = dict(zip(self.massey_teams, [self.massey_df['team'] == i for i in self.massey_teams]))

        self.massey_systems = self.massey_df['sys_name'].unique()
        self.is_massey_system = dict(zip(self.massey_systems, [self.massey_df['sys_name'] == i for i in self.massey_systems]))

    def massey_game(self, game): # add here any features specific to a game, i.e., how do teams interact       
        try:
            daynum = game['Daynum']
        except:
            daynum = 134 # submission file games don't have daynum, but are all after day 133 (last day before tourney)


        latest_day = np.max(self.massey_day_nums[self.massey_day_nums < daynum]) # only take ordinals from dates that happened before the game, and take latest one of those
        ordinals0 = [self.getOrdinal(game['Season'], self.massey_systems[i], latest_day, game['team0']) for i in range(len(self.massey_systems))]
        ordinals1 = [self.getOrdinal(game['Season'], self.massey_systems[i], latest_day, game['team1']) for i in range(len(self.massey_systems))]
        f0 = pd.Series(ordinals0, index=[self.massey_systems[i]+'0' for i in range(len(self.massey_systems))])   
        f1 = pd.Series(ordinals1, index=[self.massey_systems[i]+'1' for i in range(len(self.massey_systems))])   
        return pd.concat([f0,f1])

    def getOrdinal(self, season, system, day, team):
        try:
            ordinal = np.float64(self.massey_df.loc[self.in_massey_season[season] & self.is_massey_system[system] & self.is_massey_day_num[day] & self.is_massey_team[team], 'orank'].values[0])
        except IndexError:
            ordinal = np.nan
        return ordinal

def add_features(df):
    dfa = FeatureAdder(df)
    dfa.massey()
    return dfa.df

if __name__ == "__main__":
    df = pd.read_csv('data/fulldata'+dfnum+'.csv', index_col=0)
    from multiprocessing import Pool
    dfnew = add_features(df)
    dfnew.to_csv('data/nfulldata'+dfnum+'.csv', encoding='ascii')
