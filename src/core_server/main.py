from fastapi import FastAPI
from pydantic import BaseModel

from api_adapters import tg_adapter
from ml.worker import find_societies_by_link


class Link(BaseModel):
    link: str

app = FastAPI()

@app.post('/process_link/')
def read_item(link_object: Link):
    link = link_object.link
    card_tg = tg_adapter.process(link)
    ml_answer = find_societies_by_link(link)
    card_ml = {'description': ml_answer}
    return [card_tg, card_ml]
