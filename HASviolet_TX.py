#!/usr/bin/python3
#
# HASviolet TX rf95
#
#
#   USAGE: HASviolet-beacon.py -c COUNT -t DELAY "message"
#
#   OPTIONS
#           -c Number of times to repeat MESSAGE
#           -t NUmber of seconds before repeat MESSAGE
#             MESSAGE is sent in double quotes
#
#   REVISION: 20220714-0200
#
#


#
# Import Libraries
#

import argparse 
import configparser
import signal
import sys
import time
import json
import subprocess
from HASvioletRF import HASrf
from HASvioletHID import HAShid


#
# STATICS
#

HASviolet_RXLOCK = False                                               # True = RX is running
HASviolet_TXLOCK = False                                               # True = TX is running
HASviolet_LOCAL = "/home/pi/hasviolet-local/"                          # Config file is in JSON format
HASviolet_SERVER = HASviolet_LOCAL + "server/"                         # Path to files. Change when Pi
HASviolet_ETC = HASviolet_LOCAL + "etc/"                               # Config file is in JSON format
HASviolet_CONFIG = HASviolet_ETC + "HASviolet.json"                    # Config file is in JSON format
HASviolet_SSL_KEY = HASviolet_ETC + "HASviolet.key"                    # SSL Key
HASviolet_SSL_CRT = HASviolet_ETC + "HASviolet.crt"                    # Cert Key
HASviolet_PWF = HASviolet_ETC + "HASviolet.pwf"                        # Password file  user:hashedpasswd
HASviolet_MSGS = HASviolet_SERVER + "msgs/HASviolet.msgs"              # radio writes msgs received here   
HASviolet_LOGIN = HASviolet_SERVER + "HASviolet_LOGIN.html"
HASviolet_LOGINCSS = HASviolet_SERVER + "HASviolet_LOGIN.css"
HASviolet_INDEX = HASviolet_SERVER + "HASviolet_INDEX.html"
HASviolet_INDEXCSS = HASviolet_SERVER + "HASviolet.css"
HASvioletjs = HASviolet_SERVER + "HASviolet.js"
HVDN_LOGO = HASviolet_ETC + "HVDN_logo.xbm"


#
# VARIABLES
#


#
# Initialise HASviolet
#

HASit = HASrf()
HAShat = HAShid()


#
# IMPORT ARGS
#

parser = argparse.ArgumentParser(description='HASviolet TX')
parser.add_argument('-c','--count', type=int, help='number of times to repeat the message', required=True)
parser.add_argument('-t','--time', type=int, help='number of seconds between repeating message', required=True)
parser.add_argument('-d','--destination', help='Destination', default='BEACON-99')
parser.add_argument('-m','--message', help='Message to send in quotes. Default from INI file', default=HASit.mybeacon)

args = vars(parser.parse_args())

bcount = args['count']
message = args['message']
timedelay = args['time']

#
# VARIABLES
#

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

HAShat.logo(HVDN_LOGO)

# SIGTINT aka control-C is quit
signal.signal(signal.SIGINT, sigs_handler)

# RF and LoRa Config init
HASit.startradio()                       # rf95 library
#HASit.startradio_pyl()                  # pyLoraRFM9x Library

if HASit.modemconfig == "CUSTOM":
    HASit.custommodemconfig()

#
# MAIN
#

reprinse=0


while bcount > reprinse:
    if bcount != 99999:
        reprinse = reprinse + 1
    # Send message
    HASit.transmit(hasvpayload)             # rf95 library
    #HASit.ontransmit(hasvpayload)          # pyLoraRFM9x Library
    print(hasvpayload)
    HAShat.OLED.fill(0)
    HAShat.OLED.text(hasvheader, 0, 1, 1)
    HAShat.OLED.text(message, 0, 9, 1)
    HAShat.OLED.show()
    time.sleep(timedelay)
HAShat.OLED.fill(0)
HAShat.OLED.show()
HASit.cleanup()
