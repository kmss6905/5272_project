## ssh 접속
* 구축한서버ip : 211.62.179.66
* hostname : synerex
* password : 시너렉스(영타)
* 유저 : synerex
* 접속 방법 : 
  * ssh synerex@211.62.179.66 입력

---
## 충무로 영상센터 ip/port
* tcp://211.62.179.65:10008

---
## 울산 현대중공업 데이터
* ip : 211.62.179.69
* port : 10004
* 총 4대 1hz 단위로
---
## MariaDB 접근
* mysql -u root -p 입력하고 비밀번호 입력하면 root계정으로  mariadb접속 할 수 있다
  
* db 시간대 서울로 설정 완료!
---
## 데이터베이스 테이블 설정
* 테이블은 계측기 울산인지 충무로인지에 따라 다르게 설계해야함...!
* 울산과 충무로 데이터 파싱이 달라야함!!
* create table rawdata_chung
  * -> (device_idx INT NOT NULL,device_id VARCHAR(30) NOT NULL,Create_time DATETIME NOT NULL, Latitude DOUBLE NOT NULL, Longitude DOUBLE NOT NULL,Height DOUBLE NOT NULL, Geoid_heigth DOUBLE NOT NULL);
  
* create table rawdata_ulsan
  * (device_idx INT NOT NULL,device_id INT NOT NULL,Create_time DATETIME NOT NULL, Latitude DOUBLE NOT NULL, Longitude DOUBLE NOT NULL,Height DOUBLE NOT NULL, Geoid_heigth DOUBLE NOT NULL);
  
* test 데이터베이스에 rawdata라는 테이블 생성
  * rawdata테이블은 계측기 데이터 원본 그대로 필요한것만 저장하기 위한 테이블 
---
## DB 용량 확인
> SELECT table_schema, sum(data_length) /1024/1024 AS mb FROM information_schema.tables GROUP BY table_schema ORDER BY sum(data_length+index_length) DESC;
* 계측기 총 5대에서 받아오는 데이터의 크기를 확인해보니 1일 30MB, 1달에 900MB, 1년에 10.8GB정도로 예상하고있습니다. (계측기 한대당 1년에 2GB정도)
---
## DB 특정 row 검색하기
* datetime 기준 
  * SELECT Create_time FROM rawdata_chung WHERE Create_time BETWEEN '2021-04-25 17:00:00' AND '2021-04-25 18:00:00';

---

## mariaDB 쿼리 성능
* 이제 mariaDB에 계측기 데이터 insert하는 것(chung.py / ulsan.py 파일로)은 쿼리가 단순하고 1초에 한번씩 db에 계측기 데이터 insert하는 것으로 성능에 큰 영향을 주지는 않지만....
* 이제 웹에서 4월10~4월27일까지의 계측기 데이터를 뽑아야하는 쿼리에서는 쿼리 성능이 중요해질 것으로 예상됨
* ===> 슬로우 쿼리 원인 분석(쿼리 추적툴이나 마리아 db에서 general_log활성화하면 슬로우 쿼리 추적 가능)들어가면 될듯...!! (추후 웹페이지 구축 다하면...)

* 성능 측정 툴인 percona TPCC, sysbench, apache JMeter, kakao MRTE등을 사용할 수 있다.
  * 성능테스트 ex) 1.메인페이지 동시접속 성능 테스트 2.검색 페이지 부하 테스트등등..
  * 1의 경우 페이지 내 모든 요청을 n개의 스레드를 만들어서 돌리고 요청 잘받는지 서버 이상없는지 확인// 주로 DB연결이 필요한 요청에서 성능 문제가 발생 // 모든 요청을 나눠서 어떤요청이 성능 저하 요인인지 판단..
  * <img src = >
---
## mariadb에 파이썬언어로 계측기 연결시켜 데이터 저장하기
* 먼저 pymysql 설치 완료
* mariadb의 test database생성 후 test db의 rawdata_chung이라는 테이블 생성
* 서버 디렉토리 /home/synerex/j로 이동하여 python3 a.py라고 치고 실행 시키면 계속 데이터가 db에 저장됨
* db저장되는거 확인할려면 ssh 접속후 mysql -u root -p 입력 시너렉스(영문)비밀번호 입력 use test; 입력 select * from rawdata_chung; 입력 이러면 데이터 쌓인거 확인 가능 

