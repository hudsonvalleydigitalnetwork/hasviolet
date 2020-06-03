#!/usr/bin/python3
#
#
# HASviolet Handheld  
#
#
#  Usage: HASviolet-handheld.py 
#
#  DESCRIPTION
#
#     Runs as a service (systemd) or standalone
#
#  OPTIONS
#
#  
#  RELEASE: BERMUDA
#


#
# Import Libraries
#

import argparse 
import configparser
import curses
import signal
import sys
import time
import subprocess
from HASvioletRF import HASrf
from HASvioletHID import HAShid


#
# Initialise HASviolet
#

HASit = HASrf()
HAShat = HAShid()


#
# FUNCTIONS
#

def sigs_handler(signal_received, frame):
    # Handle any cleanup here
    print('Exiting gracefully')
    HASit.cleanup()
    HAShat.OLED.fill(0)
    HAShat.OLED.show()
    HAShat.OLED.text('Goodbye...', 0, 10, 1)
    HAShat.OLED.show()
    time.sleep(2)
    HAShat.OLED.fill(0)
    HAShat.OLED.show()
    exit(0)

def main_menu():
    HAShat.OLED.fill(0)
    HAShat.OLED.show()
    HAShat.OLED.text(" ",0, HAShat.prevpos,1)
    HAShat.OLED.text("*",0, HAShat.currpos,1) 
    HAShat.OLED.text("= MAIN MENU =",1,0,1)
    HAShat.OLED.text("  TRANSMIT",1,8,1)
    HAShat.OLED.text("  RECEIVE",1,16,1)
    HAShat.OLED.text("  OPTIONS",1,24,1)
    HAShat.OLED.show()

def tx_menu():
    HAShat.OLED.fill(0)
    HAShat.OLED.show()
    HAShat.OLED.text(" ",0, HAShat.prevpos,1)
    HAShat.OLED.text("*",0, HAShat.currpos,1)
    HAShat.OLED.text("= TRANSMIT =",1,0,1)
    HAShat.OLED.text("  QSL",1,8,1)
    HAShat.OLED.text("  QRZ",1,16,1)
    HAShat.OLED.text("  BEACON",1,24,1)
    HAShat.OLED.show()

def rx_menu():
    HAShat.OLED.fill(0)
    HAShat.OLED.show()
    HAShat.OLED.text(" ",0, HAShat.prevpos,1)
    HAShat.OLED.text("*",0, HAShat.currpos,1)
    HAShat.OLED.text("= RECEIVE =",1,0,1)
    HAShat.OLED.text("  ALL",1,8,1)
    HAShat.OLED.text("  BEACONS",1,16,1)
    HAShat.OLED.text("  FOR ME",1,24,1)
    HAShat.OLED.show()

def options_menu():
    HAShat.OLED.fill(0)
    HAShat.OLED.show()
    HAShat.OLED.text(" ",0, HAShat.prevpos,1)
    HAShat.OLED.text("*",0, HAShat.currpos,1)
    HAShat.OLED.text("= OPTIONS =",1,0,1)
    HAShat.OLED.text("  DUCKHUNT",1,8,1)
    HAShat.OLED.text("  ABOUT",1,16,1)
    HAShat.OLED.text("  QUIT",1,24,1)
    HAShat.OLED.show()

def game_menu():
    HAShat.OLED.fill(0)
    HAShat.OLED.show()
    HAShat.OLED.text(" ",0, HAShat.prevpos,1)
    HAShat.OLED.text("*",0, HAShat.currpos,1)
    HAShat.OLED.text("= DUCKHUNT =",1,0,1)
    HAShat.OLED.text("  SIMPLE",1,8,1)
    HAShat.OLED.text("  HARDER",1,16,1)
    HAShat.OLED.text("  HARDCORE",1,24,1)
    HAShat.OLED.show()

def menu_update():
    HAShat.OLED.text(" ",0, HAShat.prevpos,1)
    HAShat.OLED.text("*",0, HAShat.currpos,1)
    HAShat.OLED.show()

def restart_svc():
    HAShat.prevpos = 8
    HAShat.currpos = 8
    HAShat.menulvl="main_menu"
    main_menu()
    menu_update()
    print("restarted")

