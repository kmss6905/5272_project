import socket
import pymysql
from datetime import date
today = str(date.today())

# 울산
HOST_ulsan =  '211.62.179.69'
PORT_ulsan = 10004


conn = pymysql.connect(host='localhost', user = 'root', password='tlsjfprtm', db = 'test',charset = 'utf8')
curs = conn.cursor(pymysql.cursors.DictCursor)
idx = 0

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST_ulsan, PORT_ulsan))
    while 1:
        data = s.recv(1024)
        idx+=1
        sql = "insert into rawdata_ulsan values (%s,%s,%s,%s,%s,%s,%s)"

        # 데이터 파싱 부분
        data = str(data).split(',')

        id = data[1] # 계측기 번호

        time = data[3] # 계측 시간

        if int(time[:2])+9 >24:
            trans_time = str(int(time[:2]) - 15)
        else:
            trans_time = str(int(time[:2]) + 9)
    
        time = today +' '+ trans_time +':'+ time[2:4] +':'+ time[4:6] 
        
        latitude = data[4] # latitude
        longitude = data[6] # longitude
        height = data[11] # height
        geoid_height = data[13] # geoid_height


        val = (idx,id, time, latitude,longitude,height,geoid_height)
        curs.execute(sql, val)
        conn.commit()
