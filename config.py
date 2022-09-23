import machine
import ubinascii

min_moisture = 0
max_moisture = 1023

topic_temp = b'ifpr/temp_sensor'
topic_humidity = b'ifpr/humidity_sensor'
topic_soil = b'ifpr/soil_sensor'
topic_rain = b'ifpr/rain_sensor'

topic_water = b'ifpr/water_control'

mqtt_broker = 'broker.hivemq.com'

mqtt_config = {
    'mqtt_broker': mqtt_broker,
    'user': '',
    'password': '',
    'port': 1883,
    'keep_alive': 30,
    # unique identifier of the chip
    'client_id': b'automated-garden' + ubinascii.hexlify(machine.unique_id())
}
