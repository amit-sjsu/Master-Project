from flask import Flask, send_file, render_template
import xlrd
import csv
import json
from model import db
from model import Age
from model import CreateDB

#import simplejson as json
from sqlalchemy.exc import IntegrityError
import os

# initate flask app
app = Flask(__name__)
CreateDB()
db.create_all()


@app.route("/")
def index():
    return send_file("templates/index.html")

@app.route('/dd')
def storeProbability():
    state_data = json.load(open('state_map.json'))
    # pprint(state_data)
    race_json = {}
    sex_json = {}
    for attribute, value in state_data.iteritems():
        race_json[attribute] = raceCalculation(value['drug'], value['census'])  # example usage
        sex_json[attribute] = userSexData(value['drug'], value['census'])  # example usage


def raceCalculation(drugColVal, censusColVal):
    race_workbook = xlrd.open_workbook('/Users/anshul/Documents/CMPE 295B/POP/POP01.xls')
    worksheet1 = race_workbook.sheet_by_name('POP01F')
    worksheet2 = race_workbook.sheet_by_name('POP01G')
    worksheet3 = race_workbook.sheet_by_name('POP01I')
    worksheet4 = race_workbook.sheet_by_name('POP01J')
    race_workbook2 = xlrd.open_workbook('/Users/anshul/Documents/CMPE 295B/POP/POP02.xls')
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

    with open('/Users/anshul/Documents/CMPE295A/ICPSR_35074/DS0001/35074-0001-Data.tsv', 'r') as tsvin:
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
    data = [
        {'white': {'census_data': census_white, 'drug_data': drug_white}},
        {'Black_African': {'census_data': census_Black_African, 'drug_data': drug_Black_African}},
        {'American_Indian_Alaska_Native': {'census_data': census_American_Indian_Alaska_Native,
                                           'drug_data': drug_American_Indian_Alaska_Native}},
        {'Asian': {'census_data': census_Asian, 'drug_data': drug_Asian}},
        {'Native_Hawaiian_Pacific_Islander': {'census_data': census_Native_Hawaiian_Pacific_Islander,
                                              'drug_data': drug_Native_Hawaiian_Pacific_Islander}},
        {'Some_Other_Single_Race': {'census_data': census_Some_Other_Single_Race,
                                    'drug_data': drug_Some_Other_Single_Race}},
        {'Two_Or_More_Race': {'census_data': census_Two_Or_More_Race, 'drug_data': drug_Two_Or_More_Race}}
    ]
    return data

