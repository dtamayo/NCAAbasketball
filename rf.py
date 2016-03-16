import pandas as pd
import numpy as np
import sys

id = sys.argv[1]
size = np.float(sys.argv[2])

tourney_df = pd.read_csv("data/fulldatasortedcut.csv", index_col=0)
tourney_df = tourney_df.fillna(-1000000)

featureList = tourney_df.columns[12:-1]

y = tourney_df['team0Win'].values # results
X = tourney_df[featureList].values # features

from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=2721)

from sklearn import svm
from sklearn.cross_validation import StratifiedShuffleSplit
from sklearn.grid_search import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.calibration import calibration_curve

X_train_sample = X_train[0:size]
y_train_sample = y_train[0:size]
   
cv_s = StratifiedShuffleSplit(y_train_sample,  n_iter=10 , test_size=0.1, random_state=42)
rfc = RandomForestClassifier(max_features= 'auto' ,n_estimators=50) 
param_grid = { 
               'n_estimators': [30],
                       'max_features': ['sqrt']}
CV_rfc = GridSearchCV(n_jobs=-1, estimator=rfc, scoring="log_loss", param_grid=param_grid, cv=cv_s)
CV_rfc.fit(X_train_sample, y_train_sample)

model = CV_rfc.best_estimator_
y_pred = model.predict_proba(X_test) # probability that team0 wins (what Kaggle calls team 1, and wants for submission)
from sklearn import metrics
test_score = metrics.log_loss(y_test, y_pred)

import pickle
with open('rf{0}.pickle'.format(id), 'wb') as f:
    pickle.dump([size, CV_rfc, test_score], f)
