var mapContainer = document.getElementById('map'), // 지도를 표시할 div
    mapCenter = new kakao.maps.LatLng(37.560639431238144, 126.9935758934571), // 지도의 중심 좌표
    mapOption = {
        center: mapCenter, // 지도의 중심 좌표
        level: 1 // 지도의 확대 레벨
    };

// 지도를 표시할 div와  지도 옵션으로  지도를 생성합니다
var map = new kakao.maps.Map(mapContainer, mapOption);

var myPosition = new kakao.maps.LatLng(37.560639431238144, 126.9935758934571);

// 지도에 올릴 마커를 생성합니다.
var mMarker = new kakao.maps.Marker({
    position: myPosition, // 지도의 중심좌표에 올립니다.
    map: map // 생성하면서 지도에 올립니다.
});

// 지도에 올릴 장소명 인포윈도우 입니다.
var mLabel = new kakao.maps.InfoWindow({
    position: myPosition, // 지도의 중심좌표에 올립니다.
    content: "syntest1" // 인포윈도우 내부에 들어갈 컨텐츠 입니다.
});
mLabel.open(map, mMarker); // 지도에 올리면서, 두번째 인자로 들어간 마커 위에 올라가도록 설정합니다.

var rvContainer = document.getElementById('roadview'); // 로드뷰를 표시할 div

var rv = new kakao.maps.Roadview(rvContainer); // 로드뷰 객체 생성
var rc = new kakao.maps.RoadviewClient(); // 좌표를 통한 로드뷰의 panoid를 추출하기 위한 로드뷰 help객체 생성
var rvPosition = new kakao.maps.LatLng(37.560639431238144, 126.9935758934571);

rc.getNearestPanoId(rvPosition, 50, function(panoid) {
    rv.setPanoId(panoid, rvPosition);//좌표에 근접한 panoId를 통해 로드뷰를 실행합니다.
});

// 로드뷰 초기화 이벤트
kakao.maps.event.addListener(rv, 'init', function() {

    // 로드뷰에 올릴 마커를 생성합니다.
    var rMarker = new kakao.maps.Marker({
        position: myPosition,
        map: rv //map 대신 rv(로드뷰 객체)로 설정하면 로드뷰에 올라갑니다.
    });
    rMarker.setAltitude(10); //마커의 높이를 설정합니다. (단위는 m입니다.)
    rMarker.setRange(100); //마커가 보일 수 있는 범위를 설정합니다. (단위는 m입니다.)

    // 로드뷰에 올릴 장소명 인포윈도우를 생성합니다.
    var rLabel = new kakao.maps.InfoWindow({
        content: "syntest1"
    });
    rLabel.setRange(100); //마커가 보일 수 있는 범위를 설정합니다. (단위는 m입니다.)
    rLabel.open(rv, rMarker); // open시 마커를 넣어주면, 마커의 altitude와 position값을 모두 따라 갑니다.

    // 로드뷰 마커가 중앙에 오도록 로드뷰의 viewpoint 조정합니다.
    var projection = rv.getProjection(); // viewpoint(화면좌표)값을 추출할 수 있는 projection 객체를 가져옵니다.

    // 마커의 position과 altitude값을 통해 viewpoint값(화면좌표)를 추출합니다.
    var viewpoint = projection.viewpointFromCoords(rMarker.getPosition(), rMarker.getAltitude());
    rv.setViewpoint(viewpoint); //로드뷰에 뷰포인트를 설정합니다.
});