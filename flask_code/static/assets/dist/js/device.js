let chartLat;
let chartLon;
let chartHeight;
const liveLatElement = document.getElementById('live_data_lat');
const resultLatElement = document.getElementById('live_data_lat_difference')
const liveLonElement = document.getElementById('live_data_lon');
const resultLonElement = document.getElementById('live_data_lon_difference')
const liveHeightElement = document.getElementById('live_data_height');
const resultHeightElement = document.getElementById('live_data_height_difference')

function sseStart(criteriaLat, criteriaLon, criteriaHeight){

    var source = new EventSource("/stream");
    source.onmessage = function(event) {
        var x = (new Date()).getTime() // current time

        if(chartLat != null && chartLon != null && chartHeight != null){
            console.log(event.data)
            _result_data = event.data.split('_')
            var time = event.data.split('_')[0]
            console.log(time)
            console.log(typeof time)
            var _result = time.split(' ')
            console.log(_result[1])
            var y = event.data.split('_')[1]
            // var series = chartLat.series[0], sheift = series.data.length > 20; // shift if the series is longer than 20


            chartLat.series[0].addPoint([x, parseFloat(y)]) // 위도

            chartLon.series[0].addPoint([x, parseFloat(y)]) // 경도 ( 수정해야함 )
            chartHeight.series[0].addPoint([x, parseFloat(y)]) // 고도 ( 수정해야함 )

            renderTableData(parseFloat(y), criteriaLat) // 위도

            renderTableData(parseFloat(y), criteriaLon) // 경도 ( 수정해야함 )
            renderTableData(parseFloat(y), criteriaHeight) // 고도 ( 수정해야함 )
        }
    };
}

// 테이블 데이터에 데이터를 렌더링 합니다.
function renderTableData(liveData, criteriaData, maxValue, minValue, value){
    if(value == 'lat'){ // 위도
        liveLatElement.innerText = liveData // 실시간 위도
        resultLatElement.innerText = String(parseFloat(liveData) - parseFloat(criteriaData));
        if(liveData > maxValue || liveData < minValue){ // 최대값보다 크거나 최소값 보다 작을 경우
            liveLatElement.style.color = "#FF0000"; // red color code
            resultLatElement.style.color = "#FF0000"; // red color code
            resultLatElement.innerText = resultLatElement.innerText + " (정상범위 초과)"
            window.alert("정상범위를 초과하는 데이터가 감지되었습니다. 확인바랍니다. [ 위도 ]");
        }
    }

    if(value == 'lon'){
        liveLonElement.innerText = liveData // 실시간 경도
        resultLonElement.innerText = String(parseFloat(liveData) - parseFloat(criteriaData));
        if(liveData > maxValue || liveData < minValue){ // 이상범위 밖
            liveLonElement.style.color = "#FF0000"; // red color code
            resultLonElement.style.color = "#FF0000"; // red color code
            resultLonElement.innerText = resultLonElement.innerText + " (정상범위 초과)"
            window.alert("정상범위를 초과하는 데이터가 감지되었습니다. 확인바랍니다. [ 경도 ]");
        }
    }

    if(value == 'height'){
        liveHeightElement.innerText = liveData // 실시간 고도
        resultHeightElement.innerText = String(parseFloat(liveData) - parseFloat(criteriaData));
        if(liveData > maxValue || liveData < minValue){ // 최대값보다 크거나 최소값 보다 작을 경우
            liveHeightElement.style.color = "#FF0000"; // red color code
            resultHeightElement.style.color = "#FF0000"; // red color code
            resultHeightElement.innerText = resultLatElement.innerText + " (정상범위 초과)"
            window.alert("정상범위를 초과하는 데이터가 감지되었습니다. 확인바랍니다. [ 고도 ]");
        }
    }
}

/**
 *
 * @param data(list)
 * @param elementName
 */
