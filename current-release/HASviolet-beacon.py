#!/usr/bin/python3
#
# HASviolet BEACON
#
# 20200804-2134
#
#  Usage: HASviolet-beacon.py -c COUNT -t DELAY "message"
#
#  OPTIONS
#           -c Number of times to repeat MESSAGE
#           -t NUmber of seconds before repeat MESSAGE
#             MESSAGE is sent in double quotes
#
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

parser = argparse.ArgumentParser(description='HASviolet Beacon')
parser.add_argument('-c','--count', type=int, help='number of times to repeat the message', required=True)
parser.add_argument('-t','--time', type=int, help='number of seconds between repeating message', required=True)
parser.add_argument('-m','--message', help='Message to send in quotes. Default from INI file', default=HASit.mybeacon)

args = vars(parser.parse_args())

bcount = args['count']
message = args['message']
timedelay = args['time']

#
# VARIABLES
#

hasvrecipient = "BEACON-99"
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

reprinse=0


while bcount > reprinse:
    reprinse = reprinse + 1
    HASit.tx(hasvpayload)
    print(hasvpayload)
    HAShat.OLED.fill(0)
    HAShat.OLED.text("Sending Count " + str(reprinse), 0, 1, 1)
    HAShat.OLED.text(hasvheader, 0, 9, 1)
    HAShat.OLED.text(message, 0, 17, 1)
    HAShat.OLED.show()

    time.sleep(timedelay)

print ("Closing ...")

HAShat.OLED.fill(0)
HAShat.OLED.show()
HASit.cleanup()
