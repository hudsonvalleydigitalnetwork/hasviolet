#!/usr/bin/python3
#
# HASviolet TX Lib Atmo
#
#
#  Usage: HASviolet-tx_BME280.py -d destination-node 
#
#  OPTIONS
#       destination-node is LoRa Node Number ID destination
#       Qwiic BME280 Atmospheric Data sent
#
#
#  RELEASE: BERMUDA
#
#

from __future__ import print_function
import qwiic_bme280
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

mySensor = qwiic_bme280.QwiicBme280()
if mySensor.connected == False:
    print("The Qwiic BME280 device isn't connected to the system. Please check your connection")
mySensor.begin()

#        print("Humidity:\t%.3f" % mySensor.humidity)
#        print("Pressure:\t%.3f" % mySensor.pressure)	
#        print("Altitude:\t%.3f" % mySensor.altitude_feet)
#        print("Temperature:\t%.2f" % mySensor.temperature_fahrenheit)		
#        print("")

# Send message
message = str(mySensor.temperature_fahrenheit) + ":" + str(mySensor.humidity) + ":" + str(mySensor.pressure)
hasvpayload = hasvheader + " | " + message 
HASit.tx(hasvpayload)
print(hasvpayload)
HASit.cleanup()

