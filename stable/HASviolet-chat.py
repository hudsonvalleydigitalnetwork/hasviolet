#!/usr/bin/python3
#
# HASviolet CHAT
#
#
#  Usage: HASviolet-chat [-r] [-s]
#
#      Within program use CTRL-Z to Send a message and
#      CTRL-C to exit program
#
#  OPTIONS
#        -r Raw data RX instead of ASCII
#        -s Show RSSI RX
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

parser = argparse.ArgumentParser(description='HASviolet Chat')
parser.add_argument('-r','--raw_data', help='Receive raw data', action='store_true')
parser.add_argument('-s','--signal', help='Signal Strength', action='store_true')
args = vars(parser.parse_args())
arg_hvdn_rawdata = args['raw_data']
arg_signal_rssi = args['signal']


#
# VARIABLES
#


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

def sigs_txmode(signal_received, frame):
    print () 
    hasvrecipient = input('CALL-SSID: ')
    message = input('MSG: ')
    hasvheader = HASit.station + ">" + hasvrecipient
    hasvpayload = hasvheader + " | " + message 
    HASit.tx(hasvpayload)
    print ('<TX>',hasvpayload)
    print ()

def rx_oled_scroll():
    HAShat.OLED.fill(0)
    HAShat.OLED.show()
    HASit.ppayload = HASit.receive_ascii.split("|")
    HAShat.OLED.fill(0)
    HAShat.OLED.show()
    HAShat.OLED.text(HASit.ppayload[0], 0, 1, 1)
    HAShat.OLED.text("RSSI: " + HASit.receive_rssi, 0, 9, 1)
    HAShat.OLED.text(HASit.ppayload[1], 0, 17, 1)
    HAShat.OLED.show()


#
# SETUP
#

HAShat.logo('hvdn-logo.xbm')

width = HAShat.OLED.width
height = HAShat.OLED.height


#
# MAIN
#

# Setup Radio

# CTRL-Z is SIGTSTP to Send
# CTRL-C is SIGINT and closes program gracefully
signal.signal(signal.SIGTSTP, sigs_txmode)
signal.signal(signal.SIGINT, sigs_handler)

print()
print('HASviolet Chat')
print('    (Entering RX mode ... use Ctrl-Z to send, Ctrl-C to exit)')
print('-------------------------------------------------------------')

# While not hearing packets check for tab pressed to ennter tx mode
while True:
    HASit.rx()
    rx_oled_scroll()
    if (arg_hvdn_rawdata) and (arg_signal_rssi):
        #datadisplay_string = 'RAW:'+ HASit.receive_string +':RSSI:'+HASit.receive-rssi
        print ('RAW:',HASit.receive,':RSSI:',HASit.receive_rssi)
    elif (arg_hvdn_rawdata):
        #datadisplay_string = 'RAW:'+ HASit.receive_string
        print ('RAW:',HASit.receive)
    elif (arg_signal_rssi):
        #datadisplay_string = 'RX:'+ HASit.receive_ascii +':RSSI:'+HASit.receive-rssi
        print (HASit.receive_ascii,':RSSI:',HASit.receive_rssi)
    else:
        print (HASit.receive_ascii)

HAShat.OLED.fill(0)
HAShat.OLED.show()
HASit.cleanup()
