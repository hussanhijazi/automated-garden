from machine import Pin
from time import sleep

relay = Pin(26, Pin.OUT)

def status(state):
    relay.value(state)