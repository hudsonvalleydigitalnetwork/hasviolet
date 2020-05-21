#!/usr/bin/python3
#
# HASviolet Sensors
#
#
#  Usage: HASviolet-sensors.py -d destination-node -s sensor
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

parser = argparse.ArgumentParser(description='HASviolet Sensor TX')
parser.add_argument('-d', '--destination', help='Destination', default='BEACON-99')
parser.add_argument('-a', '--atmosphere', help='Atmosphere Sensor', action='store_true')
parser.add_argument('-f', '--distance', help='Distance Sensor', action='store_true')
parser.add_argument('-g', '--gps', help='GPS Sensor', action='store_true')
args = vars(parser.parse_args())


#bcount = args['count']
#message = args['message']
#timedelay = args['time']


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

def sensor_distance():
    ToF = qwiic.QwiicVL53L1X()
    if (ToF.sensor_init() == None):
        print("Sensor online!\n")
    try:
        ToF.start_ranging()
        time.sleep(.005)
        distance = ToF.get_distance()
        time.sleep(.005)
        ToF.stop_ranging()
        distanceInches = distance / 25.4
        distanceFeet = distanceInches / 12.0
        hasvpayload = str(distanceFeet)
        print("Distance(mm): %s Distance(ft): %s" % (distance, distanceFeet))
        return (hasvpayload)
    except Exception as e:
        print(e)
        HASit.cleanup()

def sensor_atmosphere():
    mySensor = qwiic.QwiicBme280()
    if mySensor.connected == False:
        print("The Qwiic BME280 device isn't connected to the system. Please check your connection")
    mySensor.begin()
    message = str(mySensor.temperature_fahrenheit) + ":" + str(mySensor.humidity) + ":" + str(mySensor.pressure)
    return (message)


def sensor_gps():
    try:
        line = sio.readline()
        message = pynmea2.parse(line)
        print(repr(message))
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
apayload = ""
dpayload = ""

# CTRL-C is SIGINT and closes program gracefully
signal.signal(signal.SIGINT, sigs_handler)

#
# MAIN
#

while True:
    if args['gps'] == True:
        gpayload = sensor_gps()
        haspayload = tx_payload(str(gpayload))
        print(haspayload)
        #rx_oled_scroll(haspayload)

    if args['atmosphere'] == True:
        apayload = sensor_atmosphere()
        haspayload = tx_payload(str(apayload))
        print(haspayload)
        # rx_oled_scroll(haspayload)

    if args['distance'] == True:
        dpayload = sensor_distance()
        haspayload = tx_payload(str(dpayload))
        print(haspayload)
        #rx_oled_scroll(haspayload)
    gpayload = ""
    apayload = ""
    dpayload = ""