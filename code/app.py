from flask import Flask, send_file, render_template
import xlrd
import csv
import json
from model import db
from model import Age
from model import Sex
from model import Race
from model import State

from model import CreateDB
import config
from config import GetConfigDataAmit as config_data
#import simplejson as json
from sqlalchemy.exc import IntegrityError
import os
from flask import request

# initate flask app
app = Flask(__name__)
app.config.from_object(config)
CreateDB()
db.create_all()


@app.route("/")
def index():
    return send_file("templates/index.html")

@app.route('/dd')
def storeProbability():
    state_data = json.load(open('state_map.json')) # Contains references columns in data sets
    # pprint(state_data)
    # race_json = {}
    # sex_json = {}
    # age_json = {}
    array_obj=[]
    for attribute, value in state_data.items():
        race_json = raceCalculation(value['drug'], value['census'])  # example usage
        #print(race_json)
        sex_json = userSexData(value['drug'], value['census'])  # example usage
        #print(sex_json)
        age_json,array_obj = getUserAgeData(value['drug'], value['census'])  # example usage
        insertProbabilityToDatabase(array_obj, attribute, age_json, sex_json, race_json)

    # print(age_json)
    print(sex_json)
    # print(race_json)
    print(array_obj[0])
    print(array_obj[1])
    #insertProbabilityToDatabase(array_obj,attribute,age_json,sex_json,race_json)

    return ""


def raceCalculation(drugColVal, censusColVal):
    race_workbook = xlrd.open_workbook(config_data.CENSUS_PATH+'POP01.xls')
    worksheet1 = race_workbook.sheet_by_name('POP01F')
    worksheet2 = race_workbook.sheet_by_name('POP01G')
    worksheet3 = race_workbook.sheet_by_name('POP01I')
    worksheet4 = race_workbook.sheet_by_name('POP01J')
    race_workbook2 = xlrd.open_workbook(config_data.CENSUS_PATH+'POP02.xls')
    worksheet5 = race_workbook2.sheet_by_name('POP02A')
    census_white = worksheet1.cell(censusColVal, 7).value
    census_Black_African = worksheet2.cell(censusColVal, 15).value
    census_American_Indian_Alaska_Native = worksheet2.cell(censusColVal, 38).value
    census_Asian = worksheet3.cell(censusColVal, 7).value
    census_Native_Hawaiian_Pacific_Islander = worksheet4.cell(censusColVal, 31).value
    census_Some_Other_Single_Race = worksheet5.cell(censusColVal, 15).value
    census_Two_Or_More_Race = worksheet5.cell(censusColVal, 31).value

    drug_white = 0.0
    drug_Black_African = 0.0
    drug_American_Indian_Alaska_Native = 0.0
    drug_Asian = 0.0
    drug_Native_Hawaiian_Pacific_Islander = 0.0
    drug_Some_Other_Single_Race = 0.0
    drug_Two_Or_More_Race = 0.0

    with open(config_data.DRUG_PATH, 'r') as tsvin:
        tsvin = csv.reader(tsvin, delimiter='\t')

        for row in tsvin:
            if row[15] == str(drugColVal):
                if row[4] == '5':
                    drug_white = drug_white + 1
                if row[4] == '4':
                    drug_Black_African = drug_Black_African + 1
                if row[4] == '2' or row[4] == '1':
                    drug_American_Indian_Alaska_Native = drug_American_Indian_Alaska_Native + 1
                if row[4] == '3' or row[4] == '13':
                    drug_Asian = drug_Asian + 1
                if row[4] == '23':
                    drug_Native_Hawaiian_Pacific_Islander = drug_Native_Hawaiian_Pacific_Islander + 1
                if row[4] == '20':
                    drug_Some_Other_Single_Race = drug_Some_Other_Single_Race + 1
                if row[4] == '21':
                    drug_Two_Or_More_Race = drug_Two_Or_More_Race + 1
    data = {}
    data = {
            'white': {
                'census_data': census_white,
                'drug_data': drug_white
            },
            'Black_sAfrican': {
                'census_data': census_Black_African,
                'drug_data': drug_Black_African
            },
            'American_Indian_Alaska_Native': {
                'census_data': census_American_Indian_Alaska_Native,
                'drug_data': drug_American_Indian_Alaska_Native
            },
            'Asian': {
                'census_data': census_Asian,
                'drug_data': drug_Asian
            },
            'Native_Hawaiian_Pacific_Islander': {
                'census_data': census_Native_Hawaiian_Pacific_Islander,
                'drug_data': drug_Native_Hawaiian_Pacific_Islander
            },
            'Some_Other_Single_Race': {
                'census_data': census_Some_Other_Single_Race,
                'drug_data': drug_Some_Other_Single_Race
            },
            'Two_Or_More_Race': {
                'census_data': census_Two_Or_More_Race,
                'drug_data': drug_Two_Or_More_Race
            }
    }

    return data

