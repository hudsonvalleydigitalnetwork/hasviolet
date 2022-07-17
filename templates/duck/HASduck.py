#!/usr/bin/python3
#
#
# HASduck
#
#
#  Usage: HASduck.py 
#
#  DESCRIPTION
#
#     Runs as a service (systemd) or standalone
#
#  OPTIONS
#
#  RELEASE: 20220717-03000  
#
#


##
# IMPORT LIBRARIES
#

import argparse 
import json
import signal
import sys
import time
import subprocess
from HASvioletRF import HASrf
from HASvioletHID import HAShid


#
# VARIABLES
#

HASduck_VER="HASduck v1.0"
HASviolet_CONFIG = "HASviolet.json"
HASduck_CONFIG = "HASduck.json" 
HVDN_LOGO = "HVDN_logo.xbm" 

#
# OBJECTS
#

class Duckwalk:
    def __init__(self):
        self.cfgjson = HASduck_CONFIG
        with open(self.cfgjson) as configFileJson:
            jsonConfig = json.load(configFileJson)
        self.message = jsonConfig["0"]["message"]
        self.interval = jsonConfig["0"]["interval"]
        self.interval_start = time.time()
        self.interval_stop = int(self.interval_start + self.interval)
        self.trigger = jsonConfig["0"]["trigger"]         # values include bluetooth, custo, gps, none, wifi
        self.trigger_value = jsonConfig["0"]["trigger_value"]
        self.action = jsonConfig["0"]["action"]           # values include custom, next, reset, quit
        self.duration = jsonConfig["0"]["duration"]
        self.duration_start = time.time()
        self.duration_stop = int(self.duration_start + self.duration)
        return
    def trigger(self, ttype, tvalue):
        return
    def action(self, taction):
        return

HASit = HASrf()
HAShat = HAShid()
Ducky = Duckwalk()


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
    HAShat.OLED.text("  TRANSMIT",1,0,1)
    HAShat.OLED.text("  RECEIVE",1,8,1)
    HAShat.OLED.text("  DUCKHUNT",1,16,1)
    HAShat.OLED.text("  OPTIONS",1,24,1)
    HAShat.OLED.show()

def tx_menu():
    HAShat.OLED.fill(0)
    HAShat.OLED.show()
    HAShat.OLED.text(" ",0, HAShat.prevpos,1)
    HAShat.OLED.text("*",0, HAShat.currpos,1)
    HAShat.OLED.text("  TX QSL",1,0,1)
    HAShat.OLED.text("  TX QRZ",1,8,1)
    HAShat.OLED.text("  TX BEACON",1,16,1)
    HAShat.OLED.text("  RETURN",1,24,1)
    HAShat.OLED.show()

def rx_menu():
    HAShat.OLED.fill(0)
    HAShat.OLED.show()
    HAShat.OLED.text(" ",0, HAShat.prevpos,1)
    HAShat.OLED.text("*",0, HAShat.currpos,1)
    HAShat.OLED.text("  RX ALL",1,0,1)
    HAShat.OLED.text("  RX BEACONS",1,8,1)
    HAShat.OLED.text("  RX ME",1,16,1)
    HAShat.OLED.text("  RETURN",1,24,1)
    HAShat.OLED.show()

def game_menu():
    HAShat.OLED.fill(0)
    HAShat.OLED.show()
    HAShat.OLED.text(" ",0, HAShat.prevpos,1)
    HAShat.OLED.text("*",0, HAShat.currpos,1)
    HAShat.OLED.text("  SHOW DUCK",1,0,1)
    HAShat.OLED.text("  RUN DUCK",1,8,1)
    HAShat.OLED.text("  RETURN",1,16,1)
    HAShat.OLED.text("  *********",1,24,1)
    HAShat.OLED.show()

def options_menu():
    HAShat.OLED.fill(0)
    HAShat.OLED.show()
    HAShat.OLED.text(" ",0, HAShat.prevpos,1)
    HAShat.OLED.text("*",0, HAShat.currpos,1)
    HAShat.OLED.text("  ABOUT",1,0,1)
    HAShat.OLED.text("  RESTART",1,8,1)
    HAShat.OLED.text("  QUIT",1,16,1)
    HAShat.OLED.text("  RETURN",1,24,1)
    HAShat.OLED.show()

