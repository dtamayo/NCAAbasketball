import pandas as pd
import numpy as np

df = pd.read_csv('data/tourneydata.csv', index_col=0)
dfsplit = np.array_split(df, 12)

for i, d in enumerate(dfsplit):
    d.to_csv('data/tourneydata'+str(i)+'.csv', encoding='ascii')
