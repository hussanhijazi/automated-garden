import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import firestore
from firebase_admin import messaging
from config import water_state_collection

databaseURL = "https://automated-garden-d403e-default-rtdb.firebaseio.com/"


def connect():
    cred = credentials.Certificate("firebase.json")
    firebase_admin.initialize_app(cred, {
        "databaseURL": databaseURL
    })
    return firestore.client()


def save_realtime_db(topic, values):
    ref = db.reference(topic)
    ref.push().set(values)


def save_firestore(client, collection, data):
    doc_ref = client.collection(collection).document(str(data["timestamp"]))
    doc_ref.set(data)


def send_notification(registration_token, status):
    message = messaging.Message(
        data={"status": status},
        token=registration_token,
    )

    response = messaging.send(message)

    print("Successfully sent message:", response)


def actual_water_state(client):
    water_state_collection_ref = client.collection(water_state_collection)
    try:
        w = water_state_collection_ref.order_by("timestamp", direction=firestore.Query.DESCENDING).limit(1)
    except:
        return "off"

    if len(w.get()):
        water_status = w.get()[0].to_dict()["state"]
        print(w.get()[0].to_dict())
        return water_status

    return "off"


def get_temperature(client, collection, limit):
    temp_collection_ref = client.collection(collection)
    try:
        w = temp_collection_ref.order_by("timestamp", direction=firestore.Query.DESCENDING).limit(limit)
        my_dict = [{el.id: {"value": el.to_dict()["value"]} for el in w.get()}]
        return my_dict
    except Exception as e:
        print(e)
        return "off"


def delete_temperature(client, collection, timestamp):
    client.collection(collection).document(str(timestamp)).delete()