def tx_msg(message):
    hasvheader = HASit.station + ">" + "BEACON-99"
    hasvpayload = hasvheader + " | " + message 
    HASit.tx(hasvpayload)
    print(hasvpayload)
    HAShat.OLED.fill(0)
    HAShat.OLED.text(hasvheader, 0, 1, 1)
    HAShat.OLED.text(message, 0, 9, 1)
    HAShat.OLED.show()
    time.sleep(5)
    HAShat.OLED.fill(0)
    HAShat.OLED.show()

def tx_beacon(message):
    hasvheader = HASit.station + ">" + "BEACON-99"
    hasvpayload = hasvheader + " | " + message 
    while HAShat.btnRight.value:
        HASit.tx(hasvpayload)
        print(hasvpayload)
        HAShat.OLED.fill(0)
        HAShat.OLED.text(hasvheader, 0, 1, 1)
        HAShat.OLED.text(message, 0, 9, 1)
        HAShat.OLED.show()
        time.sleep(5)
        HAShat.OLED.fill(0)
        HAShat.OLED.show()
    restart_svc()
    time.sleep(0.25)

def rx_oled_scroll():
    HAShat.OLED.fill(0)
    HAShat.OLED.show()
    HASit.ppayload = HASit.receive_ascii.split("|")
    HAShat.OLED.fill(0)
    HAShat.OLED.show()
    HAShat.OLED.text(HASit.ppayload[0], 0, 1, 1)
    HAShat.OLED.text("RSSI: " + HASit.receive_rssi, 0, 9, 1)
    HAShat.OLED.text(HASit.ppayload[1], 0, 17, 1)
    HAShat.OLED.show()

def game_simple():
    print("Simple")
    config = configparser.ConfigParser()
    config.sections()
    config.read('HASviolet-duckhunt.ini')
    try:
        duck_simple_message = str(config["SIMPLE"]["message"])
        duck_simple_interval = int(config["SIMPLE"]["interval"])
    except KeyError as e:
        raise LookupError("Error HASviolet-duckhunt.ini : {} missing.".format(str(e)))
        exit (1)
    hasvheader = HASit.station + ">" + "BEACON-99"
    hasvpayload = hasvheader + " | " + duck_simple_message 
    while HAShat.btnRight.value:
        HASit.tx(hasvpayload)
        print(hasvpayload)
        HAShat.OLED.fill(0)
        HAShat.OLED.text(hasvheader, 0, 1, 1)
        HAShat.OLED.text(duck_simple_message, 0, 9, 1)
        HAShat.OLED.show()
        time.sleep(duck_simple_interval)
        HAShat.OLED.fill(0)
        HAShat.OLED.show()
    restart_svc()
    time.sleep(0.25)

def game_harder():
    print("Harder")
    config = configparser.ConfigParser()
    config.sections()
    config.read('HASviolet-duckhunt.ini')
    try:
        duck_harder_message = str(config["HARDER"]["message"])
        duck_harder_interval = int(config["HARDER"]["interval"])
        duck_harder_message2 = str(config["HARDER"]["message2"])
        duck_harder_interval2 = int(config["HARDER"]["interval2"])
    except KeyError as e:
        raise LookupError("Error HASviolet-duckhunt.ini : {} missing.".format(str(e)))
        exit (1)
    hasvheader = HASit.station + ">" + "BEACON-99"
    hasvpayload = hasvheader + " | " + duck_harder_message 
    while HAShat.btnRight.value:
        HASit.tx(hasvpayload)
        print(hasvpayload)
        HAShat.OLED.fill(0)
        HAShat.OLED.text(hasvheader, 0, 1, 1)
        HAShat.OLED.text(duck_harder_message , 0, 9, 1)
        HAShat.OLED.show()
        time.sleep(duck_harder_interval)
        HAShat.OLED.fill(0)
        HAShat.OLED.show()
    restart_svc()
    time.sleep(0.25)

def game_hardcore():
    print("Hardcore")
    while HAShat.btnRight.value:
        print("Hardcore coming soon!")
        HAShat.OLED.fill(0)
        HAShat.OLED.text("Hardcore coming soon!", 0, 9, 1)
        HAShat.OLED.show()
        time.sleep(3)
        HAShat.OLED.fill(0)
        HAShat.OLED.show()
    restart_svc()
    time.sleep(0.25)

#
# MAIN
#

HAShat.logo('hvdn-logo.xbm')

