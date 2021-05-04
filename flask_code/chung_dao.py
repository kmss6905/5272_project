import pymysql
import db_conn # db_conn.py 불러오기
from time import time

def get_chung():
    conn = db_conn.get_connection()
    sql ='select device_id,Latitude,Longitude,Height from rawdata_chung order by Create_time desc limit 1'
    cursor = conn.cursor()
    cursor.execute(sql)
    row = cursor.fetchone()

    data_list = [time()*1000,row[1],row[2]] #Latitude
    conn.close
    return data_list
get_chung()