---
# ssh 연결 유지하는 방법
* python3 파일명.py 2>&1 & 치면 백그라운드에서 실행이됨
* 파일 종료하고싶으면 ps -ef | grep 파일명.py 치고 PID번호를 알아낸다
* ex) synerex  19624(이게 PID번호) 19004  0 15:17 pts/0    00:00:00 python3 ulsan.py
* kill -9 PID번호 치면 해당 프로세스 종료
* ps -ef | grep의 뜻
  * ps : 실행 중인 프로세스를 확인 // ps -ef : 모든 프로세스 리스트 확인 // ps -aux : 프로세스 목록 배열 및 시스템 자원 사용률 확인 
  * grep : 특정 문자열이 들어있는 파일을 검색하고 싶을 때 사용 
* 백그라운드 실행 프로세스 확인 
  * jobs -l 명령어

* **문제 발생** ==> **해결 완료**
  * python ulsan.py 2>&1 & 명령어로 백그라운드 실행으로 데이터베이스에 계측기 데이터 insert 파일을 ssh 연결이 끊어져도 계속 실행하려하는데 오류가 발생하여 파일 실행이 자꾸 멈춤.....
  * ====> 2>1&1 &은 출력을 전부 없애고 데몬에서 구동하는것(2는 표준 에러, >는 그쪽으로 리다이렉트, &1은 표준출력, &은 데몬,백그라운드,에서 구동시키게 하는것)
  * ====> 해결: tmux(terminal multiplexer)를 사용하여 영구적인 세션을 제공받아 세션에서 실행되는 프로그램(py파일)을 ssh 연결이 끊겨도 유지되게 한다.
    * 세션이름 db_insert라고 만들어놓음
    * ssh 연결 -> 새로운 세션 만들기 tmux new -s 세션이름 -> 세션을 제거하고싶으면 tmux kill-session -t 세션이름 또는 세션들어가서 exit 명령어 치기 -> 현재 세션 숨기기(다시 ssh연결했을 때 처음 화면으로 돌아가기) ctrl +b하고(ctrl키에서 손 떼고) d -> ssh 연결 끊고 다시 접속해도 해당 세션은 계속 돌아가고 있는중 -> 해당 세션으로 다시 들어가고싶으면 tmux attach -t 세션이름  
    * python chung.py > /home/synerex/j/chung.log 2>&1 &로 실행 시켜서 오류가 발생했을 때 /home/synerex/j 디렉토리에 chung.log를 생성하여 오류 메시지 저장되게 만듬 // ulsan도 마찬가지로... 

* **문제점** : 
  * 1. 만약 chung.py 파일 실행하다가 계측기 데이터받아오는 메인서버와 소켓 연결이 끊기면?? 
    * ==> 메인서버가 꺼지거나 포트번호를 바꾸는 상황이 발생하지 않는 이상 소켓 연결은 정상적일듯
  * 2. 소켓연결은 정상인데 현장에서 계측기를 꺼놔서 데이터수신이 없는 상황(데이터가 0인 상황)이면 ??
    * ==> chung.py에서 data 변수 값이 아무것도 없는 상황인데 어떻게 극복??

---
## 노트북 파일을 회사 서버로 옮기는 방법
* 내 노트북에서 cmd 연 후 
* scp (-r) C:/Users/LG/desktop/ulsan.py synerex@211.62.179.66:/home/synerex/j
* 디렉토리 옮기는건 (-r) 추가
* 여러개 파일은 그냥 C:/Users/LG/desktop/ulsan.py C:/Users/LG/desktop/ulsan.py C:/Users/LG/desktop/ulsan.py 띄어쓰기로 여러번 쓰면 된다.
  
