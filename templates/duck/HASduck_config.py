#!/usr/bin/python3
#
# HASduck Config
#
#
# Usage: HASduck_config.py
#
#
#  20210303-1300
#


#
# Import Libraries
#

import argparse 
import configparser
import json
import os
import sys
import time


#
# STATICS
#

HASviolet_RXLOCK = False                                               # True = RX is running
HASviolet_TXLOCK = False                                               # True = TX is running
HASviolet_LOCAL = "/home/pi/hasviolet-local/"                          # Config file is in JSON format
HASviolet_SERVER = HASviolet_LOCAL + "server/"                         # Path to files. Change when Pi
HASviolet_ETC = HASviolet_LOCAL + "etc/"                               # Config file is in JSON format
HASviolet_CONFIG = HASviolet_ETC + "HASviolet.json"                    # Config file is in JSON format
HASviolet_SSL_KEY = HASviolet_ETC + "HASviolet.key"                    # SSL Key
HASviolet_SSL_CRT = HASviolet_ETC + "HASviolet.crt"                    # Cert Key
HASviolet_PWF = HASviolet_ETC + "HASviolet.pwf"                        # Password file  user:hashedpasswd
HASviolet_MSGS = HASviolet_SERVER + "msgs/HASviolet.msgs"              # radio writes msgs received here   
HASviolet_LOGIN = HASviolet_SERVER + "HASviolet_LOGIN.html"
HASviolet_LOGINCSS = HASviolet_SERVER + "HASviolet_LOGIN.css"
HASviolet_INDEX = HASviolet_SERVER + "HASviolet_INDEX.html"
HASviolet_INDEXCSS = HASviolet_SERVER + "HASviolet.css"
HASvioletjs = HASviolet_SERVER + "HASviolet.js"
HVDN_LOGO = HASviolet_ETC + "HVDN_logo.xbm"


#
# VARIABLES
#

HASduck_VER="HASduck v1.0"
HASviolet_CONFIG = "HASviolet.json"
HASduck_CONFIG = "HASduck.json" 
HVDN_LOGO = "HVDN_logo.xbm" 


#
# CLASSES
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


#
# FUNCTIONS
#

def main_menu():
    os.system("clear")
    print ()
    print ('- - - - - HASduck Config Tool - - - - -')
    print ()
    print ('  1         Message ',Ducky.message)
    print ('  2        Interval ',Ducky.interval)
    print ('  3         Trigger ',Ducky.trigger, Ducky.trigger_value)
    print ('  4          Action ',Ducky.action)
    print ('  5        Duration ',Ducky.duration)
    print ()
    print ('- - - - - - - - - - - - - - - -')
    print()
    print ('  9     Quick Guide ')
    print (' 99   Write changes ')
    print ('  0       Exit Menu ')
    print ()
    fun = input('Select option: ')  
    if fun=="1":
        setducky_message()
    elif fun=="2":
        setducky_interval()
    elif fun=="3":
        setducky_trigger()
    elif fun=="4":
        setducky_action()
    elif fun=="5":
        setducky_duration()
    elif fun=="9":
        show_quickguide()
    elif fun=="99":
        write_changes()
    elif fun=="0":
        exit(0)
    else:
        print ("Programmer error: unrecognized option")
    pass

def setducky_message():
    print ()
    print ('--')
    Ducky.message = input('-- Enter message: ')
    return

def setducky_interval():
    print ()
    print ('--')
    Ducky.interval = input('Enter seconds between message being sent: ')
    return

def setducky_trigger():
    print ()
    print ('-- Trigger Type: ')  
    print ('-- ')  
    funnier = input('-- (b)luetooth, (c)ustom, (g)ps, (n)one, or (w)ifi: ')
    if funnier=="b":
        Ducky.trigger = "bluetooth"
        Ducky.trigger_value = input('-- Value: ')
    elif funnier=="c":
        Ducky.trigger = "custom"
        Ducky.trigger_value = input('-- Value: ')
    elif funnier=="g":
        Ducky.trigger = "gps"
        Ducky.trigger_value = input('-- Value: ')
    elif funnier=="n":
        Ducky.trigger = "none"
        Ducky.trigger_value = "0"
    elif funnier=="w":
        Ducky.trigger = "wifi"
        Ducky.trigger_value = input('-- Value: ')
    else:
        print ("Programmer error: unrecognized option")
        Ducky.trigger = "none"
        Ducky.trigger_value = "0"
    return

def setducky_action():
    print ()
    print ('-- Action Type: ')  
    print ('-- ')
    funnier = input('-- (c)ustom, (n)ext, (r)eset, or (q)uit: ')
    if funnier=="c":
        Ducky.action = "custom"
    elif funnier=="n":
        Ducky.action = "next"
    elif funnier=="r":
        Ducky.action = "reset"
    elif funnier=="q":
        Ducky.action = "quit"
    else:
        print ("Programmer error: unrecognized option")
        Ducky.action = "reset"
    return

def setducky_duration():
    print ()
    print ('--')
    Ducky.duration = input('Enter duration of beacon in seconds: ')
    return

def show_quickguide():
    os.system("clear")
    print ()
    print ('HASduck Framework')
    print ()
    print ('To make this a smart beacon we have created a short command set, order specific, all lower case:')
    print ()
    print (' message ')
    print ('      then followed with whatever your message is. No quotes required')
    print ()
    print (' interval')
    print ('      followed with number of seconds between message transmissions')
    print ()
    print (' trigger')
    print ('      during countdown to the next interval, a trigger can be set. Trigger values include')
    print ('      when signals are detected (wifi or bluetooth), current GPS location and custom triggers')
    print ('      can be written in Python.')
    print ()
    print (' action ')
    print ('      given a trigger, what action can be taken. This includes reset, next, custom, quit')
    print ()
    print (' duration')
    print ('      How long in seconds until the beacon stops')
    print ()
    print ('NOTE: Trigger types and actions have yet to be coded. For now beacon runs for interval and duration')
    print ('specified.')
    print ()
    print ()
    programPause = input("Press the <ENTER> key to continue...")
    return   

def write_changes():
    with open(Ducky.cfgjson) as configReadFile:
        data = json.load(configReadFile)
    time.sleep(3)           
    data["0"]["message"] = Ducky.message
    data["0"]["interval"] = int(Ducky.interval)
    data["0"]["trigger"] = Ducky.trigger
    data["0"]["trigger_value"] = Ducky.trigger_value
    data["0"]["action"] = Ducky.action
    data["0"]["duration"] = int(Ducky.duration)
    print ('Updating HASduck.json')
    with open(Ducky.cfgjson, 'w') as configWriteFile:
        json.dump(data, configWriteFile, indent=3)
    time.sleep(3)

    
#
# SETUP
#

#
# OBJECTS
#

Ducky = Duckwalk()

#
# MAIN
#


while True:
    main_menu()  