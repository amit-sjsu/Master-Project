import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import train_test_split

min_max_scaler = preprocessing.MinMaxScaler(feature_range=(-1,1))
df1 = pd.read_csv("drugdata3.csv", header=0)
df=pd.read_csv('testDate.csv', sep='\t')
input_columns = ['AGE','GENDER','RACE','ETHNIC','MARSTAT','EDUC','EMPLOY','DETNLF','PREG','VET','LIVARAG','PRIMINC','ARRESTS','STFIPS','CBSA','PMSA','REGION','DIVISION','SERVSETD']
#input_columns = ['DISYR','AGE','GENDER','RACE','ETHNIC','MARSTAT','EDUC','EMPLOY','DETNLF','PREG','VET','LIVARAG','PRIMINC','ARRESTS','STFIPS','CBSA','PMSA','REGION','DIVISION','SERVSETD']

# output_columns = ["ALCFLG"]
# output_columns = ["MARFLG"]
output_columns = ["COKEFLG"]

#'DISYR','AGE','GENDER','RACE','ETHNIC','MARSTAT','EDUC','EMPLOY','DETNLF','PREG','VET','LIVARAG','PRIMINC','ARRESTS','STFIPS','CBSA','PMSA','REGION','DIVISION','SERVSETD','METHUSE	DAYWAIT	REASON	LOS	PSOURCE	DETCRIM	NOPRIOR	SUB1	ROUTE1	FREQ1	FRSTUSE1	SUB2	ROUTE2	FREQ2	FRSTUSE2	SUB3	ROUTE3	FREQ3	FRSTUSE3	NUMSUBS	IDU	ALCFLG	COKEFLG	MARFLG	HERFLG	METHFLG	OPSYNFLG	PCPFLG	HALLFLG	MTHAMFLG	AMPHFLG	STIMFLG	BENZFLG	TRNQFLG	BARBFLG	SEDHPFLG	INHFLG	OTCFLG	OTHERFLG	ALCDRUG	DSMCRIT	PSYPROB	HLTHINS	PRIMPAY"





#print df1[target_col1].values


#df.columns = ["AGE","EDUC","EMPLOY","SUB1"]
X = df[input_columns].values
X = np.array(X)
X = min_max_scaler.fit_transform(X)
Y = df[output_columns].values
Y = np.array(Y)


X_train,X_test,Y_train,Y_test = train_test_split(X,Y,test_size=0.1)
#print(len(X_train));
#print(len(X_test));
#print(X_train.shape);
#print(X_test.shape);
# train scikit learn model
clf = LogisticRegression()
clf.fit(X_train,Y_train)

print "Model is trained:::"
#print(clf);
print 'score Scikit learn: ', clf.score(X_test,Y_test)
print clf.predict_proba(X_test)
print clf.predict(X_test)
#RACE, EMPLOYMENT STATUS, LIVING ARRANGEMENTS, >------ SUB1
