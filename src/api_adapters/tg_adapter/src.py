import json
import os

import pika
import requests
from dotenv import load_dotenv
# from kafka import KafkaConsumer
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
from qrcode import QRCode

qr = QRCode()

load_dotenv()

TOKEN = os.getenv('TG_TOKEN')
API_ID = os.getenv('APP_API_ID')  # https://my.telegram.org/apps
API_HASH = os.getenv('APP_API_HASH')
PHONE = os.getenv('PHONE')
URL = f'https://api.telegram.org/bot{TOKEN}'

# client = TelegramClient(PHONE, API_ID, API_HASH)
# client.start()

channel = None

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
    channel.basic_consume(queue='api-adapter-tg', auto_ack=True, on_message_callback=callback)
    channel.queue_declare(queue='api-adapter-tg')
    channel.queue_declare(queue='api-adapters-output')
    print('channel openned', channel)


connection = pika.SelectConnection(pika.ConnectionParameters('localhost'), on_open_callback=on_connected, on_close_callback=on_close)

def gen_qr(token:str):
    qr.clear()
    qr.add_data(token)
    qr.print_ascii()


async def main(client: TelegramClient):
    if(not client.is_connected()):
        await client.connect()
    client.connect()
    qr_login = await client.qr_login()
    print(client.is_connected())
    r = False
    while not r:
        gen_qr(qr_login.url)
        # Important! You need to wait for the login to complete!
        try:
            r = await qr_login.wait(10)
        except:
            await qr_login.recreate()


#client = TelegramClient('SessionName', API_ID, API_HASH)
#client.loop.run_until_complete(main(client))


def get_chat_info(channel_id):
    def populate_location(data, location):
        data['address'] = location['address']
        loc = location.get('location')  # https://core.telegram.org/bots/api#location
        if loc:
            data['latitude'] = loc['latitude']
            data['longitude'] = loc['longitude']

    data = {}

    params = {'chat_id': channel_id}
    response = requests.post(f'{URL}/getChat', json=params)
    if response.status_code == 200:
        response_json = response.json()
        if response_json.get('ok'):
            result = response_json['result']
            data['is_private'] = result['type'] == 'private'
            data['tg'] = {}
            data['tg']['type'] = result['type']  # private, group, supergroup, channel
            if data['is_private']:
                intro = result.get('business_intro')
                if intro:
                    data['title'] = intro['title']
                    data['description'] = intro['message']

                location = result.get('business_location')
                if location:
                    populate_location(data, location)

                opening_hours = result.get('business_opening_hours')
                if opening_hours:
                    data['time_zone_name'] = opening_hours['time_zone_name']
                    data['openning_time'] = []
                    for interval in opening_hours['opening_hours']:  # https://core.telegram.org/bots/api#businessopeninghoursinterval
                        start = interval['opening_minute']
                        end = interval['closing_minute']
                        data['openning_time'].append(f'{start} - {end}')

                data['bio'] = result['bio']
            else:
                data['title'] = result.get('title')
                data['short_description'] = result.get('description')
                data['description'] = result.get('pinned_message', {}).get('text', '')
                data['tg']['is_forum'] = result.get('is_forum')  # True, if the supergroup chat is a forum (has topics enabled)
                location = result.get('location')
                if location:
                    populate_location(data, location)


    params = {'chat_id': channel_id}
    response = requests.post(f'{URL}/getChatMemberCount', json=params)
    if response.status_code == 200:
        response_json = response.json()
        if response_json.get('ok'):
            data['count_members'] = response_json['result']

    # if not data.get('is_private', True):
    #     history = client(GetHistoryRequest(
    #         peer=channel_id,
    #         offset_id=0,
    #         offset_date=None,
    #         add_offset=0,
    #         limit=10,
    #         max_id=0,
    #         min_id=0,
    #         hash=0
    #     ))
    #     data['messages'] = [message.message for message in history.messages]

    return data


def link2channel_id(link):
    if link.startswith('@'):
        return link
    
    if link.startswith('https://t.me/') or link.startswith('t.me/'):
        chat_name = link.split('/')[-1]
        return f'@{chat_name}'


def callback(ch, method, properties, body):
    print(body)
    recieved_data = json.loads(body)
    chat_id = link2channel_id(recieved_data['link'])
    data = get_chat_info(chat_id)
    print(data)
    data['connection_id'] = recieved_data['connection_id']
    channel.basic_publish(exchange='', routing_key='api-adapters-output', body=json.dumps(data))


try:
    # Loop so we can communicate with RabbitMQ
    connection.ioloop.start()
except KeyboardInterrupt:
    # Gracefully close the connection
    connection.close()
    # Loop until we're fully closed.
    # The on_close callback is required to stop the io loop
    connection.ioloop.start()

# consumer = KafkaConsumer(bootstrap_servers='10.2.0.244:9093')

# for message in consumer:
#     data = json.loads(message)
#     channel_id = link2channel_id(data['link'])
#     data = get_chat_info(channel_id)
#     print(message, data)