def menu_update():
    HAShat.OLED.text(" ",0, HAShat.prevpos,1)
    HAShat.OLED.text("*",0, HAShat.currpos,1)
    HAShat.OLED.show()

def restart_svc():
    HAShat.prevpos = 0
    HAShat.currpos = 0
    HAShat.menulvl="main_menu"
    main_menu()
    menu_update()
    print("restarted")

def tx_msg(message):
    HASheader = HASit.mystation + ">" + "BEACON-99"
    HASpayload = HASheader + " | " + message 
    HASit.transmit(HASpayload)
    print(HASpayload)
    HAShat.OLED.fill(0)
    HAShat.OLED.text(HASheader, 0, 0, 1)
    HAShat.OLED.text(message, 0, 10, 1)
    HAShat.OLED.show()
    time.sleep(5)
    HAShat.OLED.fill(0)
    HAShat.OLED.show()

def tx_beacon():
    HASheader = HASit.mystation + ">" + "BEACON-99"
    HASpayload = HASheader + " | " + HASit.mybeacon 
    while HAShat.btnRight.value:
        HASit.transmit(HASpayload)
        print(HASpayload)
        HAShat.OLED.fill(0)
        HAShat.OLED.text(HASheader, 0, 0, 1)
        HAShat.OLED.text(HASit.mybeacon , 0, 10, 1)
        HAShat.OLED.show()
        time.sleep(5)
        HAShat.OLED.fill(0)
        HAShat.OLED.show()
    time.sleep(0.25)

def rx_msg_rfm9x(whom):
    breakbad = 0
    while True:
        while not HASit.rfm.available():
            if breakbad == 1:
                break
            if not HAShat.btnRight.value:
                breakbad = 1
                break
        if breakbad == 1:
                break
        HASit.receive = HASit.rfm.recv()
        HASit.receive_rssi = str(int(HASit.rfm.last_rssi))
        HASit.receive_string = str(HASit.receive)
        HASit.receive_ascii=""
        for i in HASit.receive:
            HASit.receive_ascii=HASit.receive_ascii+chr(i)
        (HASit.header, HASit.payload) = HASit.receive_ascii.split("|")
        (HASit.source, HASit.destination) = HASit.header.split(">")
        if whom == 'all':
            print (HASit.receive_ascii,':RSSI:',HASit.receive_rssi)
            HAShat.OLED.fill(0)
            HAShat.OLED.show()
            HAShat.OLED.text(HASit.header, 0, 0, 1)
            HAShat.OLED.text(HASit.payload, 0, 10, 1)
            HAShat.OLED.text("RSSI: " + HASit.receive_rssi, 0, 20, 1)
            HAShat.OLED.show()
        if (whom == 'BEACON-99') and (HASit.destination == 'BEACON-99'):
            print (HASit.receive_ascii,':RSSI:',HASit.receive_rssi)
            HAShat.OLED.fill(0)
            HAShat.OLED.show()
            HAShat.OLED.text(HASit.header, 0, 0, 1)
            HAShat.OLED.text(HASit.payload, 0, 10, 1)
            HAShat.OLED.text("RSSI: " + HASit.receive_rssi, 0, 20, 1)
            HAShat.OLED.show()
        if (whom == HASit.destination) and (HASit.destination == HASit.mystation):
            print (HASit.receive_ascii,':RSSI:',HASit.receive_rssi)
            HAShat.OLED.fill(0)
            HAShat.OLED.show()
            HAShat.OLED.text(HASit.header, 0, 0, 1)
            HAShat.OLED.text(HASit.payload, 0, 10, 1)
            HAShat.OLED.text("RSSI: " + HASit.receive_rssi, 0, 20, 1)
            HAShat.OLED.show()
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

