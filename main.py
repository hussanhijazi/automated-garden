import server
import wifi
import soil_sensor
import temp_sensor
from time import sleep
import mqtt_client

is_connected = wifi.connect()

if not is_connected:
    print("not connected...")
    wifi.access_point()
    server.listen()
else:
    print("connected wifi")
    mqtt_client.init()
    while True:
        temp_sensor.subscribe_mqtt()
        soil_sensor.subscribe_mqtt()
        sleep(5)

