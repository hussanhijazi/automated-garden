import dht
from machine import Pin
from time import sleep
import mqtt_client

pin = 33
sensor = dht.DHT11(Pin(pin))

def subscribe_mqtt():
#    mqtt_client.init()
#    while True:
    sensor.measure()
    print('--------------------------')
    print('Temperature = %.2f' % sensor.temperature())
    print('Humidity = %.2f' % sensor.humidity())
    mqtt_client.publish(b"ifpr/temp_sensor", str(sensor.temperature()))
    mqtt_client.publish(b"ifpr/humidity_sensor", str(sensor.humidity()))
#    sleep(3)