def userAgeData():
    workbook = xlrd.open_workbook('/Users/Harshit/LECTURES/295B/Code/Master-Project/code/AGE02.xls')
    worksheet = workbook.sheet_by_name('Sheet5')
    worksheet1 = workbook.sheet_by_name('Sheet7')
    worksheet_age_02_sheet3=workbook.sheet_by_name('Sheet3')
    census_albama_25_29 = worksheet.cell(2, 15).value
    census_california_25_29 = worksheet.cell(192, 15).value
    census_florida_25_29 = worksheet.cell(331, 15).value
    census_new_york_25_29 = worksheet.cell(1863, 15).value
    census_albama_30_34 = worksheet1.cell(2, 11).value
    census_california_30_34 = worksheet1.cell(192, 11).value
    census_florida_30_34 = worksheet1.cell(331, 11).value
    census_new_york_30_34 = worksheet1.cell(1863, 11).value
    cal_count_12_14 = 0
    cal_count_15_17 = 0
    cal_count_18_20 = 0
    cal_count_21_24 = 0
    cal_count_25_29 = 0
    albama_count_25_29 = 0
    ny_count_25_29 = 0
    fl_count_25_29 = 0
    cal_count_30_34 = 0
    albama_count_30_34 = 0
    ny_count_30_34 = 0
    fl_count_30_34 = 0

    cal_count = 0
    albama_count = 0
    ny_count = 0
    fl_count = 0

    with open('/Users/Harshit/LECTURES/295B/Code/Master-Project/code/35074-0001-Data.tsv', 'r') as tsvin:
        tsvin = csv.reader(tsvin, delimiter='\t')
        for row in tsvin:
            if row[15] == '6' and row[2] == '2':
                cal_count_12_14 = cal_count_12_14+1
            if row[15] == '6' and row[2] == '3':
                cal_count_15_17 = cal_count_15_17+1
            if row[15] == '6' and row[2] == '4':
                cal_count_18_20 = cal_count_18_20+1
            if row[15] == '6' and row[2] == '5':
                cal_count_21_24 = cal_count_21_24+1
            if row[15] == '6' and row[2] == '6':
                cal_count_25_29 = cal_count_25_29+1
            if row[15] == '1' and row[2] == '6':
                albama_count_25_29 = albama_count_25_29+1
            if row[15] == '12' and row[2] == '6':
                fl_count_25_29 = fl_count_25_29+1
            if row[15] == '36' and row[2] == '6':
                ny_count_25_29 = ny_count_25_29+1
            if row[15] == '6' and row[2] == '7':
                cal_count_30_34 = cal_count_30_34+1
            if row[15] == '1' and row[2] == '7':
                albama_count_30_34 = albama_count_30_34+1
            if row[15] == '12' and row[2] == '7':
                ny_count_30_34 = ny_count_30_34+1
            if row[15] == '36' and row[2] == '7':
                fl_count_30_34 = fl_count_30_34+1

            if row[15] == '6':
                cal_count = cal_count+1
            if row[15] == '1':
                albama_count = albama_count+1
            if row[15] == '12':
                fl_count = fl_count+1
            if row[15] == '36':
                ny_count = ny_count+1


    workbook1 = xlrd.open_workbook('/Users/Harshit/LECTURES/295B/Code/Master-Project/code/AGE01.xls')
    worksheet2 = workbook1.sheet_by_name('Sheet1')
    census_albama = worksheet2.cell(2, 15).value
    census_california = worksheet2.cell(192, 15).value
    census_florida = worksheet2.cell(331, 15).value
    census_new_york = worksheet2.cell(1863, 15).value

    workbook_sex = xlrd.open_workbook('/Users/Harshit/LECTURES/295B/Code/Master-Project/code/SEX01.xls')
    worksheet_sex_1 = workbook_sex.sheet_by_name('Sheet1')
    census_sex_male_albama = worksheet_sex_1.cell(2, 7).value
    census_sex_male_california = worksheet_sex_1.cell(192, 7).value
    census_sex_male_florida = worksheet_sex_1.cell(331, 7).value
    census_sex_male_newyork = worksheet_sex_1.cell(1863, 7).value
    worksheet_sex_2 = workbook_sex.sheet_by_name('Sheet2')
    census_sex_female_albama = worksheet_sex_2.cell(2, 19).value
    census_sex_female_california = worksheet_sex_2.cell(192, 19).value
    census_sex_female_florida = worksheet_sex_2.cell(331, 19).value
    census_sex_female_newyork = worksheet_sex_2.cell(1863, 19).value

    print(census_albama)
    print(census_california)
    print(census_florida)
    print(census_new_york)
    print(census_albama_25_29)
    print(census_california_25_29)
    print(census_florida_25_29)
    print(census_new_york_25_29)
    print(cal_count_25_29)
    print(albama_count_25_29)
    print(fl_count_25_29)
    print(ny_count_25_29)

    print(cal_count)
    print(albama_count)
    print(fl_count)
    print(ny_count)

    data={}
    data['CA']=[{'age_25_29':{'census_data':census_california_25_29, 'drug_data':cal_count_25_29}},
                {'age_30_34':{'census_data':census_california_30_34, 'drug_data':cal_count_30_34}}]

    data['AL'] = [{'age_25_29': {'census_data': census_albama_25_29, 'drug_data': albama_count_25_29}},
                  {'age_30_34': {'census_data': census_albama_30_34, 'drug_data': albama_count_30_34}}]

    data['FL'] = [{'age_25_29': {'census_data': census_florida_25_29, 'drug_data': fl_count_25_29}},
                  {'age_30_34': {'census_data': census_florida_30_34, 'drug_data': fl_count_30_34}}]

    data['NY'] = [{'age_25_29': {'census_data': census_new_york_25_29, 'drug_data': ny_count_25_29}},
                  {'age_30_34': {'census_data': census_new_york_30_34, 'drug_data': ny_count_30_34}}]

