import socket
import pymysql
from datetime import date,datetime
today = str(date.today())

def insert_ulsan():
    global today
    HOST =  '211.62.179.69'
    PORT = 10004

    conn = pymysql.connect(host='211.62.179.66', user = 'root', password='tlsjfprtm', db = 'test',charset = 'utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    idx = 0
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        while 1:
            data = s.recv(1024)
            if data is not None:
                print(data)
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
            else:
                print("Problem with Device!!!!!!!")
                return 

def insert_chung():
    global today
    HOST =  '211.62.179.65'
    PORT = 10008

    conn = pymysql.connect(host='211.62.179.66', user = 'root', password='tlsjfprtm', db = 'test',charset = 'utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    idx = 0

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        while 1:
            data = s.recv(1024)
            if data is not None:
                # print(data)
                idx+=1
                sql = "insert into rawdata_chung values (%s,%s,%s,%s,%s,%s,%s)"

                # 데이터 파싱 부분
                data = str(data).split(',')

                id = data[0] # 계측기 번호
                time = data[1] # 계측 시간
                if int(time[:2])+9 >24:
                    trans_time = str(int(time[:2]) - 15)
                else:
                    trans_time = str(int(time[:2]) + 9)

                time = today +' '+ trans_time +':'+ time[2:4] +':'+ time[4:6] 

                latitude = data[2] # latitude
                longitude = data[4] # longitude
                height = data[9] # height
                geoid_height = data[11] # geoid_height


                val = (idx,id, time, latitude,longitude,height,geoid_height)
                curs.execute(sql, val)
                conn.commit()
            else:
                print("Problem with Device!!!!!!!")
                return 

def create_table():
    conn = pymysql.connect(host='211.62.179.66', user = 'root', password='tlsjfprtm', db = 'test',charset = 'utf8')
    try:
        with conn.cursor() as curs:
            sql = "crate table rawdata (device_idx INT NOT NULL, device_id VARCHAR(30) NOT NULL, Create_time DATETIME NOT NULL,Latitude DOUBLE NOT NULL, Longitude DOUBLE NOT NULL,Height DOUBLE NOT NULL, Geoid_heigth DOUBLE NOT NULL) "
            curs.execute(sql, where)
    finally:
        conn.close()

def chung_last_ten():
    conn = pymysql.connect(host='211.62.179.66', user = 'root', password='tlsjfprtm', db = 'test',charset = 'utf8')
    try:
        with conn.cursor() as curs:
            sql = "select * from rawdata_chung order by Create_time desc limit 10"
            curs.execute(sql)
            rs = curs.fetchall()
            for row in rs:
                print(row)    
    finally:
        conn.close()

def ulsan_last_ten():
    conn = pymysql.connect(host='211.62.179.66', user = 'root', password='tlsjfprtm', db = 'test',charset = 'utf8')
    try:
        with conn.cursor() as curs:
            sql = "select * from rawdata_ulsan order by Create_time desc limit 10"
            curs.execute(sql)
            rs = curs.fetchall()
            for row in rs:
                print(row)    
    finally:
        conn.close()

def a_z_chung(start_date,end_date):
    conn = pymysql.connect(host='211.62.179.66', user = 'root', password='tlsjfprtm', db = 'test',charset = 'utf8')
    try:
        with conn.cursor() as curs:
            sql = "SELECT Create_time FROM rawdata_chung WHERE Create_time BETWEEN %s AND %s "
            curs.execute(sql,(start_date,end_date))
            rs = curs.fetchall()
            for row in rs:
                date = row[0].strftime("%Y/%m/%d %H:%M:%S")
                print(date)    
    finally:
        conn.close()

def a_z_ulsan(start_date,end_date):
    conn = pymysql.connect(host='211.62.179.66', user = 'root', password='tlsjfprtm', db = 'test',charset = 'utf8')
    try:
        with conn.cursor() as curs:
            sql = "SELECT Create_time FROM rawdata_ulsan WHERE Create_time BETWEEN %s AND %s "
            curs.execute(sql,(start_date,end_date))
            rs = curs.fetchall()
            for row in rs:
                date = row[0].strftime("%Y/%m/%d %H:%M:%S")
                print(date)
    finally:
        conn.close()