def userSexData(drugColVal, censusColVal):
    drug_male = 0.0
    drug_female = 0.0

    with open(config_data.DRUG_PATH, 'r') as tsvin:
        tsvin = csv.reader(tsvin, delimiter='\t')
        for row in tsvin:
            if row[15] == str(drugColVal):
                if row[3] == '1':
                    drug_male = drug_male + 1
                if row[3] == '2':
                    drug_female = drug_female + 1

    workbook_sex = xlrd.open_workbook(config_data.CENSUS_PATH + 'SEX01.xls')
    worksheet_sex_1 = workbook_sex.sheet_by_name('Sheet1')
    census_sex_male = worksheet_sex_1.cell(censusColVal, 7).value

    worksheet_sex_2 = workbook_sex.sheet_by_name('Sheet2')
    census_sex_female = worksheet_sex_2.cell(censusColVal, 19).value

    sex_data = {
        "male": {
            "census_data": census_sex_male,
            "drug_data": drug_male
        },
        "female": {
            "census_data": census_sex_female,
            "drug_data": drug_female
        }
    }

    return sex_data


def insertProbabilityToDatabase(stateCensusTotalPopulation = [],state='',age_state_census={} ,sex={},race={}, *args):
   # p_drug_addict = stateCensusTotalPopulation[0] / stateCensusTotalPopulation[1];

   # print sex
   # print "==========>"
   # print race
   probability=[];
   k=0;
   Querries=[];
   if (bool(age_state_census)):
       probability=calculateProbabilty(age_state_census, stateCensusTotalPopulation);
       print(probability)
       for items in probability:
           print(items)
           print(items[0], round(float(items[2]), 2),round(float(items[1]), 2))
           Querries.append(Age(age=items[0] , age_probability=round(float(items[2]), 2), age_drug_probability=round(float(items[1]), 2) , state=state));


   if (bool(sex)):
       probability = calculateProbabilty(sex, stateCensusTotalPopulation);
       for items in probability:
           Querries.append(Sex(sex=items[0], sex_probability=round(float(items[2]), 2), sex_drug_probability=round(float(items[1]), 2), state=state));



   if (bool(race)):
       probability = calculateProbabilty(race, stateCensusTotalPopulation);
       for items in probability:
           Querries.append(Race(race=items[0], race_probability=round(float(items[2]), 2), race_drug_probability=round(float(items[1]), 2), state=state));


   for querry in Querries:
       db.session.add(querry)
   db.session.commit()


def calculateProbabilty(values={},stateCensusTotalPopulation=[]):
    # value = json.loads(values)
    # print vaule, stateCensusTotalPopulation
    h=0;  w=3; i=0;
    for k,v in values.items():
        h=h+1;

    # print h
    Matrix = [[0 for x in range(w)] for y in range(h)]

    # print Matrix

    for k, v in values.items():
        p_drug = v["drug_data"] / stateCensusTotalPopulation[0];
        p = v["census_data"] / stateCensusTotalPopulation[1];
        Matrix[i]=([k,p_drug,p]);
        i=i+1;

    # print "===========>111111"
    # print Matrix
    return Matrix


def getProbabiltyfromDatabase(personData={},*args):

    Total_data=State.query.filter_by(state=personData["State"]).first();
    print Total_data;
    p_drug_addict=Total_data.drug_count/Total_data.census_count;
    finalProbability = p_drug_addict;

    if(personData["Age"]):
        result=Age.query.filter_by(age=personData["Age"]).first()
        finalProbability=finalProbability * (result.age_drug_probability/result.age_probability);

    if (personData["Sex"]):
        result = Sex.query.filter_by(sex=personData["Sex"]).first()
        finalProbability = finalProbability * (result.sex_drug_probability / result.sex_probability);

    if (personData["Race"]):
        result = Race.query.filter_by(race=personData["Race"]).first()
        finalProbability = finalProbability * (result.race_drug_probability / result.race_probability);

    return finalProbability


