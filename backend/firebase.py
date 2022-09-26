import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import messaging

databaseURL = 'https://automated-garden-d403e-default-rtdb.firebaseio.com/'


def connect():
    cred = credentials.Certificate("firebase.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': databaseURL
    })


def save(topic, values):
    ref = db.reference(topic)
    ref.push().set(values)


def send_notification(registration_token, status):
    message = messaging.Message(
        data={'status': status},
        token=registration_token,
    )

    response = messaging.send(message)

    print('Successfully sent message:', response)
