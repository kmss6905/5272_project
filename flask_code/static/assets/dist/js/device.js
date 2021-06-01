/**
 *
 * @param data(list)
 * @param elementName
 */
function render_plot(data, elementName, title, xAxisName, yAxisName, min, max, absValue){
    data.reverse();  // 순서변경

    // if(calculateFlag == 1){ // 여기가 동작을 안함.. 0.01을 곱한 결과값으로 바뀌지 않는다..
    //       // * 10
    //     for (let i = 0; i <data.length; i++) {
    //         data[i]['low'] = data[i]['low'] * 0.01
    //         data[i]['high'] = data[i]['high'] * 0.01
    //         data[i]['q1'] = data[i]['q1'] * 0.01
    //         data[i]['q3'] = data[i]['q3'] * 0.01
    //         data[i]['median'] = data[i]['median'] * 0.01
    //     }
    // }


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

    // // show information when mouse is over a marker
    // chart.listen("mouseOver", function (e) {
    //     // var symbol = e.eventMarker.symbol;
    //     // var description = e.eventMarker.description;
    //     // var date = e.eventMarker.date;
    //     console.log(e)
    //     document.getElementById('information-lat').innerHTML = "heel";
    //
    //     // hide information when mouse leaves a marker
    //     // chart.listen("eventMarkerMouseOut", function () {
    //     //     document.getElementById(elementName).innerHTML = "";
    //     // });
    //     //
    //     // // open a url when a marker is clicked on
    //     // chart.listen("eventMarkerClick", function (e) {
    //     //     var url = "https://www.google.ru/search?q=" +
    //     //         e.eventMarker.description;
    //     //     window.open(url, "_blank");
    //     // });
    // })
}





