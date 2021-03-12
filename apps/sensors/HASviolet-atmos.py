#!/usr/bin/python3
#
# HASviolet Sensors - Atmosphere
#
# 20200804-2134
#
#  Usage: HASviolet-atomos.py -d destination-node
#
#  OPTIONS
#
#
#

import qwiic_bme280
import io
import serial
import time
import sys
import board
from digitalio import DigitalInOut, Direction, Pull
import busio
import signal
from HASvioletRF import HASrf
from HASvioletHID import HAShid
import argparse 
import configparser


#
# OBJECTS
#

HASit = HASrf()
HAShat = HAShid()


#
# IMPORT ARGS
#

parser = argparse.ArgumentParser(description='HASviolet Atmos TX')
parser.add_argument('-d', '--destination', help='Destination', default='BEACON-99')
args = vars(parser.parse_args())


#
# VARIABLES
#

hasvrecipient = args['destination']
#message = args['message']
hasvheader = HASit.mystation + ">" + hasvrecipient


#
# FUNCTIONS
#

def sigs_handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    HASit.cleanup()
    HAShat.OLED.fill(0)
    HAShat.OLED.show()
    HAShat.OLED.text('Goodbye...', 0, 10, 1)
    HAShat.OLED.show()
    time.sleep(2)
    HAShat.OLED.fill(0)
    HAShat.OLED.show()
    exit(0)

def rx_oled_scroll(self):
    HAShat.OLED.fill(0)
    HAShat.OLED.show()
    HASit.ppayload = HASit.receive_ascii.split("|")
    HAShat.OLED.fill(0)
    HAShat.OLED.show()
    HAShat.OLED.text(HASit.ppayload[0], 0, 1, 1)
    HAShat.OLED.text("RSSI: " + HASit.receive_rssi, 0, 9, 1)
    HAShat.OLED.text(HASit.ppayload[1], 0, 17, 1)
    HAShat.OLED.show()

def tx_payload(payload):
    hasvpayload = hasvheader + " | " + payload
    HASit.transmit(hasvpayload)
    time.sleep(1)
    return (hasvpayload)

def sensor_atmosphere():
    mySensor = qwiic.QwiicBme280()
    if mySensor.connected == False:
        print("The Qwiic BME280 device isn't connected to the system. Please check your connection")
    mySensor.begin()
    message = str(mySensor.temperature_fahrenheit) + ":" + str(mySensor.humidity) + ":" + str(mySensor.pressure)
    return (message)


#
# SETUP
#

HAShat.logo('hvdn-logo.xbm')
apayload = ""

# CTRL-C is SIGINT and closes program gracefully
signal.signal(signal.SIGINT, sigs_handler)


#
# MAIN
#

while True:
    apayload = sensor_atmosphere()
    haspayload = tx_payload(str(apayload))
    print(haspayload)
    #rx_oled_scroll(haspayload)
    apayload = ""