def duckhunt(subpop):   
    if subpop == "show":
        print("Duckhunt Show")
        print("message", Ducky.message)
        print("interval", Ducky.interval)
        print("trigger " + Ducky.trigger + " " + Ducky.trigger_value)
        print("action " + Ducky.action)
        print("duration", Ducky.duration)
        HAShat.OLED.fill(0)
        HAShat.OLED.text("message " + str(Ducky.message), 0, 0, 1)
        HAShat.OLED.text("interval " + str(Ducky.interval), 0, 8, 1)
        HAShat.OLED.text("trigger " + Ducky.trigger + " " + Ducky.trigger_value, 0, 16, 1)
        HAShat.OLED.text("action " + Ducky.action, 0, 24, 1)
        HAShat.OLED.text("duration " + str(Ducky.duration), 0, 32, 1)
        HAShat.OLED.show()
        time.sleep(5)
        HAShat.OLED.fill(0)
        HAShat.OLED.show()
        return

    HASheader = HASit.mystation + ">" + "BEACON-99"
    HASpayload = HASheader + " | " + Ducky.message

    while (time.time() < Ducky.duration_stop):
        if not HAShat.btnRight.value:
            break
        if Ducky.trigger != "none":                            # If there is a TRIGGER
            Ducky.trigger(Duck.trigger, Duck.trigger_value)    # Call DUCKY.TRIGGER FUNCTION
            Ducky.action()                                          # then call ACTION
        HASit.transmit(HASpayload)
        print(HASpayload)
        HAShat.OLED.fill(0)
        HAShat.OLED.text(HASheader, 0, 0, 1)
        HAShat.OLED.text(Ducky.message, 0, 10, 1)
        HAShat.OLED.show()
        time.sleep(Ducky.interval)
        HAShat.OLED.fill(0)
        HAShat.OLED.show()
    restart_svc()
    time.sleep(0.25)


#
# MAIN
#

HAShat.logo(HVDN_LOGO)

# CTRL-C is SIGINT and closes program gracefully
signal.signal(signal.SIGINT, sigs_handler)
signal.signal(signal.SIGTERM, sigs_handler)

# RF and LoRa Config init
HASit.startradio()                                  # rf95 library

HAShat.prevpos = 0                                  # Tracking OLED cursor Y position          
HAShat.currpos = 0                                  # Tracking OLED cursor Y position          
HAShat.menulvl="main_menu"                          # Current Menu
main_menu()
menu_update()
firstoledline = 0                                   # First OLED Line position (Y)
lastoledline = 24                                   # Last OLED Line position (Y)

