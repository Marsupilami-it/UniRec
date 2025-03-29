import json
import os

import requests
from dotenv import load_dotenv
from kafka import KafkaConsumer

load_dotenv()

TOKEN = os.getenv('TG_TOKEN')
URL = f'https://api.telegram.org/bot{TOKEN}'


def get_chat_info(channel_id):
    data = {}

    params = {'chat_id': channel_id}
    response = requests.post(f'{URL}/getChat', json=params)
    if response.status_code == 200:
        response_json = response.json()
        if response_json.get('ok'):
            result = response_json['result']
            data['title'] = result['title']
            data['short_description'] = result['description']
            data['description'] = result.get('pinned_message', {}).get('text', '')

    params = {'chat_id': channel_id}
    response = requests.post(f'{URL}/getChatMemberCount', json=params)
    if response.status_code == 200:
        response_json = response.json()
        if response_json.get('ok'):
            data['count_members'] = response_json['result']

    return data

def link2channel_id(link):
    if link.startswith('@'):
        return link
    
    if link.startswith('https://t.me/') or link.startswith('t.me/'):
        chat_name = link.split('/')[-1]
        return f'@{chat_name}'


# Not for production >>>>>>>>
chat_id = link2channel_id('https://t.me/it_syeysk')
#chat_id = link2channel_id('@it_syeysk')
print(chat_id)
data = get_chat_info(chat_id)
print(data)
exit()
# <<<<<<<<<


consumer = KafkaConsumer('my_favorite_topic')
for message in consumer:
    data = json.loads(message)
    channel_id = link2channel_id(data['link'])
    data = get_chat_info(channel_id)
    print(message, data)
