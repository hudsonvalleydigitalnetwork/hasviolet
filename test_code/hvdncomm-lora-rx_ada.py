#!/usr/bin/python3
#
# HVDN LORA RECEIVE ADA
#
# Usage: hvdncomm-lora-rx_ada.py
#
# Inspired by sample code from Tony DiCola
#
# Dependencies:
#
#     Note libraries referenced below. This uses Adafruit rfm9x library
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

#example-arg-1= int(sys.argv[1])
#example-arf-2= sys.argv[2]

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
# FUNCTIONS
#


#
# MAIN
#

while True:
    #packet = rfm9x.receive()
    # Optionally change the receive timeout from its default of 0.5 seconds:
    packet = rfm9x.receive(timeout=5.0)
    # If no packet was received during the timeout then None is returned.
    if packet is None:
        # Packet has not been receive.d for some reason noop necessary to avoide format fail of if-else
        noop
    else:
        print('  ')
        # Print out the raw bytes of the packet:
        print('RAW BYTES: {0}'.format(packet))
        # Decode to ASCII text and print.  Note that you always
        # receive raw bytes and need to convert to a text format like ASCII
        # if you intend to do string processing on your data.  Make sure the
        # sending side is sending ASCII data before you try to decode!
        packet_text = str(packet, 'ascii')
        print('      MSG: {0}'.format(packet_text))
        # RSSI (signal strength) of the last received message and
        rssi = rfm9x.rssi
        print('     RSSI: {0} dB'.format(rssi))
        print('  ')
        display.fill(0)
        display.text('From: ',35 ,0 ,1)
        display.text(packet_text, 25, 15,1)
        display.show()

