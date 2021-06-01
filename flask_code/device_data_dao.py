import db_conn # db_conn.py 불러오기
import pymysql
from time import time
from datetime import datetime

# 유저의 계측기 정보들을 가져옵니다.
def get_device_list():
    conn = db_conn.get_connection()
    sql ='select * from device inner join building_type on device.device_building_type = building_type.building_type where device_user_id=1'
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql)
    rows = cursor.fetchall()
    conn.close()
    return rows

# 유저의 계측기 정보들을 가져옵니다.
def get_data():
    conn = db_conn.get_connection()
    sql ='SELECT CAST(UNIX_TIMESTAMP(Create_time)/3600 AS SIGNED) ,FROM_UNIXTIME(CAST(UNIX_TIMESTAMP(Create_time)/3600 AS SIGNED)*3600) AS tDate ,COUNT(*) cnt, AVG(Longitude), AVG(Latitude), AVG(Height), device_id FROM rawdata_ulsan WHERE Create_time BETWEEN "2021-04-29 15:15:00" AND "2021-04-30 23:59:59" AND device_id=2214 GROUP BY 1'
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql)
    rows = cursor.fetchall()
    conn.close()
    print(rows)
    return rows
# 1.개별 계측기에 대한 기본정보
def all_device_info():
    conn = db_conn.get_connection()
    sql ='select device.device_location,user.user_phone_number,device.device_latitude,device.device_longitude,device.device_height from device inner join user on user.user_id= device.device_user_id '
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql)
    rows = cursor.fetchall()
    conn.close()
    return rows
# 2.해당 건물에 위치한 또다른 계측기를 볼 수 있도록 
def each_device_building(login_user_id,building_name):
    conn = db_conn.get_connection()
    sql ='select distinct(device_id) from device LEFT JOIN building ON device.building_name=building.building_name where device.device_user_id=%s and device.building_name = %s'
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    values = (login_user_id,building_name)
    cursor.execute(sql,values)
    infos = cursor.fetchall()
    conn.close()
    return infos

def each_device_info(device_id):
    conn = db_conn.get_connection()
    sql ='select device.device_location,user.user_phone_number,device.device_latitude,device.device_longitude,device.device_height from device inner join user on user.user_id= device.device_user_id where device.device_id=%s'
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql,device_id)
    rows = cursor.fetchall()
    conn.close()
    return rows

# 모든 사용자의 총 계측기 개수
def get_all_device():
    conn = db_conn.get_connection()
    sql ='select count(distinct(device_id)) from device'
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql)
    counts = cursor.fetchall()
    conn.close()
    return counts
# 로그인 후 나의 계측기 개수// 예외처리필요??
def get_my_device(login_user_id):
    conn = db_conn.get_connection()
    sql ='select count(distinct(device_id)) from device INNER JOIN user ON device_user_id = %s'
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql,login_user_id)
    counts = cursor.fetchall()
    conn.close()
    return counts

# 계측기 등록하기 (/register) //  구조물이름, 구조물종류,구조물 주소, 계측기 번호(device_id), 계측기 위치
def index_find_device():
    conn = db_conn.get_connection()
    sql_select = 'select MAX(id) from device'
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql_select)
    id_idx = cursor.fetchone()
    conn.close()
    return id_idx
def index_find_building():
    conn = db_conn.get_connection()
    sql_select = 'select MAX(id) from building'
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql_select)
    id_idx = cursor.fetchone()
    conn.close()
    return id_idx

def register_my_device(login_user_id,b_name,b_type,b_addr,d_id,d_name,d_loc):
    lat,long,height = d_loc.split('/')
    t_date = datetime.today()
    conn = db_conn.get_connection()
    max_id = index_find_device()['MAX(id)'] +1
    sql_insert ='insert into device values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    values = (max_id,d_id,d_name,login_user_id,t_date,pymysql.NULL,pymysql.NULL,pymysql.NULL,pymysql.NULL,b_type,b_addr,b_name,float(lat),float(long),float(height))
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql_insert,values)
    conn.commit()
    conn.close()

def register_device_to_building(login_user_id,b_name,b_type,b_addr):
    conn = db_conn.get_connection()
    max_id = index_find_building()['MAX(id)'] +1
    sql_find = 'select building_type_name from building_type where building_type = %s'
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql_find,b_type)
    b_type_name = cursor.fetchone()
    sql_insert ='insert into building values (%s,%s,%s,%s,%s,%s)'
    values = (max_id,b_addr,b_type,b_type_name['building_type_name'],b_name,login_user_id)
    cursor.execute(sql_insert,values)
    conn.commit()
    conn.close()


