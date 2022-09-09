import dht
from machine import Pin
from time import sleep
import mqtt_client

pin = 33
topic_temp = b"ifpr/temp_sensor"
topic_humidity = b"ifpr/humidity_sensor"

sensor = dht.DHT11(Pin(pin))

def subscribe_mqtt():
    sensor.measure()
    print('--------------------------')
    print('Temperature: %.2f' %sensor.temperature())
    print('Humidity: %.2f' %sensor.humidity())
    mqtt_client.publish(topic_temp, str(sensor.temperature()))
    mqtt_client.publish(topic_humidity, str(sensor.humidity()))
