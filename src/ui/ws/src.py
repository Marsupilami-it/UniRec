import asyncio
import json
import os
import re

from dotenv import load_dotenv
from websockets.asyncio.server import ServerConnection, serve
from websockets.exceptions import ConnectionClosedOK, ConnectionClosedError

load_dotenv()

WS_SERVER_PORT = os.getenv('WS_SERVER_PORT')

async def send_to_browser(websocket, what, data):
    await websocket.send(json.dumps({what: data}))


def send_to_broker(topic, data):
    pass


def get_from_broker(topic):
    return


async def view_start_process(websocket):
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
                    
                    send_to_broker(f'api-adapter-{adapter_code}', {'link': link})

                    # card = {'title': 'Their title', 'description': 'Their description', 'short_description': 'Their description', 'count_members': 10, 'is_mine': True}
                    # await send_to_browser(websocket, 'card', card)
        except ConnectionClosedOK as _:
            break
        except ConnectionClosedError as _:
            break
        except Exception as error:
            raise error

        card = get_from_broker(f'api-adapters-output')
        # card = {'title': 'Their title', 'description': 'Their description', 'short_description': 'Their description', 'count_members': 10, 'is_mine': True}
        await send_to_browser(websocket, 'card', card)


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


if __name__ == "__main__":
    asyncio.run(main(WS_SERVER_PORT))
