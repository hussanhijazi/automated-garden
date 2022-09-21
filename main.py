import server
import wifi
import soil_sensor
import temp_sensor
import rain_sensor
from time import sleep
import umqtt_client
from config import topic_water

is_connected = wifi.connect()

if not is_connected:
    print("not connected...")
    wifi.access_point()
    server.listen()
else:
    print("wifi connected")
    umqtt_client.init()
    umqtt_client.subscribe([topic_water])
    while True:
        temp_sensor.publish_mqtt()
        soil_sensor.publish_mqtt()
        rain_sensor.publish_mqtt()
        umqtt_client.check_msg()
        sleep(5)

    umqtt_client.disconnect()