import db_conn # db_conn.py 불러오기
import pymysql
from time import time

# 유저의 계측기 정보들을 가져옵니다.
def get_device_list():
    conn = db_conn.get_connection()
    sql ='select * from device inner join building_type on device.device_building_type = building_type.building_type where device_user_id=1'
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql)
    rows = cursor.fetchall()
    conn.close()
    return rows
#해당 건물의 계측기 정보들
def each_device_building2(login_user_id,building_name):
    conn = db_conn.get_connection()
    sql ='select * from device LEFT JOIN building ON device.building_name=building.building_name where device.device_user_id=%s and device.building_name = %s'
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    values = (login_user_id,building_name)
    cursor.execute(sql,values)
    infos = cursor.fetchall()
    conn.close()
    return infos

if __name__ == "__main__":
    get_device_list()