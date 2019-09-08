#!/usr/bin/python3
#
# HVDN LORA BROADCAST 
#
# hvdncomm-lora-broadcast_rf95.py
#
# Usage: hvdncomm-lora-broadcast_rdl.py bcount "message"
#
# Dependencies:
#
#     This uses the rf95 library
#
#     https://github.com/ladecadence/pyRF95
#
# Revisions:
#
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

bcount= int(sys.argv[1])
message = sys.argv[2]

#
# Variables
#
# gpio_rfm_irq - Use chip select 1. GPIO pin 22 will be used for interrupts
# node_address - The address of this device will be set to (1-254)
# freqmhz - The freq of this device in MHz (911.250 MHz is recommended)
# recipient - Address of receiveing LoRa node, 255 = broadcast
# message - message as caputred from args


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

# Send broadcast

reprinse=0

if __name__ == '__main__':
    # Tell Python to run the handler() function when SIGINT is recieved
    signal(SIGINT, handler)

    print('HVDN Communicator TX Running...')
    print('Press CTRL-C to exit.')
    while bcount > reprinse:
       reprinse = reprinse + 1
       rf95.send(rf95.str_to_data(message))
       rf95.wait_packet_sent()
       print("Sent ", reprinse,":", message)
       display.fill(0)
       display.text("Sending Count " + str(reprinse), 0, 0, 1)
       display.text(message, 5, 10, 1)
       display.show()
       time.sleep(3)
print ("Closing ...")

display.fill(0)
display.show()
    
rf95.set_mode_idle()
rf95.cleanup()

