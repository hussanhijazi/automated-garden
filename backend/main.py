import json
import logging
import time
import paho.mqtt.client as paho
import datetime
import firebase as my_firebase
from config import mqtt_config
from config import topic_humidity
from config import topic_rain
from config import topic_soil
from config import topic_temp
from config import topic_water
from config import water_state_collection
from mqtt_client import on_connect
from mqtt_client import on_publish
from mqtt_client import on_subscribe
from presets import check_time

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

firestore_client = my_firebase.connect()
soil_value = 0
temp_value = 0
rain_value = 0
humidity_value = 0
#water_threshold = 55

mqtt_client = paho.Client(mqtt_config['client_id'], userdata=None, protocol=paho.MQTTv5)
mqtt_client.on_connect = on_connect
mqtt_client.connect(mqtt_config['mqtt_broker'], mqtt_config['port'])

water_status = False
def on_message(client, userdata, msg):
    value = msg.payload.decode()
    data = json.loads(value)

    set_value(msg.topic, data['value'])
    save_value(msg.topic, data)

    if msg.topic == topic_soil.decode():
        logging.info(msg.topic + " - " + str(msg.qos) + " - " + str(msg.payload))
        check_water_status(data['timestamp'])
        # time.sleep(0.5)



def check_water_status(timestamp):
    global water_status
    presets = my_firebase.get_presets(firestore_client)

    start = presets[0]["time1"]
    end = presets[0]["time2"]
    soil_humidity = presets[0]["soilHumidity"]

    parts_start = start.split(":")
    parts_end = end.split(":")

    ## TODO Checar se vem vazio os horários
    time_start = datetime.time(int(parts_start[0]), int(parts_start[1]), 0)
    time_end = datetime.time(int(parts_end[0]), int(parts_end[1]), 0)

    start_seconds = check_time(time_start)
    end_seconds = check_time(time_end)

    can_start_time = -0.01 > start_seconds > -1
    can_end_time = -0.01 > end_seconds > -1

    logging.info(str(time_start) + " - Seconds Start: " + str(start_seconds) + " - " + str(can_start_time))
    logging.info(str(time_end) + " - Seconds End: " + str(end_seconds) + " - " + str(can_end_time))
    logging.info("Water status: " + str(water_status))
    logging.info("Actual soil value: " + str(soil_value) + " - Soil trigger: " + str(soil_humidity))
    logging.info("--------------------------------")

    if soil_value >= int(soil_humidity):
        if water_status:
            send_water_status('off', timestamp)
            save_water_status('off', timestamp)
            my_firebase.send_notification(firestore_client, "Automated Garden", "Irrigação desligada com sucesso...")
            water_status = False
    else:
        if (can_start_time or can_end_time) and water_status == False:
            send_water_status('on', timestamp)
            save_water_status('on', timestamp)
            my_firebase.send_notification(firestore_client, "Automated Garden", "Irrigação ligada com sucesso...")
            water_status = True

def send_water_status(status, timestamp):
    mqtt_client.publish(topic_water.decode(), status.encode())
    logging.info('Water State - ' + str(status) + ' - ' + str(timestamp))
    #firebase.send_notification('{TOKEN}', status)


def save_water_status(state, timestamp):
    # firebase.save('water_state', {
    #     'timestamp': timestamp,
    #     'state': state
    # })
    my_firebase.save_firestore(firestore_client, water_state_collection, {
        'timestamp': timestamp,
        'state': state
    })


def save_value(topic, data):
    topic = topic.replace('/', '_')
    my_firebase.save_firestore(firestore_client, topic, {
        'timestamp': data['timestamp'],
        'value': data['value']
    })

def set_value(topic, value):
    global soil_value, rain_value, temp_value, humidity_value
    if topic == topic_soil.decode():
        soil_value = float(value)
    elif topic == topic_rain.decode():
        rain_value = float(value)
    elif topic == topic_temp.decode():
        temp_value = float(value)
    elif topic == topic_humidity.decode():
        humidity_value = float(value)


mqtt_client.on_subscribe = on_subscribe
mqtt_client.on_message = on_message
mqtt_client.on_publish = on_publish

mqtt_client.subscribe(topic_soil.decode(), qos=1)
mqtt_client.subscribe(topic_temp.decode(), qos=1)
mqtt_client.subscribe(topic_humidity.decode(), qos=1)
mqtt_client.subscribe(topic_rain.decode(), qos=1)

mqtt_client.loop_forever()
