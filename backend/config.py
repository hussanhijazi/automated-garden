min_moisture = 0
max_moisture = 1023

topic_temp = b'ifpr/temp_sensor'
topic_humidity = b'ifpr/humidity_sensor'
topic_soil = b'ifpr/soil_sensor'
topic_rain = b'ifpr/rain_sensor'

topic_water = b'ifpr/water_control'

mqtt_broker = "broker.hivemq.com"

mqtt_config = {
    "mqtt_broker": mqtt_broker,
    "port": 1883,
    "client_id": b"automated-garden"
}