# CTRL-C is SIGINT and closes program gracefully
signal.signal(signal.SIGINT, sigs_handler)
signal.signal(signal.SIGTERM, sigs_handler)

HAShat.prevpos = 8
HAShat.currpos = 8
HAShat.menulvl="main_menu"
main_menu()
menu_update()
firstoledline = 8
lastoledline = 32

while True:
    #print(HAShat.menulvl, HAShat.currpos)
    if not HAShat.btnLeft.value:
        time.sleep(0.025)
        if not HAShat.btnLeft.value:
            if HAShat.currpos == lastoledline:
                HAShat.currpos = firstoledline
                HAShat.prevpos = lastoledline
            else: 
                HAShat.prevpos = HAShat.currpos
                HAShat.currpos = HAShat.currpos + 8
            if HAShat.menulvl == "main_menu": 
                main_menu() 
            elif HAShat.menulvl == "tx_menu":
                tx_menu()
            elif HAShat.menulvl == "rx_menu":
                rx_menu()
            elif HAShat.menulvl == "options_menu":
                options_menu()
            elif HAShat.menulvl == "game_menu":
                game_menu()
            else:
                pass
    if not HAShat.btnMid.value:
        time.sleep(.025)
        if not HAShat.btnMid.value: 
            if HAShat.menulvl == "main_menu" and HAShat.currpos == 8:
                HAShat.menulvl = "tx_menu"
                HAShat.currpos == 8
                tx_menu()
            elif HAShat.menulvl == "main_menu" and HAShat.currpos == 16:
                HAShat.menulvl = "rx_menu"
                HAShat.currpos == 8
                rx_menu()
            elif HAShat.menulvl == "main_menu" and HAShat.currpos == 24:
                HAShat.menulvl = "options_menu"
                HAShat.currpos == 8
                options_menu()
            elif HAShat.menulvl == "tx_menu" and HAShat.currpos == 8:
                tx_msg(' QSL ')
                restart_svc()
            elif HAShat.menulvl == "tx_menu" and HAShat.currpos == 16:
                tx_msg(' QRZ ')
                restart_svc()
            elif HAShat.menulvl == "tx_menu" and HAShat.currpos == 24:
                tx_beacon(HASit.beacon)
                restart_svc()
            elif HAShat.menulvl == "rx_menu" and HAShat.currpos == 8:
                HAShat.OLED.fill(0)
                HAShat.OLED.show()
                rx_msg('all')
                restart_svc()
            elif HAShat.menulvl == "rx_menu" and HAShat.currpos == 16:
                HAShat.OLED.fill(0)
                HAShat.OLED.show()
                rx_msg('BEACON-99')
                restart_svc()
            elif HAShat.menulvl == "rx_menu" and HAShat.currpos == 24:
                HAShat.OLED.fill(0)
                HAShat.OLED.show()
                rx_msg(HASit.station)
                restart_svc()
            elif HAShat.menulvl == "options_menu" and HAShat.currpos == 8:
                HAShat.menulvl = "game_menu"
                HAShat.currpos == 8
                game_menu()
            elif HAShat.menulvl == "options_menu" and HAShat.currpos == 16:
                HAShat.OLED.fill(0)
                HAShat.OLED.show()
                HAShat.logo('hvdn-logo.xbm')
                restart_svc()
            elif HAShat.menulvl == "options_menu" and HAShat.currpos == 24:
                HASit.cleanup()
                HAShat.OLED.fill(0)
                HAShat.OLED.show()
                HAShat.OLED.text('Goodbye...', 0, 10, 1)
                HAShat.OLED.show()
                time.sleep(2)
                HAShat.OLED.fill(0)
                HAShat.OLED.show()
                exit(0)
            elif HAShat.menulvl == "game_menu" and HAShat.currpos == 8:
                HAShat.OLED.fill(0)
                HAShat.OLED.show()
                game_simple()
                restart_svc()
            elif HAShat.menulvl == "game_menu" and HAShat.currpos == 16:
                HAShat.OLED.fill(0)
                HAShat.OLED.show()
                game_harder()
                restart_svc()
            elif HAShat.menulvl == "game_menu" and HAShat.currpos == 24:
                HAShat.OLED.fill(0)
                HAShat.OLED.show()
                game_hardcore()
                restart_svc()
            else:
                pass
    if not HAShat.btnRight.value:
       time.sleep(0.025)
       if not HAShat.btnRight.value:
           restart_svc()