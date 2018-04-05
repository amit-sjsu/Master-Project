function age(data){


var data = data;

json = [];

all_keys = Object.keys(data);
all_values = Object.values(data);
for (var i = 0; i<all_keys.length; i++) {
    json[i] = {
        "name": all_keys[i],
        "y": all_values[i]
    };
}

var chartAge = new Highcharts.chart('Age', {
    chart: {
        type: 'column'
        // events:{
        //       render: function (e) {
        //         setTimeout(function(){ resizeChart(0); }, 3000);
        //     }
        // }
    },
    title: {
        text: 'Probability '
    },
    subtitle: {
        text: 'Source: WorldClimate.com'
    },
    xAxis: {
        type: 'category',
        crosshair: true
    },
    yAxis: {
        title: {
            text: 'Probability'
        }
    },
    plotOptions: {
        series: {
            borderWidth: 0,
            dataLabels: {
                enabled: true,
                format: '{point.y:.1f}%'
            }
        }
    },

    tooltip: {
        headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
        pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y:.2f}%</b> of total<br/>'
    },

    "series": [
        {
            "name": "Age",
            "colorByPoint": true,
            "data": json
        }
    ]
});
}
