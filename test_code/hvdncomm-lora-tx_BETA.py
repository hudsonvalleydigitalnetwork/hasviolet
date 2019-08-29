#!/usr/bin/python3
#
# HVDN LORA TX 
#
# hvdncomm-lora-tx.py
#
# Usage: hvdncomm-lora-tx.py destination-node "message"
#
# Dependencies:
#
#     Note libraries referenced below. This used the raspi-lora library
#     available via pip and NOT the Adafruit RFM9x library. 
#
#     https://pypi.org/project/raspi-lora/
#
# Revisions:
#
#     Alpha  - 20180828: Initial Success using raspi-lora librarys
#
#
# To-do:
#            - Add ModemConfig option to ini file
#            - More complete args support overide of INI file
#            - Clean up OLED
#            - Canned test msg toggled via button
#

#
# Import Libraries
#

import argparse
import configparser
import sys
import time
import busio
from digitalio import DigitalInOut, Direction, Pull
import board
import adafruit_ssd1306
from raspi_lora import LoRa, ModemConfig

#
# Import Settings
#

config = configparser.ConfigParser()
config.sections()
config.read('hvdn-comm.ini')
try:
   gpio_rfm_irq = int(config["DEFAULT"]["gpio_rfm_irq"])
   node_address = int(config["DEFAULT"]["node_address"])
   freqmhz = float(config["DEFAULT"]["freqmhz"])
   txpwr = int(config["DEFAULT"]["txpwr"])
except KeyError as e:
   raise LookupError("Error hvdn-comm.ini[DEFAULT] : {} missing.".format(str(e)))
   exit (1)
#
# Variables
#

# gpio_rfm_irq - Use chip select 1. GPIO pin 22 will be used for interrupts
# node_address - The address of this device will be set to (1-254)
# freqmhz - The freq of this device in MHz (911.250 MHz is recommended)
# recipient - Address of receiving LoRa node, 255 = broadcast
# message - message to be sent. Must be in quotes or only will send one word


#
# Import args
#

recipient = int(sys.argv[1])
message = sys.argv[2]

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
# Functions
#

#
# MAIN
#

lora = LoRa(1,gpio_rfm_irq, node_address, freq=freqmhz, modem_config=ModemConfig.Bw125Cr45Sf128, tx_power=txpwr, acks=False)

#
# Send a message to dest_address
#

lora.send_to_wait(message, recipient, header_flags=0)
print("Sending to", recipient)
display.fill(0)
display.text('Sending to', 0, 0, 1)
display.text(str(recipient), 5, 10, 1)
display.show()
time.sleep(3)
print ("Sent")
display.fill(0)
display.text('Sent', 5, 10, 1)
display.show()
time.sleep(2)
display.fill(0)
display.text('HVDN Communicator', 5, 10, 1)
display.show()

# And remember to call this as your program exits...

lora.close()
