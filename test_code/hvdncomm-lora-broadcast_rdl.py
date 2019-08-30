#!/usr/bin/python3
#
# HVDN LORA BROADCAST 
#
# hvdncomm-lora-broadcast_rdl.py
#
# Usage: hvdncomm-lora-broadcast_rdl.py bcount "message"
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
#     Alpha  - 20190828: Initial Success using raspi-lora librarys
#     Beta   - 20190830: Added count option
#
# To-do:
#            - Add OLED
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

gpio_rfm_irq=22
node_address=1
freqmhz = 911.25
recipient = 255

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

lora = LoRa(1,gpio_rfm_irq, node_address, freq=freqmhz, modem_config=ModemConfig.Bw125Cr45Sf128, tx_power=14, acks=False)

#
# Send a message to dest_address
#
reprinse=0
while bcount > reprinse:
   reprinse = reprinse + 1
   lora.send_to_wait(message, recipient, header_flags=0)
   print("Sent ", reprinse,":", message)
   display.fill(0)
   display.text("Send Count " + str(reprinse), 0, 0, 1)
   display.text(message, 5, 10, 1)
   display.show()
   time.sleep(3)
print ("Closing ...")

display.fill(0)
display.text('HVDN Communicator', 5, 10, 1)
display.show()

# And remember to call this as your program exits...
lora.close()
