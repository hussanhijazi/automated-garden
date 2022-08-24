import machine
import network
import ubinascii
import file

def connect():              
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        data = file.get_wifi_password()
        if data != "":
            print('connecting to network...', data[0])
            sta_if.active(True)
            sta_if.connect(data[0], data[1])
            while not sta_if.isconnected():
                pass
    print('network config:', sta_if.ifconfig())
    print('network config:', sta_if.ifconfig())
    if sta_if.ifconfig()[0] == "0.0.0.0":
        return False
    return True


def getMacAddress():
    mac = ubinascii.hexlify(network.WLAN().config('mac'), ':').decode()
    return mac


def access_point():
    ap = network.WLAN(network.AP_IF)
    ap.active()
    WIFI_NAME = 'espcoffee'
    WIFI_PASSWORD = 'esp1234567890'
    ap.config(essid=WIFI_NAME, password=WIFI_PASSWORD)
    print('Connect to ', WIFI_NAME, ' network with password', WIFI_PASSWORD, ' and access: http://' +
          ap.ifconfig()[0], " in you browser")


def get_networks():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    return wlan.scan()
