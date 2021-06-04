import db_conn 
import pymysql
from time import time
from datetime import datetime, timedelta
import redis
import json
# 개별 계측기별로 tf
def warning_tf():
    tf = True
    t_date = datetime.today()
    t_date_minus = t_date - timedelta(seconds=10)

    
    return 

    # 요청 : /api/{충무로 ... }/ systest1 / status -> { "device" :"syntest1", "is_warn" : "정상" }

# 건물별로 tf 
def building_warning():
    return
# /api/building/{building_name}/status -> {"building_name":'충무로',"is_warn":'정상'}



# def insert_dd(device_id):
#     conn = db_conn.get_connection()
#     sql ='select MAX(Latitude),MAX(Longitude),MAX(Height),MIN(Latitude),MIN(Longitude),MIN(Height) from rawdata_chung where (Create_time between %s and %s)'
#     cursor = conn.cursor(pymysql.cursors.DictCursor)
#     values = ('2021-04-24','2021-04-30')
#     cursor.execute(sql,values)
#     rows = cursor.fetchall()
#     conn.close()
#     return rows
# def insert_d(device_id):
#     conn = db_conn.get_connection()
#     sql ='select MAX(Latitude),MAX(Longitude),MAX(Height),MIN(Latitude),MIN(Longitude),MIN(Height) from rawdata_ulsan where (device_id=%s) and (Create_time between %s and %s)'
#     cursor = conn.cursor(pymysql.cursors.DictCursor)
#     values = (device_id,'2021-04-24','2021-04-30')
#     cursor.execute(sql,values)
#     rows = cursor.fetchall()
#     conn.close()
#     return rows
# def insert_dd(device_id):
#     conn = db_conn.get_connection()
#     sql_s ='select MAX(Latitude),MAX(Longitude),MAX(Height),MIN(Latitude),MIN(Longitude),MIN(Height) from rawdata_ulsan where (device_id=%s) and (Create_time between %s and %s)'
#     cursor = conn.cursor(pymysql.cursors.DictCursor)
#     v = (device_id,'2021-04-24','2021-04-30')
#     cursor.execute(sql_s,v)
#     result = cursor.fetchall()
#     sql ='UPDATE device SET device_criteria_latitude=%s, device_criteria_longitude=%s, device_criteria_height=%s,device_criteria_latitude_min=%s,device_criteria_longitude_min=%s,device_criteria_height_min=%s WHERE device_id = %s'
#     values = (float(result[0]['MAX(Latitude)'])/100,float(result[0]['MAX(Longitude)'])/100,float(result[0]['MAX(Height)']),float(result[0]['MIN(Latitude)'])/100,float(result[0]['MIN(Longitude)'])/100,float(result[0]['MIN(Height)']),device_id)
#     cursor.execute(sql,values)
#     conn.commit()
#     conn.close()
# insert_dd('2223')