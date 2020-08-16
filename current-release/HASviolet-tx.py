#!/usr/bin/python3
#
# HASviolet TX
#
# 20200804-2134
#
#  Usage: HASviolet-tx.py destination-node "message"
#
#  OPTIONS
#       destination-node is LoRa Node Number ID destination
#       MESSAGE is sent in double quotes
#
#
#  RELEASE: BERMUDA
#
#


#
# Import Libraries
#

import argparse 
import configparser
import curses
import signal
import sys
import time
from HASvioletRF import HASrf
from HASvioletHID import HAShid

#
# Initialise HASviolet
#

HASit = HASrf()
HAShat = HAShid()


#
# IMPORT ARGS
#

parser = argparse.ArgumentParser(description='HASviolet TX')
parser.add_argument('-d','--destination', help='Destination', default='BEACON-99')
parser.add_argument('-m','--message', help='Message in quotes', required=True)
args = vars(parser.parse_args())


#
# VARIABLES
#

# hasvrecipient - Address of receiving node
# hasvname - mycall + "-" + ssid
# hasvheader - hasname + ">" + hasvrecipient
# hasvpayload - header + message

hasvrecipient = args['destination']
message = args['message']
hasvheader = HASit.mystation + ">" + hasvrecipient
hasvpayload = hasvheader + " | " + message 


#
# FUNCTIONS
#

def sigs_handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    HASit.cleanup()
    HAShat.OLED.text('Goodbye...', 0, 10, 1)
    HAShat.OLED.show()
    time.sleep(2)
    HAShat.OLED.fill(0)
    HAShat.OLED.show()
    exit(0)


#
# SETUP
#

HAShat.logo('hvdn-logo.xbm')

# SIGTINT aka control-C is quit
signal.signal(signal.SIGINT, sigs_handler)


#
# MAIN
#

# Send message
HASit.tx(hasvpayload)
#rf95.send(rf95.str_to_data(hasvpayload))
#rf95.wait_packet_sent()

print(hasvpayload)

HAShat.OLED.fill(0)
HAShat.OLED.text(hasvheader, 0, 1, 1)
HAShat.OLED.text(message, 0, 9, 1)
HAShat.OLED.show()

time.sleep(5)

HAShat.OLED.fill(0)
HAShat.OLED.show()
HASit.cleanup()