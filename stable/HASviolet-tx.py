#!/usr/bin/python3
#
# HASviolet TX
#
#
#  Usage: HASviolet-tx.py destination-node "message"
#
#  OPTIONS
#       destination-node is LoRa Node Number ID destination
#       MESSAGE is sent in double quotes
#
#
# TO-DO:
#
#


#
# IMPORT LIBRARIES
#


import adafruit_ssd1306
import argparse
import board
import busio
import configparser
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
config.read('HASviolet.ini')
try:
   gpio_rfm_cs = int(config["DEFAULT"]["gpio_rfm_cs"])
   gpio_rfm_irq = int(config["DEFAULT"]["gpio_rfm_irq"])
   node_address = int(config["DEFAULT"]["node_address"])
   freqmhz = float(config["DEFAULT"]["freqmhz"])
   txpwr = int(config["DEFAULT"]["txpwr"])
   modemcfg = str(config["DEFAULT"]["modemcfg"])
   mycall = str(config["DEFAULT"]["mycall"])
   ssid = str(config["DEFAULT"]["ssid"])
   beacon = str(config["DEFAULT"]["beacon"])
except KeyError as e:
   raise LookupError("Error HASviolet.ini[DEFAULT] : {} missing.".format(str(e)))
   exit (1)


#
# IMPORT ARGS
#

parser = argparse.ArgumentParser(description='HASviolet TX')
parser.add_argument('-d','--destination', help='Destination Name-Call', required=True)
parser.add_argument('-m','--message', help='Message to be sent in quotes', required=True)
args = vars(parser.parse_args())

hasvrecipient = args['destination']
message = args['message']


#
# VARIABLES
#

# gpio_rfm_irq - Use chip select 1. GPIO pin 22 will be used for interrupts
# node_address - The address of this device will be set to (1-254)
# freqmhz - The freq of this device in MHz (911.250 MHz is recommended)
# hasvrecipient - Address of receiving node
# hasvname - mycall + "-" + ssid
# hasvheader - hasname + ">" + hasvrecipient
# hasvpayload - header + message

hasvname = mycall + "-" + ssid
hasvheader = hasvname + ">" + hasvrecipient
hasvpayload = hasvheader + " | " + message 

#
# FUNCTIONS
#

def sigs_handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    rf95.set_mode_idle()
    rf95.cleanup()
    OLED_display('bye','GoodBye...')
    exit(0)

def OLED_display(OLED_where, OLED_msg):
    display.fill(0)
    if OLED_where == 'logo':
        display.text(OLED_msg, 0, 10, 1)
    elif OLED_where == 'rxid':
        display.text(OLED_msg, 0, 20, 1)
    elif OLED_where == 'rxmsg':
        display.text(OLED_msg, 0, 20, 1)
    elif OLED_where == 'txid':
        display.text(OLED_msg, 0, 0, 1)
    elif OLED_where == 'txmsg':
        display.text(OLED_msg, 0, 0, 1)
    elif OLED_where == 'bye':
        display.text(OLED_msg, 0, 10, 1)
        display.show()
        time.sleep (3)
        display.fill(0)
        display.show()
    else:
        display.fill(0)
    display.show()


#
# SETUP
#

# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)

# 128x32 OLED Display
display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, addr=0x3c)

# Clear the OLED display.
display.fill(0)
display.show()
width = display.width
height = display.height

# Startup OLED Message

display.fill(0)
display.text('HASviolet TX', 35, 0, 2)
display.show()

# SIGTINT aka control-C is quit
signal.signal(signal.SIGINT, sigs_handler)


#
# MAIN
#

# Setup Radio

rf95 = RF95(cs=gpio_rfm_cs, int_pin=gpio_rfm_irq, reset_pin=None)
rf95.set_frequency(freqmhz)
rf95.set_tx_power(txpwr)
# Custom predefined mode
#rf95.set_modem_config(Bw31_25Cr48Sf512)
#rf95.set_modem_config(modemcfg)
rf95.init()
# hasname - mycall + "-" + ssid
# payload - hasname + message

# Send message
rf95.send(rf95.str_to_data(hasvpayload))
rf95.wait_packet_sent()

print(hasvpayload)
display.fill(0)
display.text('TX:', 0, 0, 1)
display.text(hasvpayload, 5, 10, 1)
display.show()

time.sleep(5)
display.fill(0)
display.text('HASviolet TX', 5, 10, 1)
display.show()

display.fill(0)
display.show()

rf95.set_mode_idle()
rf95.cleanup()