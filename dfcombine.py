import pandas as pd
import numpy as np

from subprocess import call

dfs = []
for i in range(100):
    dfs.append(pd.read_csv('data/nfulldata{0}.csv'.format(i), index_col=0)

dfnew = pd.concat(dfs)
dfnew.to_csv('data/nfulldata.csv', encoding='ascii')
