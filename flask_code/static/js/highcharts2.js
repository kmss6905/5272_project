var chart;
var line_chart;

/**
 * Request data from the server, add it to the graph and set a timeout
 * to request again
 */
function requestData() {
    $.ajax({
        url: '/live-data',
        success: function(point) {
            var series = chart.series[0],
                shift = series.data.length > 30; // 그래프에 풀로 채워지면 30초

            // add the point
            chart.series[0].addPoint(point, true, shift);
        },
        cache: false  //
    });
}

function requestAverageDate() {
    $.ajax({
        url: '/info',
        data: {
            "start": "2021-4-29",
            "end": "2021-4-29",
            "device_name": "ulsan1"
        },
        type: "GET",
        success: function(data) {
            console.log(data)
        },
        cache: false  //
    });
}

$(document).ready(function() {
    chart = new Highcharts.Chart({
        chart: {
            renderTo: 'data-container',
            defaultSeriesType: 'spline'
        },
        title: {
            text: 'Live Latitude Data'
        },
        xAxis: {
            type: 'datetime',
            tickPixelInterval: 150,
            maxZoom: 20 * 1000
        },
        yAxis: {
            minPadding: 0.2,
            maxPadding: 0.2,
            title: {
                text: 'Value',
                margin: 80
            }
        },
        series: [{
            name: 'Latitude data',
            data: []
        }]
    });
    // call it again after one second
    setInterval(requestData,1000);
});

$(document).ready(function () {
    Highcharts.chart('line-container', {
        title: {
            text: 'Solar Employment Growth by Sector, 2010-2016'
        },

        subtitle: {
            text: 'Source: thesolarfoundation.com'
        },

        yAxis: {
            title: {
                text: 'value'
            }
        },

        xAxis: {
            accessibility: {
                rangeDescription: 'Range: 2010 to 2017'
            }
        },

        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle'
        },

        plotOptions: {
            series: {
                label: {
                    connectorAllowed: false
                },
                pointStart: 2021
            }
        },

        series: [{
            name: '위도',
            data: [43934, 52503, 57177, 69658, 97031, 119931, 137133, 154175]
        }, {
            name: '고도',
            data: [24916, 24064, 29742, 29851, 32490, 30282, 38121, 40434]
        }, {
            name: '경도',
            data: [11744, 17722, 16005, 19771, 20185, 24377, 32147, 39387]
        }],

        responsive: {
            rules: [{
                condition: {
                    maxWidth: 500
                },
                chartOptions: {
                    legend: {
                        layout: 'horizontal',
                        align: 'center',
                        verticalAlign: 'bottom'
                    }
                }
            }]
        }

    });

    requestAverageDate()
});




