import json

from machine import Pin, ADC

import umqtt_client
from config import max_moisture
from config import min_moisture
from config import topic_rain

pin = 32


def publish_mqtt(timestamp):
    pot = ADC(Pin(pin))
    pot.atten(ADC.ATTN_11DB)
    pot.width(ADC.WIDTH_10BIT)

    # pot_value = pot.read()
    moisture = (pot.read()) * 100 / (max_moisture - min_moisture)
    # print('Rain:', str(pot_value))
    print("Rain sensor: " + "%.2f" % moisture + "% (adc: " + str(pot.read()) + ")")
    umqtt_client.publish(topic_rain, json.dumps({'timestamp': timestamp, 'value': str(moisture)}))
