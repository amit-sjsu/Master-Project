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

    print(census_albama_25_29)
    print(census_california_25_29)
    print(census_florida_25_29)
    print(census_new_york_25_29)
    print(cal_count_25_29)
    print(albama_count_25_29)
    print(fl_count_25_29)
    print(ny_count_25_29)
    data={}
    data["CA"]=[{"age_25_29":{"census_data":census_california_25_29, "drug_data":cal_count_25_29}},
                {"age_30_34":{"census_data":census_california_30_34, "drug_data":cal_count_30_34}}]

    data["AL"] = [{"age_25_29": {"census_data": census_albama_25_29, "drug_data": albama_count_25_29}},
                  {"age_30_34": {"census_data": census_albama_30_34, "drug_data": albama_count_30_34}}]

    data["FL"] = [{"age_25_29": {"census_data": census_florida_25_29, "drug_data": fl_count_25_29}},
                  {"age_30_34": {"census_data": census_florida_30_34, "drug_data": fl_count_30_34}}]

    data["NY"] = [{"age_25_29": {"census_data": census_new_york_25_29, "drug_data": ny_count_25_29}},
                  {"age_30_34": {"census_data": census_new_york_30_34, "drug_data": ny_count_30_34}}]

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
    userAgeData()
    app.run(port=5003);