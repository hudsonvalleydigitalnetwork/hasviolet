#!/usr/bin/python3
#
# HVDN LORA BROADCAST - ALPHA
#
# Alpha 20180825 Joe NE2Z - Initial Success
#
#
#
# https://pypi.org/project/raspi-lora/
#
# Sends out a broadcast message
#

#
# Imports
#

#import argparse
import sys
import time

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
#message = str(sys.argv)
message = "VVV"

#
# Setup
#

from raspi_lora import LoRa, ModemConfig

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
yay=0

while True:
   yay=yay+1
   lora.send_to_wait(message, recipient, header_flags=0)
   print(yay)
   time.sleep(3)
print ("Closing ...")

# And remember to call this as your program exits...
lora.close()
