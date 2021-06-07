import db_conn 
import pymysql
from time import time
from datetime import datetime, timedelta
import redis
import json
import pandas as pd
from twilio.rest import Client

# 건물별 이상여부
def warning_building(building_name):
    conn = db_conn.get_connection()
    sql = 'select building.building_tf,user.user_phone_number from building inner join user on building.building_user_id=user.user_id where building.building_name = %s '
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql,building_name)
    rows = cursor.fetchall()
    conn.close()
    result = {
        "building_name":building_name,
        "is_warn" : rows[0]['building_tf']
    }
    if rows[0]['building_tf'] =='이상발생':
        account_sid = 'AC3b9a05724c78abd037b899eff26f9358'
        auth_token = '056beb7d7acfd15640ce9c958b8d4f3d'
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            to=rows[0]['user_phone_number'],
            from_="+18595349674",
            body="건축물 이상 발생!!")
    return result
# return 요청 : /api/building/{building_name}/status -> {"building_name":'충무로영상센터',"building_tf":'정상'}

# warning_building('충무로영상센터')

# 계측기별 이상여부
def warning_device(building_name,device_id):
    tf = "정상"
    # t_date = datetime.today()
    # t_date_minus = t_date - timedelta(minutes=10)
    t_date = datetime(2021,6,4).date()
    t_date_minus = t_date - timedelta(days=1)
    conn = db_conn.get_connection()
    sql_th = 'select device_criteria_latitude,device_criteria_longitude,device_criteria_height,device_criteria_latitude_min,device_criteria_longitude_min,device_criteria_height_min from device where device_id =%s'
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql_th,device_id)
    threshold = cursor.fetchall()
    df_th = pd.DataFrame(data={
        'lat':[threshold[0]['device_criteria_latitude'],threshold[0]['device_criteria_latitude_min']],
        'long':[threshold[0]['device_criteria_longitude'],threshold[0]['device_criteria_longitude_min']],
        'height':[threshold[0]['device_criteria_height'],threshold[0]['device_criteria_height_min']]
    }) 
    if device_id =='syntest1':
        sql = 'select MAX(Latitude)/100,MAX(Longitude)/100,MAX(Height),MIN(Latitude)/100,MIN(Longitude)/100,MIN(Height) from rawdata_chung where (device_id = %s) and (Create_time between %s and %s)'
    else:
        sql = 'select MAX(Latitude)/100,MAX(Longitude)/100,MAX(Height),MIN(Latitude)/100,MIN(Longitude)/100,MIN(Height) from rawdata_ulsan where (device_id = %s) and (Create_time between %s and %s)'
    values = (device_id,t_date_minus,t_date)
    cursor.execute(sql,values)
    tf_data = cursor.fetchall()
    df = pd.DataFrame(data={
        'lat':[tf_data[0]['MAX(Latitude)/100'],tf_data[0]['MIN(Latitude)/100']],
        'long':[tf_data[0]['MAX(Longitude)/100'],tf_data[0]['MIN(Longitude)/100']],
        'height':[tf_data[0]['MAX(Height)'],tf_data[0]['MIN(Height)']]
    }) 

    tf_decide = ((df_th-df)['lat'][0]>0 or (df_th-df)['lat'][0]<0) and ((df_th-df)['long'][0]>0 or (df_th-df)['long'][0]<0) and ((df_th-df)['height'][0]>0 or (df_th-df)['height'][0]<0) 
    is_warn = "정상" if tf_decide else "이상발생"
    result = {
        'device_id' : device_id,
        'is_warn' : is_warn
    }
    if not tf_decide:
        sql_up = 'UPDATE building SET building_tf= %s WHERE building_name=%s'
        values = (is_warn,building_name)
        cursor.execute(sql_up,values)
        conn.commit()
    # else:
    #     sql_up = 'UPDATE building SET building_tf= %s WHERE building_name=%s'
    #     values = (is_warn, building_name)
    #     cursor.execute(sql_up, values)
    #     conn.commit()
    return result
#     # return 요청 : /api/{충무로 ... }/ systest1 / status -> { "device" :"syntest1", "device_tf" : "정상" }
# print(warning_device('울산','2223'))


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