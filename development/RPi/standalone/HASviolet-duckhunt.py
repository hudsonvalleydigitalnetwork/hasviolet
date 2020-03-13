#!/usr/bin/python3
#
# HASviolet Duckhunt
#
#
#  Usage: HASviolet-duckhunt.py 
#
#  DESCRIPTION
#
#     Runs on RPI Z WH startup executed from /etc/rd.local
#     Left button runs beacon, Middle button quits beacon
#     Right button receives. Must pull plug to shutoff, no reset
#
#  OPTIONS
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
import signal
import sys
import time


#
# IMPORT SETTINGS
#

config = configparser.ConfigParser()
config.sections()
config.read('HASviolet.ini')
try:
   gpio_rfm_cs = int(config["DEFAULT"]["gpio_rfm_cs"])
   gpio_rfm_irq = int(config["DEFAULT"]["gpio_rfm_irq"])
   node_address = int(config["DEFAULT"]["node_address"])
   freqmhz = float(config["DEFAULT"]["freqmhz"])
   txpwr = int(config["DEFAULT"]["txpwr"])
   modemcfg = str(config["DEFAULT"]["modemcfg"])
   mycall = str(config["DEFAULT"]["mycall"])
   ssid = str(config["DEFAULT"]["ssid"])
   beacon = str(config["DEFAULT"]["beacon"])
except KeyError as e:
   raise LookupError("Error HASviolet.ini[DEFAULT] : {} missing.".format(str(e)))
   exit (1)


#
# IMPORT ARGS
#


#
# VARIABLES
#

# gpio_rfm_irq - Use chip select 1. GPIO pin 22 will be used for interrupts
# node_address - The address of this device will be set to (1-254)
# freqmhz - The freq of this device in MHz (911.250 MHz is recommended)
# recipient - Address of receiveing node
# message - message as captured from args
# timedelay - beacon interval in seconds
# getout - used for beaking loops for mode exit detection
#

hasname = mycall + "-" + ssid
payload = hasname + " | " + message 
timedelay = 5
getout = False

#
# FUNCTIONS
#

def sigs_handler(signal_received, frame):
    # Handle any cleanup here
    print('CTRL-C detected. Exiting gracefully')
    rf95.set_mode_idle()
    rf95.cleanup()
    display.fill(0)
    display.show()
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


#
# SETUP
#

# Button A
beaconA = DigitalInOut(board.D5)
beaconA.direction = Direction.INPUT
beaconA.pull = Pull.UP
 
# Button B
btnB = DigitalInOut(board.D6)
btnB.direction = Direction.INPUT
btnB.pull = Pull.UP
 
# Button C
listenC = DigitalInOut(board.D12)
listenC.direction = Direction.INPUT
listenC.pull = Pull.UP

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
display.text('HASviolet Duckhunt', 0, 0, 2)
display.show()

# Setup Radio

#rf95 = RF95(cs=1, int_pin=22, reset_pin=None)
rf95 = RF95(cs=gpio_rfm_cs, int_pin=gpio_rfm_irq, reset_pin=None)
rf95.set_frequency(freqmhz)
rf95.set_tx_power(txpwr)
# Custom predefined mode
#rf95.set_modem_config(Bw31_25Cr48Sf512)
rf95.init()


#
# MAIN
#
while True:
    if not beaconA.value:
        while btnB.value:
            rf95.send(rf95.str_to_data(payload))
            rf95.wait_packet_sent()
            display.fill(0)
            display.text("Beaconing ...", 0, 0, 1)
            display.text(message, 5, 10, 1)
            display.show()
            time.sleep(timedelay)
        display.fill(0)
        display.text('HASviolet Duckhunt', 0, 0, 2)
        display.show()
        rf95.set_mode_idle()
        rf95.cleanup()
    if not listenC.value:
        display.fill(0)
        display.text("RX Mode ...", 0, 0, 1)
        display.show()
        while True:
            while not rf95.available():
                pass
            data = rf95.recv()
            data_rssi = str(int(rf95.last_rssi))
            data_stringed = str(data)
            data_ascii=""
            for i in data:
                data_ascii=data_ascii+chr(i)
                datadisplay_string = 'RX:'+ data_ascii +':RSSI:'+data_rssi
                OLED_display('rxmsg','RX:' + data_ascii + ' :' + data_rssi)
            display.fill(0)
            display.show()
    pass
display.fill(0)
display.show()
rf95.set_mode_idle()
rf95.cleanup()
