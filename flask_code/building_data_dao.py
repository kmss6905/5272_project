import db_conn 
import pymysql
from time import time

# 모든 사용자의 총 건축물 개수
def get_all_building():
    conn = db_conn.get_connection()
    sql = 'select count(distinct(building_name)) from building'
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql)
    rows = cursor.fetchall()
    conn.close()
    return rows
# 모든 사용자의 건축물 정보 // 건축물 이름, 종류, 건축물 주소, 계측기 개수, 이상 여부
def get_all_building_info():
    conn = db_conn.get_connection()
    sql_b = 'select building_name,building_type_name,building_address from building'
    sql_d = 'select count(*) from device where building_name=%s'
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql_b)
    building_info = cursor.fetchall()
    for info in building_info:
        cursor.execute(sql_d,info['building_name'])
        device_num = cursor.fetchone()
        info['device_num'] = device_num['count(*)']
    conn.close()
    return building_info

# 로그인 후 나의 건축물의 수 //예외처리 필요??
def get_user_building(login_user_id):
    conn = db_conn.get_connection()
    sql ='SELECT count(distinct(building.building_type_name)) FROM building LEFT JOIN user ON building.building_user_id = %s'
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql,login_user_id)
    counts = cursor.fetchall()
    conn.close()
    return counts

# 지도 - 나의 건축물 위치에 마크 // 1)건축물 이름 2)종류 3)건축물 주소
def get_my_building_info_map(login_user_id):
    conn = db_conn.get_connection()
    sql ='SELECT building.building_name, building.building_type, building_address FROM building LEFT JOIN user ON building.building_user_id=%s'
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql,login_user_id)
    infos = cursor.fetchall()
    conn.close()
    return infos

# 표 - 그 건축물의 계측기 개수
def get_my_building_info_table(login_user_id,building_name):
    conn = db_conn.get_connection()
    sql ='select count(distinct(device_id)) from device LEFT JOIN building ON device.building_name=building.building_name where device.device_user_id=%s and device.building_name = %s'
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    values = (login_user_id,building_name)
    cursor.execute(sql,values)
    infos = cursor.fetchall()
    conn.close()
    return infos

# 이상 여부
def decide_criteria(login_user_id,building_name):
    conn = db_conn.get_connection()
    sql ='select device.device_criteria_latitude, device.device_criteria_longitude, device.device_criteria_height from device where device.device_user_id=%s and device.building_name = %s'
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    values = (login_user_id,building_name)
    cursor.execute(sql,values)
    infos = cursor.fetchall()
    conn.close()
    return infos