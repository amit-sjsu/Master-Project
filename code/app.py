from flask import Flask, send_file, render_template
import xlrd
import csv
import json


app = Flask(__name__)

@app.route("/")
def index():
    return send_file("templates/index.html")

@app.route('/dd')
def userAgeData():
    workbook = xlrd.open_workbook('/Users/anshul/Documents/LinkedIn Profile/AGE/AGE02.xls')
    worksheet = workbook.sheet_by_name('Sheet5')
    worksheet1 = workbook.sheet_by_name('Sheet7')
    census_albama_25_29 = worksheet.cell(2, 15).value
    census_california_25_29 = worksheet.cell(192, 15).value
    census_florida_25_29 = worksheet.cell(331, 15).value
    census_new_york_25_29 = worksheet.cell(1863, 15).value
    census_albama_30_34 = worksheet1.cell(2, 11).value
    census_california_30_34 = worksheet1.cell(192, 11).value
    census_florida_30_34 = worksheet1.cell(331, 11).value
    census_new_york_30_34 = worksheet1.cell(1863, 11).value
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

    with open('/Users/anshul/Documents/CMPE295A/ICPSR_35074/DS0001/35074-0001-Data.tsv', 'r') as tsvin:
        tsvin = csv.reader(tsvin, delimiter='\t')
        for row in tsvin:
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


    workbook1 = xlrd.open_workbook('/Users/anshul/Documents/LinkedIn Profile/AGE/AGE01.xls')
    worksheet2 = workbook1.sheet_by_name('Sheet1')
    census_albama = worksheet2.cell(2, 15).value
    census_california = worksheet2.cell(192, 15).value
    census_florida = worksheet2.cell(331, 15).value
    census_new_york = worksheet2.cell(1863, 15).value

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





    print(p_da_ca_25_29)
    print(p_da_ca_30_34)
    print(p_da_al_25_29)
    print(p_da_al_30_34)
    print(p_da_ny_25_29)
    print(p_da_ny_30_34)
    print(p_da_fl_25_29)
    print(p_da_fl_30_34)

    return json.dumps(data);




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
