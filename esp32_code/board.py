import network
import ubinascii


def get_mac_address():
    mac = ubinascii.hexlify(network.WLAN().config('mac'), ':').decode()
    return mac


def topic_factory_composer(args):
    topics = []
    for i in range(len(args)):
        topic = args[i]
        topic_composition = (get_mac_address(), '/', topic)
        agglutinate = ''
        topics.append(agglutinate.join(topic_composition))
    return topics
