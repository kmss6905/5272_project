import socket
import pymysql
from datetime import date
today = str(date.today())
# 영상센터 
HOST = '211.62.179.65'
PORT = 10008
PORT = 10008


conn = pymysql.connect(host='localhost', user = 'root', password='s12131213', db = 'test',charset = 'utf8')
curs = conn.cursor(pymysql.cursors.DictCursor)
idx = 0

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while 1:
        data = s.recv(1024)
        idx+=1
        sql = "insert into rawdata_chung values (%s,%s,%s,%s,%s,%s,%s)"

        # 데이터 파싱 부분
        data = str(data).split(',')

        id = data[0] # 계측기 번호
        time = data[1] # 계측 시간
        if int(time[:2])+9 >24:
            trans_time = str(int(time[:2]) - 24)
        else:
            trans_time = str(int(time[:2]) + 9)

        time = today +' '+ trans_time +':'+ time[2:4] +':'+ time[4:6] 

        print(time)
        latitude = data[2] # latitude
        longitude = data[4] # longitude
        height = data[9] # height
        geoid_height = data[11] # geoid_height

        print(idx,id,time,latitude,longitude,height,geoid_height)

        val = (idx,id, time, latitude,longitude,height,geoid_height)
        curs.execute(sql, val)
        conn.commit()