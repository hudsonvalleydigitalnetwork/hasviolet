#!/usr/bin/python3
#
# HASviolet TX UBLOCK7 GPS
#
#
#  Usage: HASviolet-tx_UBLOCK7.py -d destination-node 
#
#  OPTIONS
#       destination-node is LoRa Node Number ID destination
#       u-blox 7 Receiver GPS Data sent
#
#       https://www.u-blox.com/sites/default/files/ublox7-FW1.01_ReleaseNote_%28UBX-13003009%29.pdf
#
#
# TO-DO:
#
#

from __future__ import print_function
import io
import pynmea2
import serial
import time
import sys

import argparse 
import board
import busio
import signal
import configparser
from digitalio import DigitalInOut, Direction, Pull
from HASvioletRF import HASrf
from HASvioletHID import HAShid


#
# FUNCTIONS
#
# IMPORT CONFIG AND INITIALIZE RADIO
#

HASit = HASrf()
HAShat = HAShid()


#
# IMPORT ARGS
#

parser = argparse.ArgumentParser(description='HASviolet Sensor TX')
parser.add_argument('-d','--destination', help='Destination Name-Call', required=True)
#parser.add_argument('-m','--message', help='Message to be sent in quotes', required=True)
args = vars(parser.parse_args())


#
# VARIABLES
#

# hasvrecipient - Address of receiving node
# hasvname - mycall + "-" + ssid
# hasvheader - hasname + ">" + hasvrecipient
# hasvpayload - header + message

hasvrecipient = args['destination']
#message = args['message']
hasvheader = HASit.station + ">" + hasvrecipient


#
# FUNCTIONS
#

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=5.0)
sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))

try:
    line = sio.readline()
    message = pynmea2.parse(line)
    print(repr(message))
except serial.SerialException as e:
    print('Device error: {}'.format(e))
#    break
except pynmea2.ParseError as e:
    print('Parse error: {}'.format(e))
#    continue 

# Send message
#message = str(mySensor.temperature_fahrenheit) + ":" + str(mySensor.humidity) + ":" + str(mySensor.pressure)
hasvpayload = hasvheader + " | " + line
HASit.tx(hasvpayload)
print(hasvpayload)
HASit.cleanup()
