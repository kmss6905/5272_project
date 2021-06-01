/* globals Chart:false, feather:false */

(function () {
  // Graphs
  var ctx = document.getElementById('myChart')
  var ctx2 = document.getElementById('myChart2')
  var ctx3 = document.getElementById('myChart3')
  var myChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: [
        '08:00:05',
        '08:00:06',
        '08:00:07',
        '08:00:08',
        '08:00:09',
        '08:00:10',
        '08:00:11'
      ],
      datasets: [{
        label: '실시간 위도 데이터',
        data: [
          3733.6462962,
          3733.6462786,
          3733.6462745,
          3733.6462574,
          3733.6462469,
          3733.6462478,
          3733.6462478
        ],
        lineTension: 0,
        backgroundColor: 'transparent',
        borderColor: '#007bff',
        borderWidth: 4,
        pointBackgroundColor: '#007bff'
      }]
    },
    options: {
      scales: {
        yAxes: [{
          ticks: {
            beginAtZero: false
          }
        }]
      },
      legend: {
        position: 'left'
      }
    }
  })

  var myChart2 = new Chart(ctx2, {
    type: 'line',
    data: {
      labels: [
        '08:00:05',
        '08:00:06',
        '08:00:07',
        '08:00:08',
        '08:00:09',
        '08:00:10',
        '08:00:11'
      ],
      datasets: [{
        label: '실시간 경도 데이터',
        data: [
          15339,
          21345,
          18483,
          24003,
          23489,
          24092,
          12034
        ],
        lineTension: 0,
        backgroundColor: 'transparent',
        borderColor: '#007bff',
        borderWidth: 4,
        pointBackgroundColor: '#007bff'
      }]
    },
    options: {
      scales: {
        yAxes: [{
          align: 'center',
          title: "위도",
          ticks: {
            beginAtZero: false
          },
          display: true
        }],
        xAxis: [{
          align: 'center',
          title: "시각",
          ticks: {
            beginAtZero: false
          },
          display: true
        }]
      },
      legend: {
        position: 'left'
      }
    }
  })

  var myChart4 = new Chart(ctx3, {
    type: 'line',
    data: {
      labels: [
        '08:00:05',
        '08:00:06',
        '08:00:07',
        '08:00:08',
        '08:00:09',
        '08:00:10',
        '08:00:11'
      ],
      datasets: [{
        label: '실시간 고도 데이터',
        data: [
          15339,
          21345,
          18483,
          24003,
          23489,
          24092,
          12034
        ],
        lineTension: 0,
        backgroundColor: 'transparent',
        borderColor: '#007bff',
        borderWidth: 4,
        pointBackgroundColor: '#007bff'
      }]
    },
    options: {
      scales: {
        yAxes: [{
          ticks: {
            beginAtZero: false
          }
        }]
      },
      legend: {
        position: 'left'
      }
    }
  })
})()

// if (document.readyState === 'complete'){
//   // renderLineGraph('myChart3', " ", "실시간 경도 그래프")
// }

function renderLineGraph(id, data, datesetLabel){
  var canvas = document.getElementById(id)
  var ctx3 = canvas.getContext("2d")
  var horizonalLinePlugin = {
  afterDraw: function(chartInstance) {
    var yScale = chartInstance.scales["y-axis-0"];
    var canvas = chartInstance.chart;
    var ctx = canvas.ctx;
    var index;
    var line;
    var style;
    if (chartInstance.options.horizontalLine) {
      for (index = 0; index < chartInstance.options.horizontalLine.length; index++) {
        line = chartInstance.options.horizontalLine[index];
        if (!line.style) {
          style = "rgba(169,169,169, .6)";
        } else {
          style = line.style;
        }
        if (line.y) {
          yValue = yScale.getPixelForValue(line.y);
        } else {
          yValue = 0;
        }
        ctx.lineWidth = 3;
        if (yValue) {
          ctx.beginPath();
          ctx.moveTo(0, yValue);
          ctx.lineTo(canvas.width, yValue);
          ctx.strokeStyle = style;
          ctx.stroke();
        }
        if (line.text) {
          ctx.fillStyle = style;
          ctx.fillText(line.text, 0, yValue + ctx.lineWidth);
        }
      }
      return;
    };
    }
  };
  Chart.pluginService.register(horizonalLinePlugin);


  var chart3 = new Chart(ctx3, {
    type: 'line',
    data: {
      labels: [
        '08:00:05',
        '08:00:06',
        '08:00:07',
        '08:00:08',
        '08:00:09',
        '08:00:10',
        '08:00:11'
      ],
      datasets: [{
        data: [
          3733.6462962,
          3733.6462786,
          3733.6462745,
          3733.6462574,
          3733.6462469,
          3733.6462478,
          3733.6462478
        ],
        lineTension: 0,
        backgroundColor: 'transparent',
        borderColor: '#007bff',
        borderWidth: 4,
        pointBackgroundColor: '#007bff'
      }]
    },
    options: {
      "horizontalLine": [{
      "y": 2000,
      "style": "rgba(255, 0, 0, .4)",
      "text": "max"
    }, {
      "y": 2000,
      "style": "#00ffff",
    }, {
      "y": 2000,
      "text": "min"
    }],
      scales: {
        yAxes: [{
          ticks: {
            beginAtZero: false
          }
        }]
      },
      legend: {
        display: false
      }
    }
  })
}

/**
 *
 * @param chart char 객체
 * @param label label ( 여기서는 1초마다 )
 * @param data (경도 / 위도 / 고도 )
 */
function addData(chart, label, data) {
    chart.data.labels.push(label);
    chart.data.datasets.forEach((dataset) => {
        dataset.data.push(data);
    });
    chart.update();
}

function renderHorizontalLine(){

}