function render_plot(data, elementName, title, xAxisName, yAxisName, min, max, absValue){
    data.reverse();  // 순서변경

    //create area chart
    var chart = anychart.box(data);

    // create a plot on the chart

    // access the annotations() object of the plot to work with annotations
    var controller = chart.annotations();

    // 측정값 중 최대값
    var horizontalLineMax = controller.horizontalLine({
        valueAnchor: max,
        normal: {stroke: "3 #ff0000"},
        hovered: {stroke: "3 #ff0000"}
    });

    // 측정값 중 최소값
    var horizontalLineMin = controller.horizontalLine({
        valueAnchor: min,
        normal: {stroke: "3 #008000"},
        hovered: {stroke: "3 #008000"},
    });

    // 기준이 되는 값
    var horizontalLineAbs = controller.horizontalLine({
        valueAnchor: absValue,
        normal: {stroke: "3 #000000"},
        hovered: {stroke: "3 #000000"},
    });

    // 최대값 라벨
    var labelMax = controller.label({
         xAnchor: data[0]['x'], // 계측 최초 시간
         valueAnchor: max,
         fontSize: 15,
         fontFamily: "Courier",
         text: "최대" + "\n" + max,
         normal: {fontColor: "#800000", fontSize: 10},
         hovered: {fontColor: "#e60000", fontSize: 13},
         selected: {fontColor: "#e60000", fontSize: 13}
    });

    // 최소값 라벨
    var labelMin = controller.label({
         xAnchor: data[0]['x'], // 계측 최초 시간
         valueAnchor: min,
         fontSize: 15,
         fontFamily: "Courier",
         text: "최소 : " + min,
         normal: {fontColor: "#008000", fontSize: 10},
         hovered: {fontColor: "#00e600", fontSize: 13},
         selected: {fontColor: "#00e600", fontSize: 13}
    });

    // 기준값 라벨
    var labelAbs = controller.label({
         xAnchor: data[data.length-3]['x'], // 계측 최초 시간
         valueAnchor: absValue, // 기준값
         fontSize: 15,
         fontFamily: "Courier",
         text: "초기측정값 : " + absValue,
         normal: {fontColor: "#000000", fontSize: 10},
         hovered: {fontColor: "#000000", fontSize: 13},
         selected: {fontColor: "#000000", fontSize: 13}
    });


    chart.title(title)

    // label axis
    chart.xAxis().title(xAxisName + "\n" + data[0]['x'] + " - " + data[data.length-1]['x']);
    chart.yAxis().title(yAxisName);

    //turn on chart animation
    chart.animation(true);

    //set container id for the chart
    chart.container(elementName);

    //initiate chart drawing
    chart.draw();
}

function renderLineGraph(elementName, title, yAxis, minRate, maxRate, absRate, deviceName){
    // Create the chart
    if(yAxis=="위도"){
        chartLat = getStockChart(elementName, title, yAxis, minRate, maxRate, absRate, deviceName)
    } else if(yAxis=="경도"){
        chartLon = getStockChart(elementName, title, yAxis, minRate, maxRate, absRate, deviceName)
    }else if(yAxis=="고도"){
        chartHeight = getStockChart(elementName, title, yAxis, minRate, maxRate, absRate, deviceName)
    }
}

function getStockChart(elementName, title, yAxis, minRate, maxRate, absRate, deviceName) {
    return new Highcharts.stockChart(elementName, {
            title: {
                text: title
            },
            yAxis: {
                minColor: 'green',
                min: minRate,
                max: maxRate,
                title: {
                    text: yAxis
                },
                plotLines: [{
                   value: absRate,
                   color: 'black',
                   dashStyle: 'shortDash',
                   width: 2,
                   label: {
                       text: '초기 측정치'
                   }
                }],
                 plotBands: [{
                    from: minRate,
                    to: maxRate,
                    color: 'rgba(68, 170, 213, 0.2)',
                    label: {
                        text: '정상범위'
                    }
               }]},
            rangeSelector: {
            buttons: [{
              count: 1,
              type: 'minute',
              text: '1분'
            }, {
              count: 3,
              type: 'minute',
              text: '3분'
            }, {
              count: 5,
              type: 'minute',
              text: '5분'
            }, {
              type: 'all',
              text: '전체'
            }],
            inputEnabled: true,
            selected: 1
          }, series: [{
                name: yAxis,
                data: []
        }]
    });
}