# Sex data appended
    cal_count_male = 0
    albama_count_male = 0
    ny_count_male = 0
    fl_count_male = 0
    cal_count_female = 0
    albama_count_female = 0
    ny_count_female = 0
    fl_count_female = 0
    with open('/Users/Harshit/LECTURES/295B/Code/Master-Project/code/35074-0001-Data.tsv', 'r') as tsvin:
        tsvin = csv.reader(tsvin, delimiter='\t')
        for row in tsvin:
            if row[15] == '6' and row[3] == '1':
                cal_count_male = cal_count_male + 1
            if row[15] == '1' and row[3] == '1':
                albama_count_male = albama_count_male + 1
            if row[15] == '12' and row[3] == '1':
                fl_count_male = fl_count_male + 1
            if row[15] == '36' and row[3] == '1':
                ny_count_male = ny_count_male + 1
            if row[15] == '6' and row[3] == '2':
                cal_count_female = cal_count_female + 1
            if row[15] == '1' and row[3] == '2':
                albama_count_female = albama_count_female + 1
            if row[15] == '12' and row[3] == '2':
                ny_count_female = ny_count_female + 1
            if row[15] == '36' and row[3] == '2':
                fl_count_female = fl_count_female + 1

    p_ca_drug_addict = cal_count/census_california
    p_ca_25_29_da = cal_count_25_29/cal_count
    p_ca_25_29 = census_california_25_29/census_california

    p_ca_30_34_da = cal_count_30_34/cal_count
    p_ca_30_34 = census_california_30_34/census_california

    p_da_ca_25_29 = p_ca_drug_addict * p_ca_25_29_da / p_ca_25_29
    p_da_ca_30_34 = p_ca_drug_addict * p_ca_30_34_da / p_ca_30_34

    p_al_drug_addict = albama_count/census_albama
    p_al_25_29_da = albama_count_25_29/albama_count
    p_al_25_29 = census_albama_25_29/census_albama
    p_al_30_34_da = albama_count_30_34/albama_count
    p_al_30_34 = census_albama_30_34/census_albama

    p_da_al_25_29 = p_al_drug_addict * p_al_25_29_da / p_al_25_29
    p_da_al_30_34 = p_al_drug_addict * p_al_30_34_da / p_al_30_34


    p_ny_drug_addict = ny_count/census_new_york
    p_ny_25_29_da = ny_count_25_29/ny_count
    p_ny_25_29 = census_new_york_25_29/census_new_york
    p_ny_30_34_da = ny_count_30_34/ny_count
    p_ny_30_34 = census_new_york_30_34/census_new_york

    p_da_ny_25_29 = p_ny_drug_addict * p_ny_25_29_da / p_ny_25_29
    p_da_ny_30_34 = p_ny_drug_addict * p_ny_30_34_da / p_ny_30_34

    p_fl_drug_addict = fl_count/census_florida
    p_fl_25_29_da = fl_count_25_29/fl_count
    p_fl_25_29 = census_florida_25_29/census_florida
    p_fl_30_34_da = fl_count_30_34/fl_count
    p_fl_30_34 = census_florida_30_34/census_florida

    p_da_fl_25_29 = p_fl_drug_addict * p_fl_25_29_da / p_fl_25_29
    p_da_fl_30_34 = p_fl_drug_addict * p_fl_30_34_da / p_fl_30_34

    user = Age(age="fl_25_29", age_probability=p_fl_25_29, age_drug_probability=p_fl_30_34_da)
    db.session.add(user)
    db.session.commit()


    print(p_da_ca_25_29)
    print(p_da_ca_30_34)
    print(p_da_al_25_29)
    print(p_da_al_30_34)
    print(p_da_ny_25_29)
    print(p_da_ny_30_34)
    print(p_da_fl_25_29)
    print(p_da_fl_30_34)


    # Calculate by Age distribution
    workbook_age_01 = xlrd.open_workbook('/Users/Harshit/LECTURES/295B/Code/Master-Project/code/AGE01.xls')
    worksheet_age_01_sheet7 = workbook_age_01.sheet_by_name('Sheet7')
    worksheet_age_01_sheet9 = workbook_age_01.sheet_by_name('Sheet9')
    census_california_10_14 = (worksheet_age_01_sheet7.cell(192, 31).value);
    census_california_15_19 = (worksheet_age_01_sheet9.cell(192, 3).value);
    census_california_20_24 = (worksheet_age_02_sheet3.cell(192, 35).value);


    #census_california_25_29 = (worksheet.cell(192, 31).value);


    #p_ca_drug_addict = cal_count / census_california
    p_ca_12_14_da = cal_count_12_14 / cal_count
    p_ca_15_17_da = cal_count_15_17 / cal_count
    p_ca_18_20_da = cal_count_18_20 / cal_count
    p_ca_21_24_da = cal_count_21_24 / cal_count

    print(cal_count_12_14)
    print(cal_count_15_17)
    print(cal_count_18_20)
    print(cal_count_21_24)
    print(cal_count_25_29)

    p_ca_10_14 = census_california_10_14 / census_california
    p_ca_15_19 = census_california_15_19 / census_california
    p_ca_20_24 = census_california_20_24 / census_california

    print(census_california_10_14)
    print(census_california_15_19)
    print(census_california_20_24)
    print(census_california_25_29)

    drugAllAge=[]
    censusAllAge = []



    # p_da_ca_12=p_ca_drug_addict*(p_ca_12_14_da/3)/(p_ca_10_14/5)
    # p_da_ca_13 = p_ca_drug_addict * (p_ca_12_14_da / 3) / (p_ca_10_14 / 5)
    # p_da_ca_14 = p_ca_drug_addict * (p_ca_12_14_da / 3) / (p_ca_10_14 / 5)
    # p_da_ca_15 = p_ca_drug_addict * (p_ca_15_17_da / 3) / (p_ca_15_19 / 5)
    # p_da_ca_16 = p_ca_drug_addict * (p_ca_15_17_da / 3) / (p_ca_15_19 / 5)
    # p_da_ca_17 = p_ca_drug_addict * (p_ca_15_17_da / 3) / (p_ca_15_19 / 5)
    # p_da_ca_18 = p_ca_drug_addict * (p_ca_18_20_da / 3) / (p_ca_15_19 / 5)
    # p_da_ca_19 = p_ca_drug_addict * (p_ca_18_20_da / 3) / (p_ca_15_19 / 5)
    # p_da_ca_20 = p_ca_drug_addict * (p_ca_18_20_da / 3) / (p_ca_20_24 / 5)
    # p_da_ca_21 = p_ca_drug_addict * (p_ca_21_24_da / 4) / (p_ca_20_24 / 5)
    # p_da_ca_22 = p_ca_drug_addict * (p_ca_21_24_da / 4) / (p_ca_20_24 / 5)
    # p_da_ca_23 = p_ca_drug_addict * (p_ca_21_24_da / 4) / (p_ca_20_24 / 5)
    # p_da_ca_24 = p_ca_drug_addict * (p_ca_21_24_da / 4) / (p_ca_20_24 / 5)

    return json.dumps(data);

