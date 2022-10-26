import json

import dht
from machine import Pin

import umqtt_client
from config import topic_humidity
from config import topic_temp

pin = 33

sensor = dht.DHT11(Pin(pin))


def publish_mqtt(timestamp):
    try:
        sensor.measure()
        print('Temperature: %.2f' % sensor.temperature() + '°')
        print('Air Humidity: %.2f' % sensor.humidity() + '%')
        umqtt_client.publish(topic_temp, json.dumps({'timestamp': timestamp, 'value': str(sensor.temperature())}))
        umqtt_client.publish(topic_humidity, json.dumps({'timestamp': timestamp, 'value': str(sensor.humidity())}))
    except:
        print('DHT11 measure error')
    