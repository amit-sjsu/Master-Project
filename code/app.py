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

    workbook = xlrd.open_workbook('/Users/Harshit/LECTURES/295B/Code/Master-Project/code/AGE02.xls')

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

    with open('/Users/Harshit/LECTURES/295B/Code/Master-Project/code/35074-0001-Data.tsv', 'r') as tsvin:

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


    workbook1 = xlrd.open_workbook('/Users/Harshit/LECTURES/295B/Code/Master-Project/code/AGE01.xls')
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


    data = [
         {'CA': [{'P_DrugAddict': 123},
                {'P_DA_Age_25_29': 123,
                'P_DA_Age_30_34': 123}
           ]
          },
         {'AL': [{'P_DrugAddict': 223},
                {'P_DA_Age_25_29': 223,
                'P_DA_Age_30_34': 223}
           ]
         },
        {'NY': [{'P_DrugAddict': 323},
                {'P_DA_Age_25_29': 323,
                'P_DA_Age_30_34': 323}
           ]
         },
        {'FL': [{'P_DrugAddict': 423},
                {'P_DA_Age_25_29': 423,
                'P_DA_Age_30_34': 423}
           ]
         }
    ];

    return data;





@app.route('/index')
def charts(chartID = 'chart_ID', chart_type = 'bar', chart_height = 550):
	chart = {"renderTo": chartID, "type": chart_type, "height": chart_height,}
	series = [{"name": 'Alcohol', "data": [25]}, {"name": 'Marijuana', "data": [30]}, {"name": 'Cocaine', "data": [56]}]
	title = {"text": 'Substance Abuse Predictions'}
	xAxis = {"categories": ['Substances']}
	yAxis = {"title": {"text": 'Probability'}}
	return render_template('charts.html', chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis, yAxis=yAxis)



@app.route('/addictionProbability',methods=['GET'])
def getAddictionProbability():
    data = userAgeData();
    print (data);
    return render_template('analysis.html', result=data);



if __name__ == '__main__':
    app.run(port=5003);