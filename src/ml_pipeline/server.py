import json

import pika
from worker import find_societies_by_link


channel = None

def callback(ch, method, properties, body):
    print(body)
    recieved_data = json.loads(body)
    answer = find_societies_by_link(recieved_data['link'])
    print(answer)
    print()
    data = {'description': answer}
    data['connection_id'] = recieved_data['connection_id']
    channel.basic_publish(exchange='', routing_key='api-adapters-output', body=json.dumps(data))


def on_connected(connection):
    """Called when we are fully connected to RabbitMQ"""
    connection.channel(on_open_callback=on_channel_open)
    print('connected', connection)


def on_close(connection, exception):
    # Invoked when the connection is closed
    connection.ioloop.stop()
    print('stopped', exception)

# Step #3
def on_channel_open(new_channel):
    """Called when our channel has opened"""
    global channel
    channel = new_channel
    # channel.queue_declare(queue="test", durable=True, exclusive=False, auto_delete=False, callback=on_queue_declared)
    channel.basic_consume(queue='llm-input', auto_ack=True, on_message_callback=callback)
    channel.queue_declare(queue='llm-output')
    print('channel openned', channel)


connection = pika.SelectConnection(pika.ConnectionParameters('localhost'), on_open_callback=on_connected, on_close_callback=on_close)

try:
    # Loop so we can communicate with RabbitMQ
    connection.ioloop.start()
except KeyboardInterrupt:
    # Gracefully close the connection
    connection.close()
    # Loop until we're fully closed.
    # The on_close callback is required to stop the io loop
    connection.ioloop.start()