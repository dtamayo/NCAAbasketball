import numpy as np
from ncaa import *
import warnings

#warnings.filterwarnings('error')

class Elo:
    def __init__(self, kfactor=None, beta=None, base=None, rating_initial=None):
        if kfactor == None:
            kfactor = np.random.normal(30, 3)
        if beta == None:
            beta = np.random.normal(1.0/400.0, 1.0/3)
        if base == None:
            base = np.random.normal(10, 3)
        if rating_initial == None:
            rating_initial = np.random.normal(1400, 3)
        
        self.kfactor = kfactor
        self.beta = beta
        self.base = base
        self.ratings = np.array([rating_initial]*TEAM_NR)
        self.fitness = 0
        
    def expected_score(self, r1, r2):
        """excluding draws, the probability of player with rating r1 beating player
        with rating r2"""
        logit = (r2 - r1)*self.beta
        return 1.0/(1.0 + np.power(self.base, logit))

    def new_rating(self, r1, r2, winner):
        """winner is 1 or 2 representing player with the rating with the same
        number or 0 for draw"""
        e1 = self.expected_score(r1, r2)
        e2 = 1 - e1

        if winner == 1:
            new_r1 = r1 + self.kfactor*(1 - e1)
            new_r2 = r2 + self.kfactor*(0 - e2)
        if winner == 2:
            new_r1 = r1 + self.kfactor*(0 - e1)
            new_r2 = r2 + self.kfactor*(1 - e2)
        if winner == 0:
            new_r1 = r1 + self.kfactor*(0.5 - e1)
            new_r2 = r2 + self.kfactor*(0.5 - e2)

        return (new_r1, new_r2)
    
    def build_ratings(self, data):
        for i in range(len(data)):
            team1 = int(data[i,MATCH_Wteam]) - 1101
            team2 = int(data[i,MATCH_Lteam]) - 1101
            score1 = int(data[i,MATCH_Wscore])
            score2 = int(data[i,MATCH_Lscore])

            winner  = 1 if score1 > score2 else 2
            self.ratings[team1], self.ratings[team2] \
                = self.new_rating(self.ratings[team1], self.ratings[team2],
                             winner)

    def eval_fitness(self, data):
        goodone = 0
        logloss = 0 
        
        for i in range(len(data)):
            team1 = int(data[i,MATCH_Wteam]) - 1101
            team2 = int(data[i,MATCH_Lteam]) - 1101
            score1 = int(data[i,MATCH_Wscore])
            score2 = int(data[i,MATCH_Lscore])
            
            # for accuracy
            winner  = 1 if score1 > score2 else 2

            winner_pred = 1 if self.expected_score(self.ratings[team1], 
                                              self.ratings[team2]) \
                > 0.5 else 2
            if winner == winner_pred:
                goodone += 1
            
            # for logloss
            y = 1 if score1 > score2 else 0
            yhat = self.expected_score(self.ratings[team1], self.ratings[team2])
            logloss -= y*np.log(yhat) + (1-y)*np.log(1-yhat)
                
        self.logloss = logloss/float(len(data))
        self.accuracy = goodone/float(len(data))
        
        # print("logloss is: %f, accuracy: %f" % (logloss, accuracy))
        return self.logloss, self.accuracy


if __name__ == "__main__":
    elo = Elo(30, 1.0/400, 10, 1600)
    elo.build_ratings(tourney[2012])
    elo.eval_fitness(tourney[2012])

    print("%f, %f" % (elo.logloss, elo.accuracy))
