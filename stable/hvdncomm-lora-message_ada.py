#!/usr/bin/python3
#
# HVDN LORA MESSAGE ADA
#
# hvdncomm-lora-message_ada.py
#
# Usage: hvdncomm-lora-message_ada.py destination-node "message"
#
# Dependencies:
#
#     This enables and uses the Adafruit RFM9x library. 
#
#
# Revisions:
#
#     Alpha  - 20180829: Initial Success using Adafruit library
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

#recipient = int(sys.argv[1])
#message = sys.argv[2]


parser = argparse.ArgumentParser(description='Send a LoRa message.')
parser.add_argument('-d','--destination', type=int, help='Destination address 1-255', required=True)
parser.add_argument('-m','--message', help='Message to be sent in quotes', required=True)
args = vars(parser.parse_args())

recipient = args['destination']
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
# FUNCTIONS
#

 
#
# MAIN
#

#
# Send a message to dest_address
#

rfm9x.send(bytes(message,"utf-8"))
#lora.send_to_wait(message, recipient, header_flags=0)

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

#lora.close()
