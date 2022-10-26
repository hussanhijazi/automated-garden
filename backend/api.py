from fastapi import FastAPI
import firebase as my_firebase
from config import topic_temp
from pydantic import BaseModel

app = FastAPI()

firestore_client = my_firebase.connect()

collection = topic_temp.decode().replace('/', '_')


class Temparature(BaseModel):
    value: str
    timestamp: int


@app.get("/temperaturas")
async def temperaturas(limit: int = 10):
    a = my_firebase.get_temperature(firestore_client, collection, limit)
    return a


@app.post("/temperaturas")
async def temparaturas(temp: Temparature):
    my_firebase.save_firestore(firestore_client, collection, {
        'timestamp': temp.timestamp,
        'value': temp.value
    })


@app.delete("/temperaturas/{timestamp}")
def delete_book(timestamp: int) -> None:
    topic = topic_temp.decode().replace('/', '_')
    my_firebase.delete_temperature(firestore_client, topic, timestamp)
