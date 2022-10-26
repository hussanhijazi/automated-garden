from time import sleep

import network
import ubinascii

import file


def connect():
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        retry = 0
        data = file.get_wifi_password()
        if data != '':
            print('Connecting to network', data[0], end='')
            sta_if.active(True)
            sta_if.connect(data[0], data[1])
            while not sta_if.isconnected():
                if retry < 15:
                    retry = retry + 1
                    sleep(0.5)
                    print('.', end='')
                    pass
                else:
                    break
    print('')
    print('Wifi network config: ', sta_if.ifconfig())
    if sta_if.ifconfig()[0] == "0.0.0.0":
        sta_if.active(False)
        return False
    return True


def get_mac_address():
    mac = ubinascii.hexlify(network.WLAN().config('mac'), ':').decode()
    return mac


def access_point():
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    print('Access Point active:', ap.active())
    wifi_name = 'automated-garden'
    wifi_password = 'esp1234567890'
    ap.config(essid=wifi_name,
              authmode=network.AUTH_WPA_WPA2_PSK, password=wifi_password)
    print('Connect to ', wifi_name, ' network with password', wifi_password, ' and access: http://' +
          ap.ifconfig()[0], " in you browser")


def get_networks():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    return wlan.scan()
