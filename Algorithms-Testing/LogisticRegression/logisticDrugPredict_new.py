import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import train_test_split

min_max_scaler = preprocessing.MinMaxScaler(feature_range=(-1,1))
#df = pd.read_csv("drugdata3.csv", header=0)
df=pd.read_csv('drugdata.csv', header=0)
input_columns = ['AGE','GENDER','RACE']
#input_columns = ['AGE','GENDER','RACE','ETHNIC','MARSTAT','EDUC','EMPLOY','DETNLF','PREG','VET','LIVARAG','PRIMINC','ARRESTS','STFIPS','CBSA','PMSA','REGION','DIVISION','SERVSETD']
#input_columns = ['DISYR','AGE','GENDER','RACE','ETHNIC','MARSTAT','EDUC','EMPLOY','DETNLF','PREG','VET','LIVARAG','PRIMINC','ARRESTS','STFIPS','CBSA','PMSA','REGION','DIVISION','SERVSETD']

# output_columns = ["ALCFLG"]
output_columns = ["MARFLG"]
#output_columns = ["COKEFLG"]

X = df[input_columns].values
X = np.array(X)
X = min_max_scaler.fit_transform(X)
Y = df[output_columns].values
Y = np.array(Y)


X_train,X_test,Y_train,Y_test = train_test_split(X,Y,test_size=0.1)
# train scikit learn model
clf = LogisticRegression()
clf.fit(X_train,Y_train)

#print "Model is trained:::"
#print 'score Scikit learn: ', clf.score(X_test,Y_test)
age=5
age=long(((age-1)*2)/11)
print age
sex=5
race=10
#test1=[[1,1,1]]
test1=[[age,sex,race]]
print clf.predict_proba(test1)
#print clf.predict(test1)
