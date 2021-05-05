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


if __name__ == "__main__":
    get_device_list()