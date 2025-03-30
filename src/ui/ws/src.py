import asyncio
import json
import os
import re
# import zmq

from dotenv import load_dotenv
from websockets.asyncio.server import ServerConnection, serve
from websockets.exceptions import ConnectionClosedOK, ConnectionClosedError

load_dotenv()

import pika
import asyncio

def callback(ch, method, properties, body):
    print(ch, method, properties, body)
    data = json.loads(body)

    ws_connection = ws_connections[data.pop('connection_id')]
    cor = send_to_browser(ws_connection, 'card', data)
    asyncio.run(cor)

# connection = pika.BlockingConnection()
# channel = connection.channel()
# channel.queue_declare(queue='api-adapters-output')
# channel.basic_consume(queue='api-adapters-output', auto_ack=True, on_message_callback=callback)

###################

def on_connected(connection):
    """Called when we are fully connected to RabbitMQ"""
    connection.channel(on_open_callback=on_channel_open)
    print('connected', connection)

def on_close(connection, exception):
    # Invoked when the connection is closed
    connection.ioloop.stop()
    print('stopped', exception)

channel = None
def on_channel_open(new_channel):
    """Called when our channel has opened"""
    global channel
    channel = new_channel
    # channel.queue_declare(queue="test", durable=True, exclusive=False, auto_delete=False, callback=on_queue_declared)
    channel.basic_consume(queue='api-adapters-output', auto_ack=True, on_message_callback=callback)
    channel.queue_declare(queue='api-adapter-tg')
    channel.queue_declare(queue='api-adapter-vk')
    channel.queue_declare(queue='api-adapters-output')
    print('channel openned', channel)

connection = pika.SelectConnection(pika.ConnectionParameters('localhost'), on_open_callback=on_connected, on_close_callback=on_close)

import threading

thread = threading.Thread(target=connection.ioloop.start)
thread.start()

###################


WS_SERVER_PORT = os.getenv('WS_SERVER_PORT')

async def send_to_browser(websocket, what, data):
    await websocket.send(json.dumps({what: data}))


def send_to_broker(topic, data):
    channel.basic_publish(exchange='', routing_key=topic, body=json.dumps(data))
    # socket.send(json.dumps([topic, data]).encode())


def get_from_broker(topic):
    method_frame, header_frame, body = channel.basic_get(topic, True)
    # socket.send(json.dumps([topic, None]).encode())
    # message = socket.recv()
    # print(message)
    # return json.loads(message)
    print(method_frame, header_frame, body)
    # if method_frame:
    #     channel.basic_ack(method_frame.delivery_tag)

    if body:
        return json.loads(body)

ws_connections = {}

async def view_start_process(websocket):
    ws_connections[websocket.id.hex] = websocket
    while True:
        try:
            data_str = await websocket.recv()
            if isinstance(data_str, str):
                data_json = json.loads(data_str)
                link = data_json.get('link')
                if link:
                    adapter_code = None
                    if link.startswith('https://t.me/'):
                        adapter_code = 'tg'
                    elif link.startswith('https://vk.com/'):
                        adapter_code = 'vk'
                    
                    send_to_broker(f'api-adapter-{adapter_code}', {'link': link, 'connection_id': websocket.id.hex})

                    # card = {'title': 'Ресторан "Булгария"', 'description': 'Традиционный ресторан города', 'short_description': 'Ресторан, кейтеринг, банкеты', 'count_members': 102400, 'is_mine': True}
                    # await send_to_browser(websocket, 'card', card)
        except ConnectionClosedOK as _:
            del ws_connections[websocket.id.hex]
            break
        except ConnectionClosedError as _:
            del ws_connections[websocket.id.hex]
            break
        except Exception as error:
            raise error

        # card = get_from_broker('api-adapters-output')
        # card = {'title': 'Their title', 'description': 'Their description', 'short_description': 'Their description', 'count_members': 10, 'is_mine': True}
        # if card:
            # await send_to_browser(websocket, 'card', card)


url_patterns = [
    [r'/ws/start_process/', view_start_process],
]


async def handler(websocket: ServerConnection):
    print('path is', websocket.request.path)
    for url in url_patterns:
        if len(url) == 2:
            url.append(re.compile(url[0]))

        matched_object = url[2].match(websocket.request.path)
        if matched_object:
            await url[1](websocket, **(matched_object.groupdict()))
            return

    await websocket.close()


async def main(port):
    async with serve(handler, "", port):
        await asyncio.get_running_loop().create_future()  # run forever
        thread.stop()


if __name__ == "__main__":
    asyncio.run(main(WS_SERVER_PORT))
