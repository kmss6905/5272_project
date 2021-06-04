import pika
import sys
import redis
import json
import time

def receive(device_id):
    rd = redis.StrictRedis(host='localhost', port=6379, db=0) # redis 접속
    credentials = pika.PlainCredentials(username='syntest',password='syntest')
    connection = pika.BlockingConnection(pika.ConnectionParameters('211.62.179.66',
                                    credentials=credentials)) # rabbit mq 접속
    channel = connection.channel()

    channel.exchange_declare(exchange=device_id, exchange_type='direct')
    result = channel.queue_declare(queue='',exclusive=True) # consumer가 disconnect될 동시에 해당 queue도 자동으로 삭제
    queue_name = result.method.queue

    channel.queue_bind(queue=queue_name,exchange=device_id,routing_key=device_id)

    print(' [*] Waiting for logs. To exit press CTRL+C')

    def callback(ch, method, properties, body):
        data = str(body).split(',')
        dataDict = {
            "id" : data[0],
            "time" : data[1],
            "lat" : data[2],
            "long" : data[3],
            "height" : data[4]
        }
        jsonDataDict = json.dumps(dataDict, ensure_ascii=False).encode('utf-8')
        rd.set("tf",jsonDataDict)
        rd.set('dict', jsonDataDict)
        print('receive [x]')

    channel.basic_consume(queue=queue_name,
                        auto_ack=True,
                        on_message_callback=callback)
    channel.start_consuming()

receive('syntest1')


