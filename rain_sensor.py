from machine import Pin, ADC
from time import sleep
import mqtt_client

min_moisture = 0
max_moisture = 65535

pin = 32

topic = b'ifpr/rain_sensor'


def subscribe_mqtt():
    pot = ADC(Pin(pin))
    pot.atten(ADC.ATTN_11DB)
    pot.width(ADC.WIDTH_10BIT)

    pot_value = pot.read()
    moisture = (pot.read_u16()) * 100 / (max_moisture - min_moisture)
    print('Rain:', str(pot_value))
    print("Rain2: " + "%.2f" % moisture + "% (adc: " + str(pot.read_u16()) + ")")
    mqtt_client.publish(topic, str(pot_value))
