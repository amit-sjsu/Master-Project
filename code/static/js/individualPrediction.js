   function chartTest(alcholoProb){


       var gaugeOptions = {
    chart: {
        type: 'solidgauge'
        // renderTo: 'gaugeOptions',
    },
    title: "Your Drug Susceptibility",
    pane: {
        center: ['50%', '85%'],
        size: '150%',
        startAngle: -90,
        endAngle: 90,
        background: {
            backgroundColor: (Highcharts.theme && Highcharts.theme.background2) || '#EEE',
            innerRadius: '60%',
            outerRadius: '100%',
            shape: 'arc'
        }
    },
    tooltip: {
        enabled: false
    },
    // the value axis
    yAxis: {
        stops: [
            [0.1, '#FFC400'], // Orange to
            [0.2, '#FF9A00'], // red
            [0.3, '#FF7000'],
            [0.4, '#FF4500'],
            [0.5, '#FF3300'],
            [0.6, '#FF0033'],
            [0.7, '#FF0000'],
            [0.8, '#CC0033'],
            [0.9, '#CC0000'],
        ],
        lineWidth: 0,
        minorTickInterval: null,
        tickAmount: 2,
        title: {
            y: -70
        },
        labels: {
            y: 16
        }
    },
    plotOptions: {
        solidgauge: {
            dataLabels: {
                y: 5,
                borderWidth: 0,
                useHTML: true
            }
        }
    }
};
// The speed gauge
var raw_probability = alcholoProb
var probability_percentage = raw_probability * 100
var rounded = +(Math.round(probability_percentage + "e+2")  + "e-2")
var chartSpeed = new Highcharts.chart('container-speed', new Highcharts.merge(gaugeOptions, {
    yAxis: {
        min: 0,
        max: 24,
        title: {
            text: ''
        }
    },
    credits: {
        enabled: false
    },
    series: [{
        name: 'Drug Susceptibility',
        data: [rounded],
        dataLabels: {
            format: '<div style="text-align:center"><span style="font-size:25px;color:' +
                ((Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black') + '">{y}</span><br/>' +
                   '<span style="font-size:12px;color:silver">%</span></div>'
        },
        tooltip: {
            valueSuffix: ' %'
        }
    }]
}));


   }