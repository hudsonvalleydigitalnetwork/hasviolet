#!/usr/bin/python3
#
# HVDN LORA RX
#
#
# Usage: hvdn_lora-rx.py
#
#
# REVISIONS:
#
#
# TO-DO:
#
#


#
# Import Libraries
#

import adafruit_ssd1306
import argparse
import board
import busio
import configparser
import curses
from digitalio import DigitalInOut, Direction, Pull
from rf95 import RF95, Bw31_25Cr48Sf512
import signal
import sys
import time


#
# IMPORT SETTINGS
#

config = configparser.ConfigParser()
config.sections()
config.read('hvdn-comm.ini')
try:
   gpio_rfm_cs = int(config["DEFAULT"]["gpio_rfm_cs"])
   gpio_rfm_irq = int(config["DEFAULT"]["gpio_rfm_irq"])
   node_address = int(config["DEFAULT"]["node_address"])
   freqmhz = float(config["DEFAULT"]["freqmhz"])
   txpwr = int(config["DEFAULT"]["txpwr"])
   modemcfg = str(config["DEFAULT"]["modemcfg"])
except KeyError as e:
   raise LookupError("Error hvdn-comm.ini[DEFAULT] : {} missing.".format(str(e)))
   exit (1)


#
# IMPORT ARGS
#

parser = argparse.ArgumentParser(description='LoRa RX')
parser.add_argument('-r','--raw_data', help='Receive raw data', action='store_true')
parser.add_argument('-s','--signal', help='Signal Strength', action='store_true')
args = vars(parser.parse_args())
arg_hvdn_rawdata = args['raw_data']
arg_signal_rssi = args['signal']


#
# VARIABLES
#

# gpio_rfm_irq - Use chip select 1. GPIO pin 22 will be used for interrupts
# node_address - The address of this device will be set to (1-254)
# freqmhz - The freq of this device in MHz (911.250 MHz is recommended)
# recipient - Address of receiving LoRa node, 255 = broadcast


#
# FUNCTIONS
#

def sigs_handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    rf95.set_mode_idle()
    rf95.cleanup()
    exit(0)


#
# SETUP
#


#
# MAIN
#

# Setup Radio

rf95 = RF95(cs=gpio_rfm_cs, int_pin=gpio_rfm_irq, reset_pin=None)
rf95.set_frequency(freqmhz)
rf95.set_tx_power(txpwr)
#rf95.set_modem_config(modemcfg)('RAW:',data,':RSSI:',data_rssi)
rf95.init()

# SIGTINT aka control-C is quit
signal.signal(signal.SIGINT, sigs_handler)

# While not hearing packets check for tab pressed to ennter tx mode
while True:
    while not rf95.available():
        pass
    data = rf95.recv()
    data_rssi = str(int(rf95.last_rssi))
    data_stringed = str(data)
    data_ascii=""
    for i in data:
        data_ascii=data_ascii+chr(i)
    if (arg_hvdn_rawdata) and (arg_signal_rssi):
        print (str(data) + "|:|" + data_rssi, end = '', flush=True)
#        print (data_rssi, end ='', flush=True)
    elif (arg_hvdn_rawdata):
        print (data, end ='', flush=True)
    elif (arg_signal_rssi):
        print (data_ascii + "|:|" + data_rssi, end = '', flush=True)
#        print(data_rssi, end = '', flush=True)
    else:
        print (data_ascii, end = '', flush=True)
    print ()
rf95.cleanup()
