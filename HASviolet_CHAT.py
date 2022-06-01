#!/usr/bin/python3
#
# HASviolet CHAT
#
#
#   USAGE: HASviolet-chat [-r] [-s]
#
#      Within program use CTRL-Z to Send a message and
#      CTRL-C to exit program
#
#   OPTIONS
#        -r Raw data RX instead of ASCII
#        -s Show RSSI RX
#
#   REVISION: 20220601-0200
#
#


#
# IMPORT
#

import argparse 
import configparser
import signal
import sys
import time
from HASvioletRF import HASrf
from HASvioletHID import HAShid


#
# STATICS
#

HASviolet_RXLOCK = False                                               # True = RX is running
HASviolet_TXLOCK = False                                               # True = TX is running
HASviolet_CFGDIR = "~/.config/HASviolet/"                              # Config file is in JSON format
HASviolet_SRVDIR = HASviolet_CFGDIR + "server/"                        # Path to files. Change when Pi
HASviolet_ETC = HASviolet_CFGDIR + "etc/"                              # Config file is in JSON format
HASviolet_CONFIG = HASviolet_CFGDIR + "HASviolet.json"                 # Config file is in JSON format
HASviolet_PWF = HASviolet_ETC + "HASviolet.pwf"                        # Password file  user:hashedpasswd
HASviolet_MSGS = HASviolet_SRVDIR + "msgs/HASviolet.msgs"              # radio writes msgs received here   
HASviolet_LOGIN = HASviolet_SRVDIR + "static/HASviolet_LOGIN.html"
HASviolet_LOGINCSS = HASviolet_SRVDIR + "static/HASviolet_LOGIN.css"
HASviolet_INDEX = HASviolet_SRVDIR + "static/HASviolet_INDEX.html"
HASviolet_INDEXCSS = HASviolet_SRVDIR + "static/HASviolet.css"
HASvioletjs = HASviolet_SRVDIR + "static/HASviolet.js"
HVDN_LOGO = HASviolet_ETC + "HVDN_logo.xbm"


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
    hasvheader = HASit.mystation + ">" + hasvrecipient
    hasvpayload = hasvheader + " | " + message 
    HASit.transmit(hasvpayload)
    print ('<TX>',hasvpayload)
    print ()

def rx_oled_scroll():
    HAShat.OLED.fill(0)
    HAShat.OLED.show()
    HAShat.OLED.text("RSSI: " + HASit.receive_rssi, 0, 9, 1)
    HAShat.OLED.text(HASit.receive_ascii, 0, 17, 1)
    HAShat.OLED.show()


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
# SETUP
#

HAShat.logo(HVDN_LOGO)

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

# RF and LoRa Config init
HASit.startradio()                       # rf95 library
#HASit.startradio_pyl()                  # pyLoraRFM9x Library
#HASit.rfm.on_recv(HASit.onreceive)      # pyLoraRFM9x Library (Uses callback for receive)

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