def userSexData(drugColVal, censusColVal):
    drug_male = 0.0
    drug_female = 0.0

    with open('/Users/Harshit/LECTURES/295B/Code/Master-Project/code/35074-0001-Data.tsv', 'r') as tsvin:
        tsvin = csv.reader(tsvin, delimiter='\t')
        for row in tsvin:
            if row[15] == str(drugColVal):
                if row[3] == '1':
                    drug_male = drug_male + 1
                if row[3] == '2':
                    drug_female = drug_female + 1


    workbook_sex = xlrd.open_workbook('/Users/Harshit/LECTURES/295B/Code/Master-Project/code/SEX01.xls')
    worksheet_sex_1 = workbook_sex.sheet_by_name('Sheet1')
    census_sex_male = worksheet_sex_1.cell(censusColVal, 7).value

    worksheet_sex_2 = workbook_sex.sheet_by_name('Sheet2')
    census_sex_female = worksheet_sex_2.cell(censusColVal, 19).value

    sex_data = [
        {
        "male": {
            "census_count": census_sex_male,
            "drug_count": drug_male
        },
        "female": {
            "census_count": census_sex_female,
            "drug_count": drug_female
        }
    }
        ]
    return sex_data


def insertProbabilityToDatabase(stateCensusTotalPopulation = [],state='',age_state_census={} ,sex={},race={}, *args):
   # p_drug_addict = stateCensusTotalPopulation[0] / stateCensusTotalPopulation[1];
   probability=[];
   k=0; Querries=[];
   if (bool(age_state_census)):
       probability=calculateProbabilty(age_state_census, stateCensusTotalPopulation);
       for items in probability:
           Querries[k] = Age(age=items[0], age_probability=items[2], age_drug_probability=items[1], state=state);
           k=k+1;

   if (bool(sex)):
       probability = calculateProbabilty(sex, stateCensusTotalPopulation);
       for items in probability:
           Querries[k] = Sex(age=items[0], age_probability=items[2], age_drug_probability=items[1], state=state);
           k = k + 1;


   if (bool(race)):
       probability = calculateProbabilty(sex, stateCensusTotalPopulation);
       for items in probability:
           Querries[k] = Race(age=items[0], age_probability=items[2], age_drug_probability=items[1], state=state);
           k = k + 1;

   for querry in Querries:
       db.session.add(querry)
   db.session.commit()


