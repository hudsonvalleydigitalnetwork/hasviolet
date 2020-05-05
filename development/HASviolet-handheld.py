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
    print('SIGINT or CTRL-C detected. Exiting gracefully')
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
    HAShat.OLED.text("  GAME",1,24,1)
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

def game_menu():
    HAShat.OLED.fill(0)
    HAShat.OLED.show()
    HAShat.OLED.text(" ",0, HAShat.prevpos,1)
    HAShat.OLED.text("*",0, HAShat.currpos,1)
    HAShat.OLED.text("= GAME =",1,0,1)
    HAShat.OLED.text("  VASILI",1,8,1)
    HAShat.OLED.text("  DUCKHNT",1,16,1)
    HAShat.OLED.text("  3DCHESS",1,24,1)
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

def tx_qsl():
    print("8x8 Sending a TX QSL")

def tx_qrz():
    print("8x16 Sending a TX QRZ")

def tx_beacon():
    print("8x24 Sending a TX BEACON")

def rx_all():
    print("16x8 RXALL")

def rx_beacons():
    print("16x16 RX Beacons")

def rx_forme():
    print("16x24 RX just for me")

def vasili():
    print("24x8 One ping only")

def duckhunt():
    print("24x16 Quack Quack -- BOOM")

def threedchess():
    print("24x24 3D Chess")

#
# MAIN
#

HAShat.logo('hvdn-logo.xbm')

# CTRL-C is SIGINT and closes program gracefully
signal.signal(signal.SIGINT, sigs_handler)

HAShat.prevpos = 8
HAShat.currpos = 8
HAShat.menulvl="main_menu"
main_menu()
menu_update()
firstoledline = 8
lastoledline = 32

while True:
    if not HAShat.btnLeft.value:
        time.sleep(0.05)
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
            elif HAShat.menulvl == "game_menu":
                game_menu()
            else:
                pass
    time.sleep(.025)
    if not HAShat.btnMid.value:
        time.sleep(.05)
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
                HAShat.menulvl = "game_menu"
                HAShat.currpos == 8
                game_menu()
            elif HAShat.menulvl == "tx_menu" and HAShat.currpos == 8:
                tx_qsl()
                restart_svc()
            elif HAShat.menulvl == "tx_menu" and HAShat.currpos == 16:
                tx_qrz()
                restart_svc()
            elif HAShat.menulvl == "tx_menu" and HAShat.currpos == 24:
                tx_beacon()
                restart_svc()
            elif HAShat.menulvl == "rx_menu" and HAShat.currpos == 8:
                rx_all()
                restart_svc()
            elif HAShat.menulvl == "rx_menu" and HAShat.currpos == 16:
                rx_beacons()
                restart_svc()
            elif HAShat.menulvl == "rx_menu" and HAShat.currpos == 24:
                rx_forme()
                restart_svc()
            elif HAShat.menulvl == "game_menu" and HAShat.currpos == 8:
                vasili()
                restart_svc()
            elif HAShat.menulvl == "game_menu" and HAShat.currpos == 16:
                duckhunt()
                restart_svc()
            elif HAShat.menulvl == "game_menu" and HAShat.currpos == 24:
                threedchess()
                restart_svc()
            else:
                pass
    time.sleep(0.25)
    if not HAShat.btnRight.value:
       time.sleep(0.05)
       if not HAShat.btnRight.value:
           restart_svc()
    time.sleep(0.25)
