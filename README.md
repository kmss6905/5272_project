# capstone_5272
---
## ssh 접속
* 구축한서버ip : 211.62.179.66
* hostname : synerex
* password : 시너렉스(영타)
* 유저 : synerex
* 접속 방법 : 
  * ssh synerex@211.62.179.66 입력
  * password : 시너렉스(영타)

---
## 충무로 영상센터 ip/port
* tcp://211.62.179.65:10008

---
## 울산 현대중공업 데이터
* ip : 211.62.179.69
* port : 10004
* 총 4대 1hz 단위로
---
## 전체적 프로세스
* 회사내 메인 서버 => 새로 설치한 서버
  * 람다 아키텍쳐 : 
    * 한쪽으로는 mariadb에 실시간으로 들어오는 모든 데이터 저장 후 배치 처리를 하는 배치 뷰를 가진 프로세스
      * ==> 실시간으로 처리하지 않아도 되거나 속도가 느려도 되는 뷰에서 활용한다.
    * 다른 한쪽에서는 rabbitMQ(메세지 브로커)를 활용하고 큐를 만들고(redis나 mongodb활용) 메세지를 사용하여 실시간으로 실시간 뷰 처리 하는 프로세스 
      * ==> 실시간으로 처리되야하는 뷰에서 활용한다. ex) 평균값 API, 실시간 움직임 API등
  * 결국 두개의 프로세스에서 배치뷰와 실시간뷰를 적절히 활용하여 최종 화면를 구성하는 것!!
---

## MariaDB 접근
* mysql -u root -p 입력하고 시너렉스(영문) 비밀번호 입력하면 root계정으로  mariadb접속 할 수 있다
  
* db 시간대 서울로 설정 완료!
---
## 데이터베이스 테이블 설정
* 테이블은 계측기 울산인지 충무로인지에 따라 다르게 설계해야함...!
* create table rawdata_chung
  * -> (device_idx INT NOT NULL,device_id VARCHAR(30) NOT NULL,Create_time DATETIME NOT NULL, Latitude DOUBLE NOT NULL, Longitude DOUBLE NOT NULL,Height DOUBLE NOT NULL, Geoid_heigth DOUBLE NOT NULL);
  
* create table rawdata_ulsan
  * (device_idx INT NOT NULL,device_id INT NOT NULL,Create_time DATETIME NOT NULL, Latitude DOUBLE NOT NULL, Longitude DOUBLE NOT NULL,Height DOUBLE NOT NULL, Geoid_heigth DOUBLE NOT NULL);
  
* test 데이터베이스에 rawdata라는 테이블 생성
  * rawdata테이블은 계측기 데이터 원본 그대로 필요한것만 저장하기 위한 테이블 


* 울산과 충무로 데이터 파싱이 달라야함!!
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
---
## 노트북 파일을 회사 서버로 옮기는 방법
* scp C:/Users/LG/desktop/ulsan.py synerex@211.62.179.66:/home/synerex/j
---
## DB 용량 확인
> SELECT table_schema, sum(data_length) /1024/1024 AS mb FROM information_schema.tables GROUP BY table_schema ORDER BY sum(data_length+index_length) DESC;


---
## rabbitMQ 사용 이유
* 주로 백엔드는 restful,soap, graphQL등의 API서버라고 불리는 것과 Analysis서버로 나뉠 수 있다. 이 둘을 하나의 서버에서 돌리는 건 위험!!
  * 사용자 접속해서 트래픽 발생시키는 API와// 데이터를 계속해서 처리하고 있는 분석 서버가 같이 돌아가면 서로에게 부담을 주는 상황 발생하면 심각한 오류 올 수 있다.
* 분석서버와 API서버(아마 웹서버??) 사이의 데이터 교환이 이뤄져야하는데 위와 같은 하나의 서버가 터져버리면 오류가 발생하니까 rawdata(계측기데이터)같은 실시간으로 들어오는 데이터를 바로 분석 서버나 웹 서버로 보내는게 아니라 rabbitMQ라는 큐에 담아놓고 분석 서버나 웹서버가 필요하는 양의 데이터만큼만 rabbitMQ 저장된 큐에서 가져오면 과부화를 줄일 수 있다. 

---
## rabbitMQ 설치완료 
* 노트북 브라우저에서 http://211.62.179.66:15672/ 검색하면 rabbitmq management화면이 표시된다. => 브라우저로 관리할 수 있는 화면

---
## redis는 설치에 오류가 있는중,,,

---
## 방화벽 라이브러리 firewall-cmd설치
* 명령어 앞에 다 sudo붙여주기!!
* http접속 허용 : firewall-cmd --permanent --add-service=http
* 80포트 접속 허용 :  firewall-cmd --permanent --add-port=80/tcp
* 포트 접속 허용된 리스트 확인하기 : firewall-cmd --list-ports 

  
---
## 4월25일 (일)
* 서버에 Django 설치한 뒤 mariadb에 실시간으로 저장되고 있는 데이터 연동하여 간단한 뷰(브라우져)만들어 보기 ==> 이건 오늘 간단한 테스트용,,,