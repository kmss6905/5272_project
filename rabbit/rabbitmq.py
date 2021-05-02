import socket
import redis
import pika

HOST = '211.62.179.65'
PORT = 10008

redisClient = redis.StrictRedis(host='127.0.0.1', port=6379, db=0) # redis 접속
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost')) # rabbit mq 접속
channel = connection.channel()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT)) # socket 연결
    while 1:
        data = s.recv(1024)
        if data is not None:
            data2 = data.decode("utf-8").split('$') # 파싱
            name = data2[0]
            real_data = data2[1].split(',')
            redisClient.hset(name, str(real_data[1]), str(real_data[2])) # redis 데이터 저장
            channel.basic_publish(exchange='amq.topic', routing_key='test', body=str(data)) # rabbit mq 에 데이터 pub
            print(" [x] send %r" % str(data))