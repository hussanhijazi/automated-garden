import time

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
import logging

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

firebase.connect()

mqtt_client = paho.Client(mqtt_config['client_id'], userdata=None, protocol=paho.MQTTv5)
mqtt_client.on_connect = on_connect
mqtt_client.connect(mqtt_config['mqtt_broker'], mqtt_config['port'])


def on_message(client, userdata, msg):
    logging.info(msg.topic + " - " + str(msg.qos) + " - " + str(msg.payload))
    value = msg.payload.decode('ASCII')

    set_value(msg.topic, value)

    save_value(msg.topic, value)

    check_status()


def check_status():
    global water_status
    if not water_status:
        if soil_value > water_threshold:
            water_status = True
            set_status('on')
    else:
        if soil_value <= water_threshold:
            water_status = False
            set_status('off')


def set_status(status):
    mqtt_client.publish(topic_water.decode('ASCII'), status.encode())
    save_status(status)
    #firebase.send_notification('{TOKEN}', status)


def save_status(state):
    timestamp = time.time()
    firebase.save('water_state', {
        'timestamp': timestamp,
        'state': state
    })


def save_value(topic, value):
    topic = topic.replace('/', '_')
    timestamp = time.time()
    firebase.save(topic, {
        'timestamp': timestamp,
        'value': value
    })


def set_value(topic, value):
    global soil_value, rain_value, temp_value, humidity_value
    if topic == topic_soil.decode('ASCII'):
        soil_value = float(value)
    elif topic == topic_rain.decode('ASCII'):
        rain_value = float(value)
    elif topic == topic_temp.decode('ASCII'):
        temp_value = float(value)
    elif topic == topic_humidity.decode('ASCII'):
        humidity_value = float(value)


mqtt_client.on_subscribe = on_subscribe
mqtt_client.on_message = on_message
mqtt_client.on_publish = on_publish

mqtt_client.subscribe(topic_soil.decode('ASCII'), qos=1)
mqtt_client.subscribe(topic_temp.decode('ASCII'), qos=1)
mqtt_client.subscribe(topic_humidity.decode('ASCII'), qos=1)
mqtt_client.subscribe(topic_rain.decode('ASCII'), qos=1)

mqtt_client.loop_forever()