def calculateProbabilty(values={},stateCensusTotalPopulation=[]):
    w=3; h=len(values); i=0;
    Matrix = [[0 for x in range(w)] for y in range(h)]
    for k, v in values.items():
        p_drug = v["drug_count"] / stateCensusTotalPopulation[0];
        p = v["census_count"] / stateCensusTotalPopulation[1];
        Matrix[i]=[k,p_drug,p];
        i=i+1;

    return Matrix


def getProbabiltyfromDatabase(personData={},State='',*args):
    p_drug_addict=123;
    finalProbability = p_drug_addict;

    for features, values in personData.items():
        p_drug="abc";
        p="abc";
        finalProbability=finalProbability * (p_drug/p);

    return finalProbability


@app.route('/dd1')
def insertUserAgeData():
    drug_column = '6'
    census_state_column=192


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
    with open('/Users/Harshit/LECTURES/295B/Code/Master-Project/code/35074-0001-Data.tsv', 'r') as tsvin:
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


    ##########Drug Data End

    workbook_age_01 = xlrd.open_workbook('/Users/Harshit/LECTURES/295B/Code/Master-Project/code/AGE01.xls')
    worksheet_age_01_sheet7 = workbook_age_01.sheet_by_name('Sheet7')
    worksheet_age_01_sheet9 = workbook_age_01.sheet_by_name('Sheet9')
    census_10_14 = (worksheet_age_01_sheet7.cell(census_state_column, 31).value);
    census_15_19 = (worksheet_age_01_sheet9.cell(census_state_column, 3).value);

    workbook_age_02 = xlrd.open_workbook('/Users/Harshit/LECTURES/295B/Code/Master-Project/code/AGE02.xls')
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

    workbook_age_03 = xlrd.open_workbook('/Users/Harshit/LECTURES/295B/Code/Master-Project/code/AGE03.xls')
    worksheet_age_03_sheet1 = workbook_age_03.sheet_by_name('Sheet1')
    worksheet_age_03_sheet3 = workbook_age_03.sheet_by_name('Sheet3')
    worksheet_age_03_sheet5 = workbook_age_03.sheet_by_name('Sheet5')
    census_45_49 = (worksheet_age_03_sheet1.cell(census_state_column, 35).value)
    census_50_54 = (worksheet_age_03_sheet3.cell(census_state_column, 31).value)
    census_55_59 = (worksheet_age_03_sheet5.cell(census_state_column, 11).value)

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
    age_data["55+"] = {"census_data": census_55_59  , "drug_data": drug_count_55_100}

    print(age_data)

    return json.dumps(age_data);




@app.route('/index')
def charts(chartID = 'chart_ID', chart_type = 'bar', chart_height = 550):
	chart = {"renderTo": chartID, "type": chart_type, "height": chart_height,}
	series = [{"name": 'Alcohol', "data": [25]}, {"name": 'Marijuana', "data": [30]}, {"name": 'Cocaine', "data": [56]}]
	title = {"text": 'Substance Abuse Predictions'}
	xAxis = {"categories": ['Substances']}
	yAxis = {"title": {"text": 'Probability'}}
	return render_template('charts.html', chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis, yAxis=yAxis)




if __name__ == '__main__':
    app.run(port=5003);
