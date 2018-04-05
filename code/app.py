from flask import Flask, send_file, render_template, jsonify
import xlrd
import csv
import json
from model import db
from model import Age
from model import Sex
from model import Race
from model import State
import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import train_test_split

from model import CreateDB
import config
from config import GetConfigDataHarshit as config_data
#import simplejson as json
from sqlalchemy.exc import IntegrityError
import os
from flask import request

#initate flask app;
app = Flask(__name__)
app.config.from_object(config)
CreateDB()
db.create_all()



min_max_scaler = preprocessing.MinMaxScaler(feature_range=(-1,1))
df=pd.read_csv('drugdata.csv', header=0)
input_columns = ['AGE','GENDER','RACE','STFIPS']

output_columns_alc = ["ALCFLG"]
output_columns_mar = ["MARFLG"]
output_columns_cok = ["COKEFLG"]

X = df[input_columns].values
X = np.array(X)
X = min_max_scaler.fit_transform(X)
Yalc = df[output_columns_alc].values
Yalc = np.array(Yalc)
Ymar = df[output_columns_mar].values
Ymar = np.array(Ymar)
Ycok = df[output_columns_cok].values
Ycok = np.array(Ycok)

X_train_alc,X_test_alc,Y_train_alc,Y_test_alc = train_test_split(X,Yalc,test_size=0.2)
X_train_mar,X_test_mar,Y_train_mar,Y_test_mar = train_test_split(X,Ymar,test_size=0.2)
X_train_cok,X_test_cok,Y_train_cok,Y_test_cok = train_test_split(X,Ycok,test_size=0.2)
clf1 = LogisticRegression()
clf2 = LogisticRegression()
clf3 = LogisticRegression()
clf1.fit(X_train_alc, Y_train_alc)
clf2.fit(X_train_mar, Y_train_mar)
clf3.fit(X_train_cok, Y_train_cok)








@app.route("/")
def index():
    result = State.query.all()
    state_json = json.load(open('state_map.json'))
    state_data = []
    for row in result:
        small_json = {"hc-key": "", "value": 999}
        small_json["hc-key"] = str("us-"+ state_json.get(row.state).get('code').lower())
        small_json["value"] = round(float(state_json.get(row.state).get('drug'))/float(state_json.get(row.state).get('census')), 4)
        state_data.append(small_json)
    for row in state_data:
        print row
    return render_template("index.html", state_data=state_data)


def calculateIndividualDrug(personData={},*args):
    age = 12
    race = 10
    state=personData["State"]

    #print (personData)

    stateMap=json.load(open('state_map.json'))
    state=stateMap.get(state).get("drug")

    if (personData["Age"]):
        if(personData["Age"]=="12" or personData["Age"]=="13" or personData["Age"]=="14"):
            age=2
        elif(personData["Age"]=="15" or personData["Age"]=="16" or personData["Age"]=="17"):
            age=3
        elif(personData["Age"]=="18" or personData["Age"]=="19" or personData["Age"]=="20"):
            age = 4
        elif(personData["Age"]=="21" or personData["Age"]=="22" or personData["Age"]=="23" or personData["Age"]=="24"):
            age = 5
        elif (personData["Age"] =="25_29"):
            age = 6
        elif (personData["Age"] =="30_34"):
            age = 7
        elif (personData["Age"] =="35_39"):
            age = 8
        elif (personData["Age"] =="40_44"):
            age = 9
        elif (personData["Age"] =="45_49"):
            age = 10
        elif (personData["Age"] =="50_54"):
            age = 11
        elif (personData["Age"] == "55+"):
            age = 12


    if (personData["Race"]):
        if(personData["Race"]=="American_Indian_Alaska_Native"):
            race=2
        elif(personData["Race"]=="Asian"):
            race=13
        elif(personData["Race"] =="Two_Or_More_Race"):
            race = 21
        elif(personData["Race"] =="Native_Hawaiian_Pacific_Islander"):
            race = 23
        elif (personData["Race"] =="Some_Other_Single_Race"):
            race = 20
        elif (personData["Race"] =="white"):
            race = 5
        elif (personData["Race"] == "Black_sAfrican"):
            race = 4

    print "age="
    print age
    if personData["Sex"] == "male":
        sexValue = .818
    else:
        sexValue = 1.0


    #print age
    #print race
    #print  sexValue



    age = round(-1 + (((float(age) - 2.00)*2 / 10)),2)
    race = round(-1 + (((race + 9) * 2) / 32.00),2)
    state = round(-1 + (((float(state) - 1) * 2) / 54.00),2)



    test1 = [[age, sexValue, race, state]]
    print test1
    alcohol= clf1.predict_proba(test1)[0][1]
    marijuana= clf2.predict_proba(test1)[0][1]
    cocaine= clf3.predict_proba(test1)[0][1]

    individual = {"alcohol": alcohol,
              "marijuana": marijuana,
              "cocaine": cocaine}
    #print individual

    return individual




