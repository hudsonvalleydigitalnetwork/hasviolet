#!/usr/bin/python3
#
# HASviolet RX rf95
#
# 
#
# Usage: HASviolet-rx.py [-r] [-s]
#
#  OPTIONS
#      -h, --help      show this help message and exit
#      -r, --raw_data  Receive raw data
#      -s, --signal    Signal Strength
#
#  REVISION: 20210312-1400
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
# VARIABLES
#

HASVIOLET_CONFIG = "~/.config/HASviolet/etc/HASviolet.json"

#
# FUNCTIONS
#

def sigs_handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    HASit.cleanup()                 # rf95 library
    #HASit.cleanup_pyl()            # pyLora library
    HAShat.OLED.text('Goodbye...', 0, 10, 1)
    HAShat.OLED.show()
    time.sleep(2)
    HAShat.OLED.fill(0)
    HAShat.OLED.show()
    exit(0)

def rx_oled_scroll():
    HAShat.OLED.fill(0)
    HAShat.OLED.show()
    HASit.ppayload = HASit.receive_ascii.split("|")
    HAShat.OLED.fill(0)
    HAShat.OLED.show()
    HAShat.OLED.text(HASit.ppayload[0], 0, 1, 1)
    HAShat.OLED.text("RSSI: " + HASit.receive_rssi, 0, 9, 1)
    HAShat.OLED.show()
  
  
#
# Initialise HASviolet
#

HASit = HASrf()
HAShat = HAShid()


#
# IMPORT ARGS
#

parser = argparse.ArgumentParser(description='HASviolet RX')
parser.add_argument('-r','--raw_data', help='Receive raw data', action='store_true')
parser.add_argument('-s','--signal', help='Signal Strength', action='store_true')
args = vars(parser.parse_args())
arg_hvdn_rawdata = args['raw_data']
arg_signal_rssi = args['signal']

  
#
# SETUP
#

HAShat.logo('~/.config/HASviolet/etc/HVDN_logo.xbm')

# SIGTINT aka control-C is quit
signal.signal(signal.SIGINT, sigs_handler)

# RF and LoRa Config init
HASit.startradio()                       # rf95 library
#HASit.startradio_pyl()                  # pyLoraRFM9x Library
#HASit.rfm.on_recv(HASit.onreceive)      # pyLoraRFM9x Library (Uses callback for receive)


prevpos = 0
currpos = 0
firstoledline = 7
lastoledline = 23

HAShat.OLED.fill(0)
HAShat.OLED.show()


#
# MAIN
#

# pyLoraRFM9x Library. Uses callback for receive so main is a infinite while loop with pass
# rf95 library. Needs to be executes within an infinite while loop

while True:

    HASit.rx()
    rx_oled_scroll()
    if (arg_signal_rssi):
        #datadisplay_string = 'RX:'+ HASit.receive_ascii +':RSSI:'+HASit.receive-rssi
        print (HASit.receive_ascii,':RSSI:',HASit.receive_rssi)
    else:
        print (HASit.receive_ascii)

HAShat.OLED.fill(0)
HAShat.OLED.show()
HASit.cleanup()                 # rf95 library
#HASit.cleanup_pyl()            # pyLora library
    
