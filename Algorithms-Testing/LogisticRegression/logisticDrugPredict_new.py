import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import train_test_split

min_max_scaler = preprocessing.MinMaxScaler(feature_range=(-1,1))
df = pd.read_csv("drugdata3.csv", header=0)
df.columns = ["AGE","EDUC","EMPLOY","SUB1"]
X = df[["AGE","EDUC","EMPLOY"]]
X = np.array(X)
X = min_max_scaler.fit_transform(X)
Y = df["SUB1"]
Y = np.array(Y)


X_train,X_test,Y_train,Y_test = train_test_split(X,Y,test_size=0.1)
print(len(X_train));
print(len(X_test));
#print(X_train.shape);
#print(X_test.shape);
# train scikit learn model
clf = LogisticRegression()
clf.fit(X_train,Y_train)

#print(clf);
print 'score Scikit learn: ', clf.score(X_test,Y_test)
#RACE, EMPLOYMENT STATUS, LIVING ARRANGEMENTS, >------ SUB1
