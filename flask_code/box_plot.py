import db_conn # db_conn.py 불러오기
import pymysql
from datetime import datetime, timedelta
import pandas as pd

def box_plot(device_id,start,end):  # 시작과 끝 날짜, 원하는 계측기이름을 정해주면 해당 lat,long,heigth,create_time을 가져오는 sql 함수 
    conn = db_conn.get_connection()
    sql ='SELECT Latitude,Longitude,Height,Create_time FROM rawdata WHERE (device_id=%s) and (Create_time BETWEEN %s and %s);'
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    values = (device_id,start,end)
    cursor.execute(sql,values)
    rows = cursor.fetchall()
    conn.close()
    return rows 
    
def each_plot(df,which,box_num):  # lat,long,heigth 각각의 정해진 기간(box_num)만큼의 통계량 데이터를 뽑는 함수
    box = []
    for i in range(0,box_num):
        data = {'x':0,'low':0,'high':0,'q1':0,'median':0,'q3':0}
        t_date = datetime.today().date()
        t_date_minus = t_date - timedelta(days=i)
        data['x'] = str(t_date_minus)
        data['low'] = df.loc[str(t_date_minus)][which].describe()['min']
        data['high'] = df.loc[str(t_date_minus)][which].describe()['max']
        data['q1'] = df.loc[str(t_date_minus)][which].describe()['25%']
        data['median'] = df.loc[str(t_date_minus)][which].describe()['50%']
        data['q3'] = df.loc[str(t_date_minus)][which].describe()['75%']
        box.append(data)
    return box
    
def plot(device_id,box_num):
    lat = []
    long = []
    height = []
    time = []
    for i in range(1,box_num):
        today = datetime.today()
        today_minus = today - timedelta(days=i)
        data_all = box_plot(device_id,today_minus,today)
    for data in data_all:
        lat.append(data['Latitude'])
        long.append(data['Longitude'])
        height.append(data['Height'])
        time.append(data['Create_time'])

    df = pd.DataFrame(data={'lat':lat,'long':long,'height':height},index=time)  
    box_lat = each_plot(df,'lat',box_num)
    box_long = each_plot(df,'lat',box_num)
    box_height = each_plot(df,'lat',box_num)

    plot_data = {
        'boxplot_data':[
        {
            "value": 'lat',
            "interval":2,
            "box_num" : 7,
            "data" : box_lat
        },
        {
            "value": 'long',
            "interval":2,
            "box_num" : 7,
            "data" : box_long
        },
        {
            "value": 'height',
            "interval":2,
            "box_num" : 7,
            "data" : box_height
        }
        ]
    }
    return plot_data