import dht
from machine import Pin
import umqtt_client
from config import topic_temp
from config import topic_humidity

pin = 33

sensor = dht.DHT11(Pin(pin))

def publish_mqtt():
    sensor.measure()
    print('--------------------------')
    print('Temperature: %.2f' %sensor.temperature())
    print('Humidity: %.2f' %sensor.humidity())
    umqtt_client.publish(topic_temp, str(sensor.temperature()))
    umqtt_client.publish(topic_humidity, str(sensor.humidity()))
