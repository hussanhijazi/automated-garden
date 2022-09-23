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
    """
        Prints a mqtt message to stdout ( used as callback for subscribe )

        :param client: the client itself
        :param userdata: userdata is set when initiating the client, here it is userdata=None
        :param msg: the message with topic and payload
    """
    global soil_value, temp_value, humidity_value, rain_value, water_status
    print(msg.topic + " - " + str(msg.qos) + " - " + str(msg.payload))
    value = msg.payload.decode('ASCII')

    if msg.topic == topic_soil.decode('ASCII'):
        soil_value = float(value)
    elif msg.topic == topic_rain.decode('ASCII'):
        rain_value = float(value)
    elif msg.topic == topic_temp.decode('ASCII'):
        temp_value = float(value)
    elif msg.topic == topic_humidity.decode('ASCII'):
        humidity_value = float(value)

    topic = msg.topic.replace('/', '-')
    timestamp = time.time()

    firebase.save(topic, {
        'timestamp': timestamp,
        'value': value
    })

    if not water_status:
        if soil_value > water_threshold:
            water_status = True
            client.publish(topic_water.decode('ASCII'), b'on')
    else:
        if soil_value <= water_threshold:
            water_status = False
            client.publish(topic_water.decode('ASCII'), b'off')


mqtt_client.on_subscribe = on_subscribe
mqtt_client.on_message = on_message
mqtt_client.on_publish = on_publish

mqtt_client.subscribe(topic_soil.decode('ASCII'), qos=1)
mqtt_client.subscribe(topic_temp.decode('ASCII'), qos=1)
mqtt_client.subscribe(topic_humidity.decode('ASCII'), qos=1)
mqtt_client.subscribe(topic_rain.decode('ASCII'), qos=1)

mqtt_client.loop_forever()
