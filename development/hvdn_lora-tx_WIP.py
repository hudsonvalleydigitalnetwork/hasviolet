#!/usr/bin/python3
#
# HVDN LORA BEACON
#
#
#  Usage: hvdn_lora-beacon.py -c COUNT -t DELAY "message"
#
#  OPTIONS
#           -b continously BEACON the MESSAGE
#           -t seconds of delay before MESSAGE is repeated when in BEACON mode
#           MESSAGE contained double quotes ("")
#
#
#  TO-DO:
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

parser = argparse.ArgumentParser(description='HVDN LoRa Beacon')
parser.add_argument('-b','--beacon x', type=int, help='continously repeat message every x seconds ', required=False)
parser.add_argument('-m','--message', help='Message to be broadcast in quotes', required=True)
args = vars(parser.parse_args())

beacon_msg = 0
if args['beacon'] > 0:
	beacon_msg = args['beacon']
message = args['message']


#
# VARIABLES
#

# gpio_rfm_irq - Use chip select 1. GPIO pin 22 will be used for interrupts
# node_address - The address of this device will be set to (1-254)
# freqmhz - The freq of this device in MHz (911.250 MHz is recommended)
# recipient - Address of receiveing LoRa node, 255 = broadcast
# message - message as caputred from args



#
# FUNCTIONS
#

def sigs_handler(signal_received, frame):
    # Handle any cleanup here
    print('CTRL-C detected. Exiting gracefully')
    rf95.set_mode_idle()
    rf95.cleanup()
    display.fill(0)
    display.show()
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


#
# MAIN
#

# Setup Radio

#rf95 = RF95(cs=1, int_pin=22, reset_pin=None)
rf95 = RF95(cs=gpio_rfm_cs, int_pin=gpio_rfm_irq, reset_pin=None)
rf95.set_frequency(freqmhz)
rf95.set_tx_power(txpwr)
# Custom predefined mode
#rf95.set_modem_config(Bw31_25Cr48Sf512)
rf95.init()

# SIGTINT aka control-C is quit
signal.signal(signal.SIGINT, sigs_handler)

# Send message

print('HVDN LoRa TX is running...')
print('Press CTRL-C to exit.')

rf95.send(rf95.str_to_data(message))
rf95.wait_packet_sent()

if beacon_msg == 0:
	print (message)
	OLED_display('txmsg', message)
	time.sleep(beacon_msg)
	rf95.set_mode_idle()
	rf95.cleanup()
	display.fill(0)
	display.show()
	exit(0)
try:
	print (message)
	OLED_display('txmsg', message)
	time.sleep(beacon_msg)
except (KeyboardInterrupt, SystemExit):
    raise
except:
    # report error and proceed
rf95.set_mode_idle()
rf95.cleanup()