while True:
    #print(HAShat.menulvl, HAShat.currpos)
    if not HAShat.btnLeft.value:                    # Move cursor with left button
        time.sleep(0.025)                           # Inserted to debounce button press
        if not HAShat.btnLeft.value:                # Left button definitely pressed
            if HAShat.currpos >= lastoledline:      # If cursor on last OLED line
                HAShat.currpos = firstoledline      #  - then move cursor to first OLED line
                HAShat.prevpos = lastoledline       #  - and then remember the cursor position as last oled line
            else: 
                HAShat.prevpos = HAShat.currpos     # Else we first remember what the current cursor position is
                HAShat.currpos = HAShat.currpos + 8 #  - and advance the cursor position to the next OLED line
            
            if HAShat.menulvl == "main_menu":       # Given MENULEVEL, display that MENU
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
    if not HAShat.btnMid.value:                                             # Selection within a menu using middle button
        time.sleep(.025)                                                    # Inserted to debounce button press
        if not HAShat.btnMid.value:                                         # Middle button definitely pressed
            if HAShat.menulvl == "main_menu" and HAShat.currpos == 0:       # If the current menu is MAIN and our cursor is next to TRANSMIT 
                HAShat.menulvl = "tx_menu"                                  # - change MENULVL to TRANSMIT
                HAShat.prevpos = 0
                HAShat.currpos == 0                                         # - reset cursor position to first OLED line
                tx_menu()                                                   # - Display TRANSMIT menu
            elif HAShat.menulvl == "main_menu" and HAShat.currpos == 8:     # Else If the current menu is MAIN and our cursor is next to RECEIVE 
                HAShat.menulvl = "rx_menu"                                  # - change MENULVL to RECEIVE
                HAShat.prevpos = 0
                HAShat.currpos = 0                                         # - reset cursor position to first OLED line
                rx_menu()                                                   # - Display RECEIVE menu
            elif HAShat.menulvl == "main_menu" and HAShat.currpos == 16:    # Else If the current menu is MAIN and our cursor is next to DUCKHUNT
                HAShat.menulvl = "game_menu"                                # - change MENULVL to DUCKHUNT
                HAShat.prevpos = 0
                HAShat.currpos = 0                                         # - reset cursor position to first OLED line
                game_menu()                                                 # - Display DUCKHUNT menu
            elif HAShat.menulvl == "main_menu" and HAShat.currpos == 24:    # Else If the current menu is MAIN and our cursor is next to OPTIONS
                HAShat.menulvl = "options_menu"                             # - change MENULVL to OPTIONS
                HAShat.prevpos = 0
                HAShat.currpos = 0                                         # - reset cursor position to first OLED line
                options_menu()                                              # - Display OPTIONS menu        
 
            elif HAShat.menulvl == "tx_menu" and HAShat.currpos == 0:       # If the current menu is TRANSMIT and our cursor is next to TX QSL
                tx_msg(' QSL ')                                             # - Transmit the message QSL
                HAShat.prevpos = 0
                HAShat.currpos = 0                                         # - reset cursor position to first OLED line
                HAShat.menulvl = "tx_menu"
                tx_menu()                                                   
            elif HAShat.menulvl == "tx_menu" and HAShat.currpos == 8:       # If the current menu is TRANSMIT and our cursor is next to TX QRZ
                tx_msg(' QRZ ')                                             # - Transmit the message QRZ
                HAShat.prevpos = 0
                HAShat.currpos = 0                                         # - reset cursor position to first OLED line
                HAShat.menulvl = "tx_menu"
                tx_menu()  
            elif HAShat.menulvl == "tx_menu" and HAShat.currpos == 16:      # If the current menu is TRANSMIT and our cursor is next to TX BEACON
                tx_beacon()                                                 # - Transmit the BEACON message HASit.mybeacon loaded from HASviolet.json
                HAShat.prevpos = 0
                HAShat.currpos = 0                                         # - reset cursor position to first OLED line
                HAShat.menulvl = "tx_menu"
                tx_menu()  
            elif HAShat.menulvl == "tx_menu" and HAShat.currpos == 24:      # If the current menu is TRANSMIT and our cursor is next to RETURN
                HAShat.prevpos = 0
                HAShat.currpos = 0                                         # - reset cursor position to first OLED line
                HAShat.menulvl = "main_menu"
                main_menu() 

            elif HAShat.menulvl == "rx_menu" and HAShat.currpos == 0:       # If the current menu is RECEIVE and our cursor is next to RX ALL
                HAShat.OLED.fill(0)                                         # - Clear OLED display
                HAShat.OLED.show()
                HAShat.OLED.text('RX ALL...', 1, 0, 1)                      # - Say what mode we are in 
                HAShat.OLED.show()
                time.sleep(1)
                rx_msg_rfm9x('all')                                         # - Run RECEIVE with no filtering of output. Function returns on right button press
                HAShat.prevpos = 0
                HAShat.currpos = 0                                         # - reset cursor position to first OLED line
                HAShat.menulvl = "rx_menu"
                rx_menu()                                                   # - refresh OLED to put in known menu state
            elif HAShat.menulvl == "rx_menu" and HAShat.currpos == 8:       # If the current menu is RECEIVE and our cursor is next to RX BEACONS
                HAShat.OLED.fill(0)                                         # - Clear OLED display
                HAShat.OLED.show()
                HAShat.OLED.text('RX BEACONS...', 1, 0, 1)                  # - Say what mode we are in 
                HAShat.OLED.show()
                time.sleep(1)
                rx_msg_rfm9x('BEACON-99')                                   # - Run RECEIVE with filtering on BEACON-99. Function returns on right button press
                HAShat.prevpos = 0
                HAShat.currpos == 0                                         # - reset cursor position to first OLED line
                HAShat.menulvl == "rx_menu"
                rx_menu()                                                   # - refresh OLED to put in known menu state
            elif HAShat.menulvl == "rx_menu" and HAShat.currpos == 16:      # If the current menu is RECEIVE and our cursor is next to RX ME
                HAShat.OLED.fill(0)                                         # - Clear OLED display
                HAShat.OLED.show()
                HAShat.OLED.text('RX ME...', 1, 0, 1)                       # - Say what mode we are in 
                HAShat.OLED.show()
                time.sleep(1)
                rx_msg_rfm9x(HASit.mystation)                               # - Run RECEIVE with filtering on your call HAS.mystation. Function returns on right button press
                HAShat.prevpos = 0
                HAShat.currpos = 0                                         # - reset cursor position to first OLED line
                HAShat.menulvl = "rx_menu"
                rx_menu()                                                   # - refresh OLED to put in known menu state
            elif HAShat.menulvl == "rx_menu" and HAShat.currpos == 24:      # If the current menu is RECEIVE and our cursor is next to RETURN
                HAShat.prevpos = 0
                HAShat.currpos = 0                                         # - reset cursor position to first OLED line
                HAShat.menulvl = "main_menu"
                main_menu() 

            elif HAShat.menulvl == "game_menu" and HAShat.currpos == 0:     # If the current menu is DUCKHUNT and our cursor is next to SHOW DUCK
                HAShat.OLED.fill(0)                                         # - Clear OLED display
                HAShat.OLED.show()
                duckhunt("show")
                HAShat.prevpos = 0
                HAShat.currpos = 0                                          # - reset cursor position to first OLED line
                HAShat.menulvl = "game_menu"
                game_menu()                                                 # - refresh OLED to put in known menu state
            elif HAShat.menulvl == "game_menu" and HAShat.currpos == 8:     # If the current menu is DUCKHUNT and our cursor is next to RUN DUCK
                HAShat.OLED.fill(0)                                         # - Clear OLED display
                HAShat.OLED.show()
                duckhunt("run")
                HAShat.prevpos = 0
                HAShat.currpos = 0                                          # - reset cursor position to first OLED line
                HAShat.menulvl = "game_menu"
                game_menu()                                                 # - refresh OLED to put in known menu state                                           # - refresh OLED to put in known menu state
            elif HAShat.menulvl == "game_menu" and HAShat.currpos == 16:    # If the current menu is DUCKHUNT and our cursor is next to RETURN
                HAShat.prevpos = 0
                HAShat.currpos = 0     
                HAShat.menulvl = "main_menu"                               # - Go up one menu level which will be MAIN MENU
                main_menu()
            elif HAShat.menulvl == "game_menu" and HAShat.currpos == 24:    # If the current menu is DUCKHUNT and our cursor is next to ******
                HAShat.prevpos = 0
                HAShat.currpos = 0     
                HAShat.menulvl = "main_menu"                               # - Go up one menu level which will be MAIN MENU
                main_menu()

            elif HAShat.menulvl == "options_menu" and HAShat.currpos == 0:  # If the current menu is OPTIONS and our cursor is next to ABOUT
                print(HASduck_VER)
                HAShat.OLED.fill(0)
                HAShat.OLED.text(HASduck_VER, 0, 10, 1)
                HAShat.OLED.show()
                time.sleep(3)
                HAShat.OLED.fill(0)
                HAShat.OLED.show()
                HAShat.prevpos = 0
                HAShat.currpos == 0                                         # - reset cursor position to first OLED line
                HAShat.menulvl = "options_menu"
                options_menu() 
            elif HAShat.menulvl == "options_menu" and HAShat.currpos == 8:  # If the current menu is OPTIONS and our cursor is next to RESTART
                HAShat.OLED.fill(0)                                         # - Clear OLED display for shaneless logo display
                HAShat.OLED.show()
                HAShat.logo(HVDN_LOGO)                                       # - Display HVDN logo
                restart_svc()                                               # - refresh OLED to put in known menu state
            elif HAShat.menulvl == "options_menu" and HAShat.currpos == 16: # If the current menu is OPTIONS and our cursor is next to QUIT
                HASit.cleanup()                                             # - Shutdown RF module properly
                HAShat.OLED.fill(0)                                         # - Clear OLED display for Goodby message
                HAShat.OLED.show()
                HAShat.OLED.text('Goodbye...', 0, 10, 1)                    # - Say Goodbye
                HAShat.OLED.show()
                time.sleep(2)
                HAShat.OLED.fill(0)                                         # - Clear OLED display
                HAShat.OLED.show()
                exit(0)
            elif HAShat.menulvl == "options_menu" and HAShat.currpos == 24: # If the current menu is OPTIONS and our cursor is next to RETURN
                HAShat.prevpos = 0
                HAShat.currpos = 0                                         # - reset cursor position to first OLED line
                HAShat.menulvl = "main_menu"
                main_menu() 
                       
            else:
                pass
    
    if not HAShat.btnRight.value:
       time.sleep(0.025)
       if not HAShat.btnRight.value:
           restart_svc()