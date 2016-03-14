import pandas as pd
import numpy as np

df = pd.read_csv('data/fulldata.csv', index_col=0)
dfsplit = np.array_split(df, 24)

for i, d in enumerate(dfsplit):
    d.to_csv('data/fulldata'+str(i)+'.csv', encoding='ascii')
