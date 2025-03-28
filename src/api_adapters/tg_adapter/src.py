import json

import requests
from kafka import KafkaConsumer

token = ''
url = f'https://api.telegram.org/bot{token}'


def get_chat_info(channel_id):
    channel = {'channel_id': channel_id}
    params = {'channel': channel}
    response = requests.post(f'{url}/getChat', json=params)
    print(response.status_code, response.content)


def link2channel_id(link):
    pass


consumer = KafkaConsumer('my_favorite_topic')
for message in consumer:
    data = json.loads(message)
    channel_id = link2channel_id(data['link'])
    get_chat_info(channel_id)
    print(message)
