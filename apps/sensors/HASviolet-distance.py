#!/usr/bin/python3
#
# HASviolet Sensors - Distance
#
# 20200804-2134
#
#  Usage: HASviolet-distance.py -d destination-node
#
#  OPTIONS
#
#
#  RELEASE: BERMUDA
#
#

import qwiic_vl53l1x
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

parser = argparse.ArgumentParser(description='HASviolet Distance TX')
parser.add_argument('-d', '--destination', help='Destination', default='BEACON-99')
args = vars(parser.parse_args())


#
# VARIABLES
#

hasvrecipient = args['destination']
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

def sensor_distance():
    ToF = qwiic.QwiicVL53L1X()
    if (ToF.sensor_init() == None):
        pass
    try:
        ToF.start_ranging()
        time.sleep(.005)
        distance = ToF.get_distance()
        time.sleep(.005)
        ToF.stop_ranging()
        distanceInches = distance / 25.4
        distanceFeet = distanceInches / 12.0
        hasvpayload = str(distanceFeet)
        #print("Distance(mm): %s Distance(ft): %s" % (distance, distanceFeet))
        return (hasvpayload)
    except Exception as e:
        print(e)
        HASit.cleanup()


#
# SETUP
#

HAShat.logo('hvdn-logo.xbm')
dpayload = ""

# CTRL-C is SIGINT and closes program gracefully
signal.signal(signal.SIGINT, sigs_handler)

#
# MAIN
#

while True:
    dpayload = sensor_distance()
    haspayload = tx_payload(str(dpayload))
    print(haspayload)
    #rx_oled_scroll(haspayload)
    dpayload = ""