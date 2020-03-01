#!/usr/bin/python3
#
# HVDN LORA TX ENGINE
#
#
#  Usage: hvdn_lora-tx.py "message"
#
#  OPTIONS
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
#import rf95
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
   modemcfg = config["DEFAULT"]["modemcfg"]
   call = config["XARPS"]["call"]
except KeyError as e:
   raise LookupError("Error hvdn-comm.ini[DEFAULT] : {} missing.".format(str(e)))
   exit (1)


#
# IMPORT ARGS
#

parser = argparse.ArgumentParser(description='HVDN LoRa TX')
parser.add_argument('-d','--destination', help='Destination')
parser.add_argument("message", help='Message')
args = vars(parser.parse_args())

recipient = args['destination']
message = args['message']
message = call + ">" + recipient + ":" + message

#
# VARIABLES
#

# gpio_rfm_irq - Use chip select 1. GPIO pin 22 will be used for interrupts
# node_address - The address of this device will be set to (1-254)
# freqmhz - The freq of this device in MHz (911.250 MHz is recommended)
# recipient - Address of receiving LoRa node


#
# FUNCTIONS
#

def sigs_handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    hvdn_lora.set_mode_idle()
    hvdn_lora.cleanup()
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
display.text('HVDN LoRa TX', 35, 0, 2)
display.show()

# SIGTINT aka control-C is quit
signal.signal(signal.SIGINT, sigs_handler)

#
# MAIN
#

# Setup Radio

hvdn_lora = RF95(cs=gpio_rfm_cs, int_pin=gpio_rfm_irq, reset_pin=None)
hvdn_lora.set_frequency(freqmhz)
hvdn_lora.set_tx_power(txpwr)
hvdn_lora.init()

# SIGTINT aka control-C is quit

signal.signal(signal.SIGINT, sigs_handler)

# Send message

hvdn_lora.send(hvdn_lora.str_to_data(message))
hvdn_lora.wait_packet_sent()
print (message)
OLED_display('txmsg','TX:' + message)
time.sleep (3)
display.fill(0)
display.show()

hvdn_lora.set_mode_idle()
hvdn_lora.cleanup()
