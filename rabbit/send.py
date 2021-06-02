import socket
import pika
from datetime import date,datetime
import timeit
import pymysql

today = str(date.today())
# 모든 계측기의 device_id를 가져오기
def all_device_id():
    conn = pymysql.connect(host='211.62.179.66', user='root', password='tlsjfprtm', db='test', charset='utf8')
    sql ='select device_id from device'
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql)
    rows = cursor.fetchall()
    conn.close()
    id_list = [i['device_id'] for i in rows]
    return id_list
all_device_id = all_device_id() # ['syntest1', '2214', '2221', '2222', '2223', 'test']

credentials = pika.PlainCredentials(username='syntest',password='syntest')
connection = pika.BlockingConnection(pika.ConnectionParameters('211.62.179.66',
                                   credentials=credentials)) # rabbit mq 접속
channel = connection.channel()
channel.exchange_declare(exchange='device_data',exchange_type='topic')
        
# queue 이름을 device_id와 연결지으면 될듯
channel.queue_declare(queue='syntest1') # 데이터 보내기전 수신자 큐가 있는 지 확인/ 존재하지 않는 위치로 메시지 보내면 메시지 삭제됨/ 메시지가 배달 될 큐의 이름을 hello로 지정

my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_socket.settimeout(15)  # 데이터 recv안될 때 15초정도는 기다리는 코드
try:
    HOST =  '211.62.179.69'
    PORT = 10004
    my_socket.connect((HOST,PORT))
    while 1:
        data = my_socket.recv(1024)
        # 데이터 파싱 부분
        data = str(data).split(',')
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
        if id =='2214':
            routing_key = id
            print(routing_key)
        else:
            continue
        channel.basic_publish(exchange='device_data', routing_key=routing_key, body=data_list) # rabbit mq 에 데이터 pub
        print(" [x] send ")
except socket.timeout:
    print('Data receive Error')