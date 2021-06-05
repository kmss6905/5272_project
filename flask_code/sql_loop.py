import db_conn # db_conn.py 불러오기
import pymysql
from time import time
from datetime import datetime

def pick_sql_data(device_id,which):
    conn = db_conn.get_connection()
    if device_id =='syntest1':
        if which == 'lat':
            sql ='select Latitude/100 from rawdata_chung where device_id = %s order by rand() limit 1'
        elif which == 'long':
            sql ='select Longitude/100 from rawdata_chung where device_id = %s order by rand() limit 1'
        else:
            sql ='select Height from rawdata_chung where device_id = %s order by rand() limit 1'
    else:
        if which == 'lat':
            sql ='select Latitude/100 from rawdata_ulsan where device_id = %s order by rand() limit 1'
        elif which == 'long':
            sql ='select Longitude/100 from rawdata_ulsan where device_id = %s order by rand() limit 1'
        else:
            sql ='select Height from rawdata_ulsan where device_id = %s order by rand() limit 1'
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql,device_id)
    rows = cursor.fetchall()
    conn.close()
    if which =='lat':
        result = [datetime.now().strftime('%Y-%m-%d %H:%M:%S'),rows[0]['Latitude/100']]
    elif which =='long':
        result = [datetime.now().strftime('%Y-%m-%d %H:%M:%S'),rows[0]['Longitude/100']]
    else:
        result = [datetime.now().strftime('%Y-%m-%d %H:%M:%S'),rows[0]['Height']]
    return result
    
print(pick_sql_data('syntest1','lat'))