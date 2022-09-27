import json
import logging

import paho.mqtt.client as paho

import firebase
from config import mqtt_config
from config import topic_humidity
from config import topic_rain
from config import topic_soil
from config import topic_temp
from config import topic_water
from mqtt_client import on_connect
from mqtt_client import on_publish
from mqtt_client import on_subscribe

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

soil_value = 0
temp_value = 0
rain_value = 0
humidity_value = 0
water_status = False
water_threshold = 55

firestore_client = firebase.connect()

mqtt_client = paho.Client(mqtt_config['client_id'], userdata=None, protocol=paho.MQTTv5)
mqtt_client.on_connect = on_connect
mqtt_client.connect(mqtt_config['mqtt_broker'], mqtt_config['port'])


def on_message(client, userdata, msg):
    logging.info(msg.topic + " - " + str(msg.qos) + " - " + str(msg.payload))
    value = msg.payload.decode()
    data = json.loads(value)

    set_value(msg.topic, data['value'])

    save_value(msg.topic, data)

    check_status(data['timestamp'])


def check_status(timestamp):
    global water_status
    if not water_status:
        if soil_value > water_threshold:
            water_status = True
            send_status('on', timestamp)
    else:
        if soil_value <= water_threshold:
            water_status = False
            send_status('off', timestamp)


def send_status(status, timestamp):
    mqtt_client.publish(topic_water.decode(), status.encode())
    save_status(status, timestamp)
    # firebase.send_notification('{TOKEN}', status)


def save_status(state, timestamp):
    # firebase.save('water_state', {
    #     'timestamp': timestamp,
    #     'state': state
    # })
    firebase.save_firestore(firestore_client, 'water_state', {
        'timestamp': timestamp,
        'state': state
    })


def save_value(topic, data):
    topic = topic.replace('/', '_')
    firebase.save_firestore(firestore_client, topic, {
        'timestamp': data['timestamp'],
        'value': data['value']
    })
    # firebase.save(topic, {
    #     'timestamp': timestamp,
    #     'value': value
    # })


def set_value(topic, value):
    global soil_value, rain_value, temp_value, humidity_value
    if topic == topic_soil.decode():
        soil_value = float(value)
    elif topic == topic_rain.decode():
        rain_value = float(value)
    elif topic == topic_temp.decode():
        temp_value = float(value)
    elif topic == topic_humidity.decode():
        humidity_value = float(value)


mqtt_client.on_subscribe = on_subscribe
mqtt_client.on_message = on_message
mqtt_client.on_publish = on_publish

mqtt_client.subscribe(topic_soil.decode(), qos=1)
mqtt_client.subscribe(topic_temp.decode(), qos=1)
mqtt_client.subscribe(topic_humidity.decode(), qos=1)
mqtt_client.subscribe(topic_rain.decode(), qos=1)

mqtt_client.loop_forever()
