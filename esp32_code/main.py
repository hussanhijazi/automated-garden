from time import sleep

import rain_sensor
import server
import soil_sensor
import temp_sensor
import umqtt_client
import wifi
import relay
from config import topic_water
from ntp_time import get_ntp_time

is_connected = wifi.connect()
publish_time = 5

def on_message(topic, msg):
    if msg == b"off":
        relay.status(0)
    else:
        relay.status(1)


if not is_connected:
    print("Wifi not connected...")
    wifi.access_point()
    server.listen()
else:
    print("Wifi connected...")
    client = umqtt_client.init()
    client.set_callback(on_message)
    umqtt_client.subscribe([topic_water])
    count = -1
    while True:
        if count == -1 or count == publish_time:
            timestamp = get_ntp_time()
            print('Timestamp:', str(timestamp))
            #temp_sensor.publish_mqtt(timestamp)
            soil_sensor.publish_mqtt(timestamp)
            #rain_sensor.publish_mqtt(timestamp)
            print('--------------------------')
            count = 0

        umqtt_client.check_msg()
        sleep(1)
        count += 1

    umqtt_client.disconnect()
