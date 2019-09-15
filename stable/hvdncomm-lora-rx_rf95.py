#!/usr/bin/python3
#
# HVDN LORA RECEIVE RF95
#
# Usage: hvdncomm-lora-rx_r95.py
#
#
# Dependencies:
#
#     This uses rf95 library
#
#
# Revisions:
#
# To-do:
#            - Add OLED
#

#
# Import Libraries
#

import argparse
import configparser
import sys
import time
from signal import signal, SIGINT
import busio
from digitalio import DigitalInOut, Direction, Pull
import board
import adafruit_ssd1306
from rf95 import RF95, Bw31_25Cr48Sf512


#
# Import Settings
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
except KeyError as e:
   raise LookupError("Error hvdn-comm.ini[DEFAULT] : {} missing.".format(str(e)))
   exit (1)

#
# Import args
#

#example-arg-1= int(sys.argv[1])
#example-arf-2= sys.argv[2]


#
# Variables
#

# gpio_rfm_irq - Use chip select 1. GPIO pin 22 will be used for interrupts
# node_address - The address of this device will be set to (1-254)
# freqmhz - The freq of this device in MHz (911.250 MHz is recommended)
# recipient - Address of receiving LoRa node, 255 = broadcast
# message - message to be sent. Must be in quotes or only will send one word


#
# Setup
#

# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)

# 128x32 OLED Display
display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, addr=0x3c)

# Clear the display.
display.fill(0)
display.show()
width = display.width
height = display.height

# Startup OLED Message

display.fill(0)
display.text('HVDN Communicator', 35, 0, 2)
display.show()


#
# FUNCTIONS
#
def handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    rf95.set_mode_idle()
    rf95.cleanup()
    display.fill(0)
    display.show()
    exit(0)


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

if __name__ == '__main__':
    # Tell Python to run the handler() function when SIGINT is recieved
    signal(SIGINT, handler)

    print('HVDN Communicator RX Running...')
    print('Press CTRL-C to exit.')

    while True:
       while not rf95.available():
          pass
       data = rf95.recv()
       print (data)
       for i in data:
#           print(chr(i))
           print(chr(i), end="")
#           print()

display.fill(0)
display.show()

rf95.set_mode_idle()
rf95.cleanup()
