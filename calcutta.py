import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from numpy.polynomial.polynomial import polyfit

try:
    plt.style.use('paper')
except:
    print("plot style not found")
    
class Calcutta():
    def __init__(self, syndicatenames, poolestimate, bracketfile, simtourneysfile):
        self._bracketfile = bracketfile
        self._simtourneys = np.load(simtourneysfile)
        self.syndicates = {name:Syndicate(bracketfile) for name in syndicatenames}
        self.mysyn = self.syndicates[syndicatenames[0]]
        self.orig_pool = poolestimate
        self.poolxs = []
        self.poolys = []
        self.poolestimates = []
        self.poolestimates2 = []
        self._update_pool_estimate()
        
    def check(self, team, plot=False):
        simresults = self.mysyn.sim_results(self._simtourneys)
        meanpre = simresults.mean()
        varpre = simresults.var()
      
        single = Syndicate(self._bracketfile)
        single.add(team)
        simresults = single.sim_results(self._simtourneys)
        meansingle = simresults.mean()
        varsingle = simresults.var()
        single.plot(self._simtourneys, pool=self.poolestimates[-1])
        
        self.mysyn.to_npy('temp.npy') # make copy before hypothetical add
        self.mysyn.add(team)
        
        simresults = self.mysyn.sim_results(self._simtourneys)
        meanpost = simresults.mean()
        varpost = simresults.var()
        
        value = (meanpost-meanpre)*self.poolestimates[-1]
        cov = (varpost - varpre - varsingle)/2. # Var(X+Y) = Var(X) + Var(Y) + 2Cov(X,Y)
        corr = cov/np.sqrt(varpre*varsingle)
       
        self.mysyn.from_npy('temp.npy') # restore
        print("Team: {0} \n Value: ${1:.2f} \n Correlation: {2:.2f}".format(team, value, corr))
        return
    
    def buy(self, team, syndicate, amount, weight=1., plot=True):
        self.syndicates[syndicate].add(team=team, weight=weight, paid=amount)
        self._update_pool_estimate()
        if plot:
            self.syndicates[syndicate].plot(self._simtourneys, pool=self.poolestimates[-1])
        
    @property
    def currentpool(self):
        pool = 0.
        for syn in self.syndicates.values():
            pool += syn.totpaid
        return pool
    
    def _update_pool_estimate(self):
        single = Syndicate(self._bracketfile)
        for syn in self.syndicates.values():
            single.add(syn.teams['Team'].values)
        totteams = single.teams.shape[0]
        if totteams == 0:
            est_pool = self.orig_pool
        else:
            simresults = single.sim_results(self._simtourneys)
            self.poolxs.append(simresults.mean()) # mean share for teams held by all syndicates
            self.poolys.append(self.currentpool)
            b,m = polyfit(self.poolxs, self.poolys, 1)
            est_pool = b+m
            
        memory = 49. # Scale for # of teams to use for orig pool estimate
        frac_orig = max(1.-totteams/memory, 0.)
        self.poolestimates.append(frac_orig*self.orig_pool + (1.-frac_orig)*est_pool)
        
class Syndicate():
    def __init__(self, bracketfile):
        # make dictionary to map from numeric ID to index in holdings array
        self._teams = pd.read_pickle(bracketfile)
        self._teams = self._teams.loc[np.array(['Playin' not in name for name in self._teams['Team']])]
        self._teams = self._teams.reset_index(drop=True)
        self._teams['Fraction Owned'] = 0.
        self._teams['Amount'] = 0.
        self.totpaid=0.
        self.mean = 0.
        self.var = 0.
    def add(self, team, weight=1, paid=0.):
        if isinstance(team, (list, np.ndarray)):
            for t in team:
                self.add(t, weight)
            return
        if team in self._teams['Team'].values:
            if self._teams.loc[self._teams['Team']==team, 'Amount'].values[0] > 0: # overwriting, remove from tot
                self.totpaid -= self._teams.loc[self._teams['Team']==team, 'Amount']
            self._teams.loc[self._teams['Team']==team, 'Fraction Owned'] = weight
            self._teams.loc[self._teams['Team']==team, 'Amount'] = paid
            self.totpaid += paid
        else:
            raise KeyError("Team name {0} not found.".format(team))
    
    def to_npy(self, filename):
        np.save(filename, self.array)
    
    def from_npy(self, filename):
        weights = np.load(filename)
        self._teams['Fraction Owned'] = weights
        
    def sim_results(self, simtourneys):
        return np.dot(simtourneys, self.array)
    
    @property
    def teams(self):
        return self._teams[self._teams['Fraction Owned'] > 0]       
    
    @property
    def array(self):
        return self._teams['Fraction Owned'].values  
    
    def plot(self, simtourneys, ax=None, pool=1, **kwargs): # if pool not passed, just gives fraction of pool
        if ax is None:
            fig, ax = plt.subplots(figsize=(6,3))
        
        simresults = np.dot(simtourneys, self.array)
        counts, bins = np.histogram(simresults*pool-self.totpaid, bins=30)
        ax.bar(bins[:-1], counts/counts.sum(), np.diff(bins), **kwargs)
        ax.set_xlabel('Money Won')