def getProbabiltyfromDatabase(personData={},*args):

    Total_data=State.query.filter_by(state=personData["State"]).first();
    #personData["State"]=Total_data.id;
    p_drug_addict=Total_data.drug_count/Total_data.census_count;
    finalProbability = p_drug_addict;

    if(personData["Age"]):
        result=Age.query.filter_by(age=personData["Age"]).first()
        print (result)
        if result.age_drug_probability == 0 or result.age_probability ==0:
            return 0
        else:
            finalProbability=finalProbability * (result.age_drug_probability/result.age_probability);

    if (personData["Sex"]):
        result = Sex.query.filter_by(sex=personData["Sex"]).first()
        if result.sex_drug_probability == 0 or result.sex_probability == 0:
            return 0
        else:
            finalProbability = finalProbability * (result.sex_drug_probability / result.sex_probability);

    if (personData["Race"]):
        result = Race.query.filter_by(race=personData["Race"]).first()
        if result.race_drug_probability == 0 or result.race_probability == 0:
            return 0
        else:
            finalProbability = finalProbability * (result.race_drug_probability / result.race_probability);

    return finalProbability




@app.route('/Result', methods=['GET','POST'])
def Result():
    if request.method == 'POST':
        age= request.form['age'];
        race = request.form['race']
        sex = request.form['sex']
        state = request.form['state']

    person={"Age":age,
            "Sex":sex,
            "Race":race,
            "State":state}

    #print person["Age"], person
    final_probability = getProbabiltyfromDatabase(person)
    individual=calculateIndividualDrug(person)
    print individual["cocaine"], individual["alcohol"], individual["marijuana"]
    #return render_template("analysis.html")
    cocain_probability=round(individual["cocaine"]*100, 2)
    alcohol_probability=round(individual["alcohol"]*100, 2)
    marijuana_probability=round(individual["marijuana"]*100, 2)

    return jsonify(data={'probability': final_probability, 'cocain_probability': cocain_probability,
                         'alcohol_probability': alcohol_probability, 'marijuana_probability': marijuana_probability});
    # return render_template(probability=final_probability, cocain_probability=cocain_probability, alcohol_probability=alcohol_probability, marijuana_probability=marijuana_probability)


@app.route('/stateData', methods=['GET'])
def stateData():
    if 'state' in request.args:
        state_stats = getStateStatistics(request.args['state'])

    return render_template("index.html", state_stats=state_stats)

def getStateStatistics(state):
    json = {"race":{}, "sex":{}, "age":{}}
    small_json_race = {}
    small_json_sex = {}
    small_json_age = dict()
    small_json_age_temp = dict()
    age_data_temp = Age.query.filter_by(state=state).all()
    sex_data = Sex.query.filter_by(state=state).all()
    race_data = Race.query.filter_by(state=state).all()

    temp_dict = {
        "12": "12-14",
        "13": "12-24",
        "14": "12-14",
        "15": "15-19",
        "16": "15-19",
        "17": "15-19",
        "18": "15-19",
        "19": "15-19",
        "20": "20-24",
        "21": "20-24",
        "22": "20-24",
        "23": "20-24",
        "24": "20-24",
        "25": "20-24",
        "25_29": "25-29",
        "30_34": "30-34",
        "35_39": "35-39",
        "40_44": "40-44",
        "45_49": "45-49",
        "50_54": "50-54",
        "55+": "55+"
    }

    for row in age_data_temp:
        age_string = str(row.age)
        probability_value = float(row.age_drug_probability)
        small_json_age_temp[age_string] = probability_value

    for row in sex_data:
        sex_string = str(row.sex)
        probability_value = float(row.sex_drug_probability)
        small_json_sex[sex_string] = probability_value

    for row in race_data:
        race_string = str(row.race)
        probability_value = float(row.race_drug_probability)
        small_json_race[race_string] = probability_value

    json["race"] = small_json_race;
    json["sex"] = small_json_sex;
    json["age"] = small_json_age;

    return json

if __name__ == '__main__':
    app.run(port=5003);
