#!/usr/bin/python3
#
# HASviolet Sensors - GPS
#
#
#  Usage: HASviolet-gps.py -d destination-node
#
#  OPTIONS
#
#
#  RELEASE: BERMUDA
#
#

import qwiic
import io
import serial
import time
import sys
import board
from digitalio import DigitalInOut, Direction, Pull
import busio
import signal
import pynmea2
from HASvioletRF import HASrf
from HASvioletHID import HAShid
import argparse 
import configparser


#
# OBJECTS
#

HASit = HASrf()
HAShat = HAShid()
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=0.5)
sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))


#
# IMPORT ARGS
#

parser = argparse.ArgumentParser(description='HASviolet GPS TX')
parser.add_argument('-d', '--destination', help='Destination', default='BEACON-99')
args = vars(parser.parse_args())


#
# VARIABLES
#

hasvrecipient = args['destination']
hasvheader = HASit.station + ">" + hasvrecipient


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
    HASit.tx(hasvpayload)
    time.sleep(1)
    return (hasvpayload)

def sensor_gps():
    try:
        line = sio.readline()
        message = pynmea2.parse(line)
        #print(repr(message))
        return (repr(message))
    except serial.SerialException as e:
        print('Device error: {}'.format(e))
#    break
    except pynmea2.ParseError as e:
        print('Parse error: {}'.format(e))
#    continue 


#
# SETUP
#

HAShat.logo('hvdn-logo.xbm')
gpayload = ""

# CTRL-C is SIGINT and closes program gracefully
signal.signal(signal.SIGINT, sigs_handler)

#
# MAIN
#

while True:
    gpayload = sensor_gps()
    haspayload = tx_payload(str(gpayload))
    print(haspayload)
    #rx_oled_scroll(haspayload)
    gpayload = ""
    