#!/usr/bin/python3
#
# HVDN LORA BROADCAST ADA
#
# hvdncomm-lora-broadcast_ada.py
#
# Usage: hvdncomm-lora-broadcast_ada.py bcount "message"
#
# Dependencies:
#
#     This enables and uses the Adafruit library
#
#     https://pypi.org/project/raspi-lora/
#
# Revisions:
#
#
# To-do:
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
import adafruit_rfm9x
#from raspi_lora import LoRa, ModemConfig

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

parser = argparse.ArgumentParser(description='Broadcast a LoRa message.')
parser.add_argument('-c','--count', type=int, help='number of times te repeate the message', required=True)
parser.add_argument('-m','--message', help='Message to be broadcast in quotes', required=True)
args = vars(parser.parse_args())

bcount = args['count']
message = args['message']


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

# Initialize RFM9x LoRa radio using raspi-lora Library (DISABLED) 

#lora = LoRa(1,gpio_rfm_irq, node_address, freq=freqmhz, modem_config=ModemConfig.Bw125Cr45Sf128, tx_power=txpwr, acks=False)


# Initialize RFM9x LoRa radio using Adafruit Libraries

CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, freqmhz)
rfm9x.tx_power = txpwr

# Note that with Adafruit rfm9X library you can't control sync
# word, encryption, frequency deviation, or other settings!

# Send a packet.  Note you can only send a packet up to 252 bytes in length.
# This is a limitation of the radio packet size, so if you need to send larger
# amounts of data you will need to break it into smaller send calls.  Each send
# call will wait for the previous one to finish before continuing.
#rfm9x.send(bytes("Hello world!\r\n","utf-8"))
#print('Sent Hello World message!')

# Wait to receive packets.  Note that this library can't receive data at a fast
# rate, in fact it can only receive and process one 252 byte packet at a time.
# This means you should only use this for low bandwidth scenarios, like sending
# and receiving a single message at a time.
#print('Waiting for packets...')


#
# Functions
#

#
# MAIN
#

#
# Send Broadcast 
#
reprinse=0
while bcount > reprinse:
   reprinse = reprinse + 1
   #lora.send_to_wait(message, recipient, header_flags=0)
   rfm9x.send(bytes(message,"utf-8")) 
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
#lora.close()
