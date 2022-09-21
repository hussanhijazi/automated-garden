import paho.mqtt.client as paho
from mqtt_client import CONFIG
from mqtt_client import on_connect
from mqtt_client import on_message
from mqtt_client import on_publish
from mqtt_client import on_subscribe

client = paho.Client(CONFIG['CLIENT_ID'], userdata=None, protocol=paho.MQTTv5)
client.on_connect = on_connect
client.connect(CONFIG['MQTT_BROKER'], 1883)

client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_publish = on_publish

client.subscribe('ifpr/rain_sensor')
client.subscribe('ifpr/temp_sensor')
client.subscribe('ifpr/soil_sensor')

client.loop_forever()
