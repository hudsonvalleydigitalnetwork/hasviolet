#!/usr/bin/python3
#
# HVDN LORA CHAT RF95
#
# Usage: hvdncomm-lora-chat_r95.py
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
#
#

#
# Import Libraries
#

import argparse
import configparser
import sys
import time
import signal
#from signal import signal, SIGSTSTP
import busio
from digitalio import DigitalInOut, Direction, Pull
import board
import adafruit_ssd1306
#import rf95
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
   modemcfg = str(config["DEFAULT"]["modemcfg"])
except KeyError as e:
   raise LookupError("Error hvdn-comm.ini[DEFAULT] : {} missing.".format(str(e)))
   exit (1)

#
# Import args
#
#
#recipient = int(sys.argv[1])
#message = sys.argv[2]
#
#
#parser = argparse.ArgumentParser(description='Send a LoRa message.')
#parser.add_argument('-d','--destination', type=int, help='Destination address 1-255', required=True)
#parser.add_argument('-m','--message', help='Message to be sent in quotes', required=True)
#args = vars(parser.parse_args())
#
#recipient = args['destination']
#message = args['message']



#
# Variables
#

# gpio_rfm_irq - Use chip select 1. GPIO pin 22 will be used for interrupts
# node_address - The address of this device will be set to (1-254)
# freqmhz - The freq of this device in MHz (911.250 MHz is recommended)
# recipient - Address of receiving LoRa node, 255 = broadcast
# message - message to be sent. Must be in quotes or only will send one word
# modemcfg - LoRa signal settings

hvdn_recipient = "255"
hvdn_message = "testing"

#
# FUNCTIONS
#
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

def handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    rf95.set_mode_idle()
    rf95.cleanup()
    OLED_display('bye','GoodBye...')
    exit(0)

def hvdn_txmode(signal_received, frame):
    print ('Recipient:')
    hvdn_recipient = input()
    if hvdn_recipient == '/QUIT':
      rf95.set_mode_idle()
      rf95.cleanup()
      OLED_display('quit','')
      exit(0)
    print ('Message:')
    hvdn_message = input()
    rf95.send(rf95.str_to_data(hvdn_message))
    rf95.wait_packet_sent()
    print('TX: ' + hvdn_recipient + ' : ' + hvdn_message)
    OLED_display('txmsg','TX:' + hvdn_recipient + ' :' + hvdn_message)
    rf95.set_mode_idle

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
OLED_display('logo','HVDN Communicator')

#
# MAIN
#

# Setup Radio

rf95 = RF95(cs=gpio_rfm_cs, int_pin=gpio_rfm_irq, reset_pin=None)
rf95.set_frequency(freqmhz)
rf95.set_tx_power(txpwr)
#rf95.set_modem_config(modemcfg)
rf95.init()

# Tell Python to run the handler() function when SIGSTP aka control-Z is recieved
signal.signal(signal.SIGTSTP, hvdn_txmode)
signal.signal(signal.SIGINT, handler)
print()
print('HVDN Communicator Chat')
print()

# While not hearing packets check for tab pressed to ennter tx mode
while True:
    while not rf95.available():
#        signal.signal(signal.SIGTSTP, hvdn_txmode)
        pass
    data = rf95.recv()
    print ('  RAW:   ',data)
    data_ascii=""
    for i in data:
        data_ascii=data_ascii+chr(i)
    print ('ASCII:  ',data_ascii)
    print (' RSSI:  ',rf95.last_rssi)
    print ()
#       display.fill(0)
#       display.text(data, 1, 10, 1)
#       display.text(data_ascii, 1, 15, 1)
#       display.show()
    OLED_display('rxmsg','RX:' + hvdn_recipient + ' :' + data_ascii)
display.fill(0)
display.show()
rf95.cleanup()
