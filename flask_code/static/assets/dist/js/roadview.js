var mapContainer = document.getElementById('map'), // 지도를 표시할 div
    mapCenter = new kakao.maps.LatLng(37.56066207135651, 126.99358785285912), // 지도의 중심 좌표
    mapOption = {
        center: mapCenter, // 지도의 중심 좌표
        level: 1 // 지도의 확대 레벨
    };

// 지도를 표시할 div와  지도 옵션으로  지도를 생성합니다
var map = new kakao.maps.Map(mapContainer, mapOption);

var positions = [

    {
        content: '<div>22013</div>',  //마크 위에 표시될 정보내용 (이건 울산_2214 계측기)
        latlng: new kakao.maps.LatLng(37.56066207135651, 126.99358785285912)
    }
// 지도에 올릴 마커를 생성합니다.
var mMarker = new kakao.maps.Marker({
    position: positions[i].latlng , // 지도의 중심좌표에 올립니다.
    map: map // 생성하면서 지도에 올립니다.
});

// 지도에 올릴 장소명 인포윈도우 입니다.
var mLabel = new kakao.maps.InfoWindow({
    position: positions[i].latlng, // 지도의 중심좌표에 올립니다.
    content: '22013' // 인포윈도우 내부에 들어갈 컨텐츠 입니다.
});
mLabel.open(map, mMarker); // 지도에 올리면서, 두번째 인자로 들어간 마커 위에 올라가도록 설정합니다.


var rvContainer = document.getElementById('roadview'); // 로드뷰를 표시할 div
var rv = new kakao.maps.Roadview(rvContainer); // 로드뷰 객체 생성
var rc = new kakao.maps.RoadviewClient(); // 좌표를 통한 로드뷰의 panoid를 추출하기 위한 로드뷰 help객체 생성
var rvResetValue = {} //로드뷰의 초기화 값을 저장할 변수
rc.getNearestPanoId(positions, 50, function(panoId) {
    rv.setPanoId(panoId, mapCenter);//좌표에 근접한 panoId를 통해 로드뷰를 실행합니다.
    rvResetValue.panoId = panoId;
});

// 로드뷰 초기화 이벤트
kakao.maps.event.addListener(rv, 'init', function() {

    // 로드뷰에 올릴 마커를 생성합니다.
    var rMarker = new kakao.maps.Marker({
        position: positions[i].latlng,
        map: rv //map 대신 rv(로드뷰 객체)로 설정하면 로드뷰에 올라갑니다.
    });

    // 로드뷰에 올릴 장소명 인포윈도우를 생성합니다.
    var rLabel = new kakao.maps.InfoWindow({
        position: positions[i].latlng,
        content: '22013'
    });
    rLabel.open(rv, rMarker);

    // 로드뷰 마커가 중앙에 오도록 로드뷰의 viewpoint 조정 합니다.
    var projection = rv.getProjection(); // viewpoint(화면좌표)값을 추출할 수 있는 projection 객체를 가져옵니다.

    // 마커의 position과 altitude값을 통해 viewpoint값(화면좌표)를 추출합니다.
    var viewpoint = projection.viewpointFromCoords(rMarker.getPosition(), rMarker.getAltitude());
    rv.setViewpoint(viewpoint); //로드뷰에 뷰포인트를 설정합니다.

    //각 뷰포인트 값을 초기화를 위해 저장해 놓습니다.
    rvResetValue.pan = viewpoint.pan;
    rvResetValue.tilt = viewpoint.tilt;
    rvResetValue.zoom = viewpoint.zoom;
});

//지도 이동 이벤트 핸들러
function moveKakaoMap(self){

    var center = map.getCenter(),
        lat = center.getLat(),
        lng = center.getLng();

    self.href = 'https://map.kakao.com/link/map/' + encodeURIComponent('22013') + ',' + lat + ',' + lng; //Kakao 지도로 보내는 링크
}

//지도 초기화 이벤트 핸들러
function resetKakaoMap(){
    map.setCenter(mapCenter); //지도를 초기화 했던 값으로 다시 셋팅합니다.
    map.setLevel(mapOption.level);
}

//로드뷰 이동 이벤트 핸들러
function moveKakaoRoadview(self){
    var panoId = rv.getPanoId(); //현 로드뷰의 panoId값을 가져옵니다.
    var viewpoint = rv.getViewpoint(); //현 로드뷰의 viewpoint(pan,tilt,zoom)값을 가져옵니다.
    self.href = 'https://map.kakao.com/?panoid='+panoId+'&pan='+viewpoint.pan+'&tilt='+viewpoint.tilt+'&zoom='+viewpoint.zoom; //Kakao 지도 로드뷰로 보내는 링크
}

//로드뷰 초기화 이벤트 핸들러
function resetRoadview(){
    //초기화를 위해 저장해둔 변수를 통해 로드뷰를 초기상태로 돌립니다.
    rv.setViewpoint({
        pan: rvResetValue.pan, tilt: rvResetValue.tilt, zoom: rvResetValue.zoom
    });
    rv.setPanoId(rvResetValue.panoId);
}
