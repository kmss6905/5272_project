import socket
import pika
from datetime import date,datetime
import timeit
import pymysql
import sys
import redis
import json
import time

def send(device_id):
    today = str(date.today())

    credentials = pika.PlainCredentials(username='syntest',password='syntest')
    connection = pika.BlockingConnection(pika.ConnectionParameters('211.62.179.66',
                                    credentials=credentials)) # rabbit mq 접속
    channel = connection.channel()
    channel.exchange_declare(exchange=device_id,exchange_type='direct')

    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.settimeout(15)  
    try:
        if device_id == 'syntest1':
            HOST =  '211.62.179.65'
            PORT = 10008
            my_socket.connect((HOST,PORT))
            while 1:
                data = my_socket.recv(1024)
                data = str(data).split(',')
                id = data[0][2:10] # 계측기 번호
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
                data_list = [id,time,latitude,longitude,height,geoid_height]
                data_join = ','.join(data_list)

                channel.basic_publish(exchange=device_id, routing_key=id, body=data_join)
                print(" [x] send ")
        else:
            HOST =  '211.62.179.69'
            PORT = 10004
            my_socket.connect((HOST,PORT))
            while 1:
                data = my_socket.recv(1024)
                # 데이터 파싱 부분
                data = str(data).split(',')
                # if len(data) >18:
                #     send(device_id)
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
                data_list = [id,time,latitude,longitude,height,geoid_height]
                data_join = ','.join(data_list)
                print(data_join)
                channel.basic_publish(exchange=device_id, routing_key=id, body=data_join) # rabbit mq 에 데이터 pub
                print(" [x] send ")
    except socket.timeout:
        connection.close()
        print('Data receive Error')
        return 

send('2223')

# # 모든 계측기의 device_id를 가져오기
# def all_device_id():
#     conn = pymysql.connect(host='211.62.179.66', user='root', password='tlsjfprtm', db='test', charset='utf8')
#     sql ='select device_id from device'
#     cursor = conn.cursor(pymysql.cursors.DictCursor)
#     cursor.execute(sql)
#     rows = cursor.fetchall()
#     conn.close()
#     id_list = [i['device_id'] for i in rows]
#     return id_list
# all_device_id = all_device_id() # ['syntest1', '2214', '2221', '2222', '2223', 'test']