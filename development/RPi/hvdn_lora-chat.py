#!/usr/bin/python3
#
# HVDN LORA CHAT
#
#
#  Usage: hvdn_lora-chat [-r] [-s]
#
#      Within program use CTRL-Z to Send a message and
#      CTRL-C to exit program
#
#  OPTIONS
#        -r Raw data RX instead of ASCII
#        -s Show RSSI RX
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
#from rf95 import RF95
#import rf95
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
   modem_cfg = int(config["DEFAULT"]["modemcfg"])
   call = str(config["XARPS"]["call"])
   beacon = str(config["XARPS"]["beacon"])
except KeyError as e:
   raise LookupError("Error hvdn-comm.ini: {} missing.".format(str(e)))
   exit (1)


#
# IMPORT ARGS
#

parser = argparse.ArgumentParser(description='HVDN LoRa Pocket')
parser.add_argument('-r','--raw_data', help='Receive raw data', action='store_true')
parser.add_argument('-s','--signal', help='Signal Strength', action='store_true')
args = vars(parser.parse_args())
arg_hvdn_rawdata = args['raw_data']
arg_signal_rssi = args['signal']


#
# VARIABLES
#

# gpio_rfm_irq - Use chip select 1. GPIO pin 22 will be used for interrupts
# node_address - The address of this device will be set to (1-254)
# freqmhz - The freq of this device in MHz (911.250 MHz is recommended)
# recipient - Address of receiveing LoRa node, 255 = broadcast

# Button A = Send Message
btnA = DigitalInOut(board.D5)
btnA.direction = Direction.INPUT
btnA.pull = Pull.UP
 
# Button B = Change LoRa Mode
btnB = DigitalInOut(board.D6)
btnB.direction = Direction.INPUT
btnB.pull = Pull.UP
 
# Button C = ACK Message
btnC = DigitalInOut(board.D12)
btnC.direction = Direction.INPUT
btnC.pull = Pull.UP


#
# FUNCTIONS
#

def sigs_handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    rf95.set_mode_idle()
    rf95.cleanup()
    OLED_display('bye','GoodBye...')
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

def sigs_txmode(signal_received, frame):
    print ('Recipient:')
    hvdn_recipient = input()
    print ('Message:')
    hvdn_message = input()
    hvdn_message = hvdn_recipient + ":" + hvdn_message
    rf95.send(rf95.str_to_data(hvdn_message))
    rf95.wait_packet_sent()
    print('TX:' + hvdn_message)
    OLED_display('txmsg','TX:'+ hvdn_message)
    rf95.set_mode_idle


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
display.text('HVDN LoRa Pocket', 35, 0, 2)


#
# MAIN
#

# Setup Radio
rf95 = RF95(cs=gpio_rfm_cs, int_pin=gpio_rfm_irq, reset_pin=None)
rf95.set_frequency(freqmhz)
rf95.set_tx_power(txpwr)
rf95.init()

# CTRL-Z is SIGTSTP to Send, CTRL-C is SIGINT and closes program gracefully
signal.signal(signal.SIGTSTP, sigs_txmode)
signal.signal(signal.SIGINT, sigs_handler)

# Display Start Message
OLED_display('logo','HVDN LoRa Pocket')
print()
print('HVDN LoRa Pocket')
print()

# CORE LOOP - While not hearing packets check loop
while True:
    while not rf95.available():
        if not btnA.value:
            hvdn_message = call + ':' + beacon 
            rf95.send(rf95.str_to_data(hvdn_message))
            rf95.wait_packet_sent()
            OLED_display('txmsg',hvdn_message)
            rf95.set_mode_idle
        elif not btnB.value:
            hvdn_message = call
            OLED_display('logo',hvdn_message)
        elif not btnC.value:
            hvdn_message = call + ': ACK'
            rf95.send(rf95.str_to_data(hvdn_message))
            rf95.wait_packet_sent()
            OLED_display('txmsg',hvdn_message)
            rf95.set_mode_idle		    
        pass
    data = rf95.recv()
    data_rssi = str(int(rf95.last_rssi))
    data_stringed = str(data)
    data_ascii=""
    for i in data:
        data_ascii=data_ascii+chr(i)
    if (arg_hvdn_rawdata) and (arg_signal_rssi):
        datadisplay_string = 'RAW:'+ data_stringed +':RSSI:'+data_rssi
        print ('RAW:',data,':RSSI:',data_rssi)
        OLED_display('rxmsg','RAW:' + data_stringed + ' :' + data_rssi)
    elif (arg_hvdn_rawdata):
        datadisplay_string = 'RAW:'+ data_stringed
        print ('RAW:',data)
        OLED_display('rxmsg','RAW:' + data_stringed)
    elif (arg_signal_rssi):
        datadisplay_string = 'RX:'+ data_ascii +':RSSI:'+data_rssi
        print ('RX:',data_ascii,':RSSI:',data_rssi)
        OLED_display('rxmsg','RX:' + data_ascii + ' :' + data_rssi)
    else:
        print ('RX:',data_ascii)
        OLED_display('rxmsg','RX:' + data_ascii)
    print ()
display.fill(0)
display.show()
rf95.cleanup()
