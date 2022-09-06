import network
import ubinascii
from wifi import getMacAddress

topic_sub = ['soil_sensor']

def get_mac_address():
    mac = ubinascii.hexlify(network.WLAN().config('mac'), ':').decode()
    return mac


def factory_topic_sub():
    topics_sub = factory_topic_composer(topic_sub)
    return topics_sub


def factory_topic_composer(args):
    topic = []
    topics = []
    for i in range(len(args)):
        topic = args[i]
        topic_composition = (get_mac_address(), '/', topic)
        agglutinate = ''
        topics.append(agglutinate.join(topic_composition))
    return topics