---
## rabbitMQ 사용 이유
* 주로 백엔드는 restful,soap, graphQL등의 API서버라고 불리는 것과 Analysis서버로 나뉠 수 있다. 이 둘을 하나의 서버에서 돌리는 건 위험!!
  * 사용자 접속해서 트래픽 발생시키는 API와// 데이터를 계속해서 처리하고 있는 분석 서버가 같이 돌아가면 서로에게 부담을 주는 상황 발생하면 심각한 오류 올 수 있다.
* 분석서버와 API서버(아마 웹서버??) 사이의 데이터 교환이 이뤄져야하는데 위와 같은 하나의 서버가 터져버리면 오류가 발생하니까 rawdata(계측기데이터)같은 실시간으로 들어오는 데이터를 바로 분석 서버나 웹 서버로 보내는게 아니라 rabbitMQ라는 큐에 담아놓고 분석 서버나 웹서버가 필요하는 양의 데이터만큼만 rabbitMQ 저장된 큐에서 가져오면 과부화를 줄일 수 있다. 

---
## rabbitMQ 설치완료 
* 노트북 브라우저에서 http://211.62.179.66:15672/ 검색하면 rabbitmq management화면이 표시된다. => 브라우저로 관리할 수 있는 화면


--
## 방화벽 라이브러리 firewall-cmd설치
* 명령어 앞에 다 sudo붙여주기!!
* http접속 허용 : firewall-cmd --permanent --add-service=http
* 80포트 접속 허용 :  firewall-cmd --permanent --add-port=80/tcp
* 접속 허용후 이 명령어 실행해야함 : firewall-cmd --reload
* 포트 접속 허용된 리스트 확인하기 : firewall-cmd --list-ports 
* **오류** firewall-cmd의 오류로 인해 포트 접속 허용하려면 sudo iptables -I INPUT 1 -p tcp --dport 3000 -j ACCEPT 이 명령어 실행해야함(여기서는 3000번 포트 허용하겠다는 뜻)
 
---
## 서버내 플라스크 설치 완료
* 포트번호를 열고 사용해야함 
* 가상환경으로 실행해서 구현하는게 더 좋을듯 
  * 가상환경 만들기 : cd ~/로 홈디렉토리에서 virtualenv '가상환경폴더명' 명령어 실행
  * 가상환경 실행하기 : source '가상환경폴더명'/bin/activate
  * 가상환경 종료 : deactivate
* port는 5550번만 접속 허용해놓음 일단
* flask_code 폴더에 있는 app.py파일 실행하고 브라우저에 211.62.179.66/5550/main 입력하면 웹 화면 보임

---
## 디렉토리 삭제
* rm -r 디렉토리명 

---
## uWSGI , nginx , docker
* WSGI는 Web Server Gateway Interface의 약어로 웹서버와 웹 애플리케이션이 어떤 방식으로 통신하는가에 관한 인터페이스로써, 웹 서버와 웹어플리케이션 간의 소통을 정의해 애플리케이션과 서버가 독립적으로 운영될 수 있게 돕는다
* flask 어플리케이션을 실행시키면 웹 서버가 가동이 되지만 쉽게 디버깅을 할 수 있도록 테스트 웹 서버만 제공해줄 뿐이지 실제 운영환경에서는 사용하면 안되기 때문에 nginx나 apache같은 웹 서버를 통해 서비스를 배포해야함
* uWSGI는 웹 어플리케이션을 구축하는데 사용하는 것, 윈도우에서는 호환이 불가능해서 우리 개발 환경과 맞음
* **uSWGI 문제??** : g유니콘이나 cherrypi에 비해 자원 소모 많고 ram,cpu 사용이 크다 그래서 우리 개발 환경에 맞게 g유니콘을 사용할 필요성도 느껴짐...!! 
* **Docker** : 일일이 uWSGI, g유니콘, nginx등을 플라스크와 연결하여 사용할 수 도 있지만 docker를 활용하면 이미 짜여진 환경을 불러와서 간편하게 사용할 수 도있으니까 이것도 알아보는거 좋을 듯.....!!

---
## VScode에서 ssh연결에서 개발 환경 구축하기

---
## Flask
* http://211.62.179.66:3000/ 브라우저에 치면 실행시킨 flask앱 볼 수 있다.
