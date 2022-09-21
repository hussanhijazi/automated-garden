from machine import Pin, ADC
from time import sleep
import mqtt_client

min_moisture = 0
max_moisture = 65535

pin = 34

topic = b'ifpr/soil_sensor'


def subscribe_mqtt():
    pot = ADC(Pin(pin))
    pot.atten(ADC.ATTN_11DB)
    pot.width(ADC.WIDTH_10BIT)

    #    while True:
    pot_value = pot.read()
    moisture = (pot.read_u16()) * 100 / (max_moisture - min_moisture)
    print('Soil Humidity:', str(pot_value))
    print("moisture: " + "%.2f" % moisture + "% (adc: " + str(pot.read_u16()) + ")")
    mqtt_client.publish(topic, str(pot_value))
