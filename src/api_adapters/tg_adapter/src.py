import json
import os

import requests
from dotenv import load_dotenv
from kafka import KafkaConsumer

load_dotenv()

TOKEN = os.getenv('TG_TOKEN')
URL = f'https://api.telegram.org/bot{TOKEN}'


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

    return data

def link2channel_id(link):
    if link.startswith('@'):
        return link
    
    if link.startswith('https://t.me/') or link.startswith('t.me/'):
        chat_name = link.split('/')[-1]
        return f'@{chat_name}'


# Not for production >>>>>>>>
#chat_id = link2channel_id('https://t.me/it_syeysk')
chat_id = link2channel_id('@it_syeysk')
#print(chat_id)
data = get_chat_info(chat_id)
print(data)
exit()
# <<<<<<<<<


consumer = KafkaConsumer(bootstrap_servers='10.2.0.244:9093')

for message in consumer:
    data = json.loads(message)
    channel_id = link2channel_id(data['link'])
    data = get_chat_info(channel_id)
    print(message, data)
