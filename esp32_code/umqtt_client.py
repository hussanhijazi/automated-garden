from umqtt.simple import MQTTClient

from config import mqtt_config

# Create an instance of MQTTClient
client = MQTTClient(mqtt_config['client_id'], mqtt_config['mqtt_broker'],
                    user=mqtt_config['user'], password=mqtt_config['password'], port=mqtt_config['port'],
                    keepalive=mqtt_config['keep_alive'])


# Method to act based on message received

def on_message(topic, msg):
    print("Topic: %s, Message: %s" % (topic, msg))


def init():
    client.set_callback(on_message)
    client.connect()


def publish(topic, msg, qos=1):
    client.publish(topic, msg, qos=qos)


def subscribe(topics):
    for topic in topics:
        client.subscribe(topic)
    print("ESP is Connected to %s in port %s and subscribed to %s topic" %
          (mqtt_config['mqtt_broker'], mqtt_config['port'], topic))


def disconnect():
    client.disconnet()


def check_msg():
    client.check_msg()