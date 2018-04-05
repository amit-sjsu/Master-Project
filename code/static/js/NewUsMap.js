

    var data ;

       $.ajax({
            url: '/getUsData',
            type: 'GET',
            success: function(response) {

              data=response.state_data;
               // Initiate the chart
           var chart = new Highcharts.mapChart('countryContainer', {

                chart: {
                        type: 'map',

                    },
                title : {
                    text : 'Substance abuse Analytics'
                },

                subtitle : {
                    text : 'United States of America'
                },

                mapNavigation: {
                    enabled: true,
                    buttonOptions: {
                        verticalAlign: 'bottom'
                    }
                },

                colorAxis: {
                  min: 0,
                  minColor: '#E6E7E8',
                  maxColor: '#005645'
                    },
                plotOptions: {
                  map: {
                    states: {
                      hover: {
                        color: '#EEDD66'
                      }
                    }
                  },
                   series:{
                        point:{
                            events:{
                                click: function(e){
                                    if(e.point.name!==null){
                                        pushToSide(e.point.name.toUpperCase());
                                    }

                                }
                            }
                        }
                    }
                },

                series : [{
                    cursor:'pointer',
                    data : data,
                    mapData: Highcharts.maps['countries/us/us-all'],
                    joinBy: 'hc-key',
                    name: 'USA',
                    states: {
                        hover: {
                            color: '#EEDD66'
                        }
                    },
                    dataLabels: {
                        enabled: true,
                        format: '{point.properties.postal-code}'
                    },
                }, {
                    name: 'Separators',
                    type: 'mapline',
                    data: Highcharts.geojson(Highcharts.maps['countries/us/us-all'], 'mapline'),
                    color: 'silver',
                    showInLegend: false,
                    enableMouseTracking: false
                }],

                tooltip: {
                backgroundColor: 'white'
            },


            });



                    },
                    error: function(error) {
                        console.log(error);
                    }
             });



