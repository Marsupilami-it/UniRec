import json
import os

import requests
from dotenv import load_dotenv
from kafka import KafkaConsumer

load_dotenv()

TOKEN = os.getenv('TG_TOKEN')
URL = f'https://api.telegram.org/bot{TOKEN}'


def get_chat_info(channel_id):
    params = {'chat_id': channel_id}
    response = requests.post(f'{URL}/getChat', json=params)
    if response.status_code == 200:
        response_json = response.json()
        if response_json.get('ok'):
            result = response_json['result']
            pinned_message = result.get('pinned_message', {}).get('text', '')
            return {
                'title': result['title'],
                'short_description': result['description'],
                'description': pinned_message,
            }


def link2channel_id(link):
    if link.startswith('@'):
        return link
    
    if link.startswith('https://t.me/') or link.startswith('t.me/'):
        chat_name = link.split('/')[-1]
        return f'@{chat_name}'


consumer = KafkaConsumer('my_favorite_topic')
for message in consumer:
    data = json.loads(message)
    channel_id = link2channel_id(data['link'])
    data = get_chat_info(channel_id)
    print(message, data)
