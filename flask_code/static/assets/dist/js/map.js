var mapContainer = document.getElementById('map'), // 지도를 표시할 div  
    mapOption = { 
        center: new kakao.maps.LatLng(37.560806, 126.993644), // 지도의 중심좌표
        level: 40// 지도의 확대 레벨
    };

var map = new kakao.maps.Map(mapContainer, mapOption); // 지도를 생성합니다
// 마커를 표시할 위치와 내용을 가지고 있는 객체 배열입니다 
var positions = [
    {
        content: '<div>충무로_syn</div>', 
        latlng: new kakao.maps.LatLng(37.560806, 126.993644)
    },
    {
        content: '<div>울산_2214</div>', 
        latlng: new kakao.maps.LatLng(35.309242397, 129.267961838)
    },
    {
        content: '<div>울산_2221</div>', 
        latlng: new kakao.maps.LatLng(35.30924818, 129.267935811)
    },
    {
        content: '<div>울산_2222</div>',
        latlng: new kakao.maps.LatLng(35.309250849, 129.267948917)
    },
    {
        content: '<div>울산_2223</div>',
        latlng: new kakao.maps.LatLng(35.30925499, 129.267942501)
    },
    {
        content: '<div>울산_2224</div>',
        latlng: new kakao.maps.LatLng(35.309222979, 129.267974469)
    }
];

for (var i = 0; i < positions.length; i ++) {
    // 마커를 생성합니다
    var marker = new kakao.maps.Marker({
        map: map, // 마커를 표시할 지도
        position: positions[i].latlng // 마커의 위치
    });

    // 마커에 표시할 인포윈도우를 생성합니다 
    var infowindow = new kakao.maps.InfoWindow({
        content: positions[i].content // 인포윈도우에 표시할 내용
    });

    // 마커에 mouseover 이벤트와 mouseout 이벤트를 등록합니다
    // 이벤트 리스너로는 클로저를 만들어 등록합니다 
    // for문에서 클로저를 만들어 주지 않으면 마지막 마커에만 이벤트가 등록됩니다
    kakao.maps.event.addListener(marker, 'mouseover', makeOverListener(map, marker, infowindow));
    kakao.maps.event.addListener(marker, 'mouseout', makeOutListener(infowindow));
}

// 인포윈도우를 표시하는 클로저를 만드는 함수입니다 
function makeOverListener(map, marker, infowindow) {
    return function() {
        infowindow.open(map, marker);
    };
}

// 인포윈도우를 닫는 클로저를 만드는 함수입니다 
function makeOutListener(infowindow) {
    return function() {
        infowindow.close();
    };
}