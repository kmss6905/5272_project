import pika
import sys

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='211.62.179.66'))
channel = connection.channel()

channel.exchange_declare(exchange='device_data', exchange_type='topic')

result = channel.queue_declare('syntest1', exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='device_data', queue=queue_name, routing_key='syntest1')


print(' [*] Waiting for logs. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))


channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()