@app.route('/dd1')
def getUserAgeData(drugColVal, censusColVal):
    drug_column = str(drugColVal)
    census_state_column=censusColVal


    ##########Drug Data Start

    drug_count_12_14 = 0
    drug_count_15_17 = 0
    drug_count_18_20 = 0
    drug_count_21_24 = 0
    drug_count_25_29 = 0
    drug_count_30_34 = 0
    drug_count_35_39 = 0
    drug_count_40_44 = 0
    drug_count_45_49 = 0
    drug_count_50_54 = 0
    drug_count_55_100 = 0
    total_drug_count = 0.0
    with open(config_data.DRUG_PATH, 'r') as tsvin:
        tsvin = csv.reader(tsvin, delimiter='\t')
        for row in tsvin:
            if row[15] == drug_column and row[2] == '2':
                drug_count_12_14 = drug_count_12_14+1
            if row[15] == drug_column and row[2] == '3':
                drug_count_15_17 = drug_count_15_17 + 1
            if row[15] == drug_column and row[2] == '4':
                drug_count_18_20 = drug_count_18_20 + 1
            if row[15] == drug_column and row[2] == '5':
                drug_count_21_24 = drug_count_21_24 + 1
            if row[15] == drug_column and row[2] == '6':
                drug_count_25_29 = drug_count_25_29 + 1
            if row[15] == drug_column and row[2] == '7':
                drug_count_30_34 = drug_count_30_34 + 1
            if row[15] == drug_column and row[2] == '8':
                drug_count_35_39 = drug_count_35_39 + 1
            if row[15] == drug_column and row[2] == '9':
                drug_count_40_44 = drug_count_40_44 + 1
            if row[15] == drug_column and row[2] == '10':
                drug_count_45_49 = drug_count_45_49 + 1
            if row[15] == drug_column and row[2] == '11':
                drug_count_50_54 = drug_count_50_54 + 1
            if row[15] == drug_column and row[2] == '12':
                drug_count_55_100 = drug_count_55_100 + 1
            if row[15] == drug_column:
                total_drug_count = total_drug_count+1


    ##########Drug Data End

    workbook_age_01 = xlrd.open_workbook(config_data.CENSUS_PATH+'AGE01.xls')
    worksheet_age_01_sheet1 = workbook_age_01.sheet_by_name('Sheet1')
    worksheet_age_01_sheet7 = workbook_age_01.sheet_by_name('Sheet7')
    worksheet_age_01_sheet9 = workbook_age_01.sheet_by_name('Sheet9')
    census_10_14 = (worksheet_age_01_sheet7.cell(census_state_column, 31).value);
    census_15_19 = (worksheet_age_01_sheet9.cell(census_state_column, 3).value);
    total_census_count = worksheet_age_01_sheet1.cell(census_state_column, 15).value

    workbook_age_02 = xlrd.open_workbook(config_data.CENSUS_PATH+'AGE02.xls')
    worksheet_age_02_sheet3 = workbook_age_02.sheet_by_name('Sheet3')
    worksheet_age_02_sheet5 = workbook_age_02.sheet_by_name('Sheet5')
    worksheet_age_02_sheet7 = workbook_age_02.sheet_by_name('Sheet7')
    worksheet_age_02_sheet8 = workbook_age_02.sheet_by_name('Sheet8')
    worksheet_age_02_sheet10 = workbook_age_02.sheet_by_name('Sheet10')
    census_20_24 = (worksheet_age_02_sheet3.cell(census_state_column, 35).value)
    census_25_29 = worksheet_age_02_sheet5.cell(census_state_column, 15).value
    census_30_34 = worksheet_age_02_sheet7.cell(census_state_column, 11).value
    census_35_39 = worksheet_age_02_sheet8.cell(census_state_column, 27).value
    census_40_44 = worksheet_age_02_sheet10.cell(census_state_column, 19).value

    workbook_age_03 = xlrd.open_workbook(config_data.CENSUS_PATH+'AGE03.xls')
    worksheet_age_03_sheet1 = workbook_age_03.sheet_by_name('Sheet1')
    worksheet_age_03_sheet3 = workbook_age_03.sheet_by_name('Sheet3')
    worksheet_age_03_sheet5 = workbook_age_03.sheet_by_name('Sheet5')
    worksheet_age_03_sheet6 = workbook_age_03.sheet_by_name('Sheet6')
    worksheet_age_03_sheet9 = workbook_age_03.sheet_by_name('Sheet9')
    census_45_49 = (worksheet_age_03_sheet1.cell(census_state_column, 35).value)
    census_50_54 = (worksheet_age_03_sheet3.cell(census_state_column, 31).value)
    census_55_59 = (worksheet_age_03_sheet5.cell(census_state_column, 11).value)
    census_60_64 = (worksheet_age_03_sheet6.cell(census_state_column, 31).value)
    census_65_74 = (worksheet_age_03_sheet9.cell(census_state_column, 23).value)

    workbook_age_04 = xlrd.open_workbook(config_data.CENSUS_PATH+'AGE04.xls')
    worksheet_age_04_sheet3 = workbook_age_03.sheet_by_name('Sheet3')
    census_75_84 = (worksheet_age_04_sheet3.cell(census_state_column, 31).value)

    age_data = {}
    age_data["12"]={"census_data": census_10_14/4,"drug_data":drug_count_12_14/3}
    age_data["13"] = {"census_data": census_10_14 / 4, "drug_data": drug_count_12_14 / 3}
    age_data["14"] = {"census_data": census_10_14 / 4, "drug_data": drug_count_12_14 / 3}
    age_data["15"] = {"census_data": census_15_19 / 5, "drug_data": drug_count_15_17 / 3}
    age_data["16"] = {"census_data": census_15_19 / 5, "drug_data": drug_count_15_17 / 3}
    age_data["17"] = {"census_data": census_15_19 / 5, "drug_data": drug_count_15_17 / 3}
    age_data["18"] = {"census_data": census_15_19 / 5, "drug_data": drug_count_18_20 / 3}
    age_data["19"] = {"census_data": census_15_19 / 5, "drug_data": drug_count_18_20 / 3}
    age_data["20"] = {"census_data": census_20_24 / 5, "drug_data": drug_count_18_20 / 3}
    age_data["21"] = {"census_data": census_20_24 / 5, "drug_data": drug_count_21_24 / 4}
    age_data["22"] = {"census_data": census_20_24 / 5, "drug_data": drug_count_21_24 / 4}
    age_data["23"] = {"census_data": census_20_24 / 5, "drug_data": drug_count_21_24 / 4}
    age_data["24"] = {"census_data": census_20_24 / 5, "drug_data": drug_count_21_24 / 4}

    age_data["25_29"] = {"census_data": census_25_29 , "drug_data": drug_count_25_29}
    age_data["30_34"] = {"census_data": census_30_34, "drug_data": drug_count_30_34}
    age_data["35_39"] = {"census_data": census_35_39, "drug_data": drug_count_35_39}
    age_data["40_44"] = {"census_data": census_40_44, "drug_data": drug_count_40_44}
    age_data["45_49"] = {"census_data": census_45_49, "drug_data": drug_count_45_49}
    age_data["50_54"] = {"census_data": census_50_54, "drug_data": drug_count_50_54}
    age_data["55+"] = {"census_data": census_55_59+census_60_64+ census_65_74+census_75_84 , "drug_data": drug_count_55_100}
    array_obj = []
    array_obj.append(total_drug_count)
    array_obj.append(total_census_count)
    return age_data, array_obj;


@app.route('/')
def index():
    return render_template("NewIndex.html")


@app.route('/Result', methods=['GET','POST'])
def Result():
    if request.method == 'POST':
        age= request.form['age'];
        race = request.form['race']
        sex = request.form['sex']

    person={"Age":age,
            "Sex":sex,
            "Race":race,
            "State":'ALABAMA'}

    print person

    print getProbabiltyfromDatabase(person)


    return render_template("analysis.html")

if __name__ == '__main__':
    app.run(port=5004);
