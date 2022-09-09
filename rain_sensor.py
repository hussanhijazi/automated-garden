from machine import Pin, ADC
from time import sleep
import mqtt_client

pin = 32

topic = b'ifpr/rain_sensor'

def subscribe_mqtt():
    pot = ADC(Pin(pin))
    pot.atten(ADC.ATTN_11DB)
    pot.width(ADC.WIDTH_10BIT)
        
    pot_value = pot.read()
    print('Rain:', str(pot_value))
    mqtt_client.publish(topic, str(pot_value))
