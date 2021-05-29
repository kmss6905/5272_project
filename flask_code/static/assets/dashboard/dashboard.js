/* globals Chart:false, feather:false */

(function () {
  // Graphs
  var ctx = document.getElementById('myChart')
  var ctx2 = document.getElementById('myChart2')
  var ctx3 = document.getElementById('myChart3')
  // eslint-disable-next-line no-unused-vars
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
        display: false
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
        display: false
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
        display: false
      }
    }
  }) 
})()
