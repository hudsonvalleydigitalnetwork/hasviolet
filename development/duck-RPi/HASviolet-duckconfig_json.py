#!/usr/bin/python3
#
# HASviolet-duckconfig
#
#
# Usage: HASviolet-duckconfig.py
#
#  OPTIONS
#      -h, --help      show this help message and exit
#
#
#  RELEASE: CAYMAN
#
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
# Variables and Classes
#

class geese:
    def __init__(self):
        with open('HASviolet-duck.json') as jsfile:
            self.config = json.load(jsfile)
            try:
                self.simple_message = str(self.config["SIMPLE"]["message"])
                self.simple_interval = str(self.config["SIMPLE"]["interval"])
                self.simple_action = str(self.config["SIMPLE"]["action"])
                self.simple_trigger = str(self.config["SIMPLE"]["trigger"])
                self.harder_message = str(self.config["HARDER"]["message"])
                self.harder_interval = str(self.config["HARDER"]["interval"])
                self.harder_trigger = str(self.config["HARDER"]["trigger"])
                self.harder_action = str(self.config["HARDER"]["action"])
                self.hardcore_message = str(self.config["HARDCORE"]["message"])
                self.hardcore_interval = str(self.config["HARDCORE"]["interval"])
                self.hardcore_trigger = str(self.config["HARDCORE"]["trigger"])
                self.hardcore_action = str(self.config["HARDCORE"]["action"])
            except KeyError as e:
                raise LookupError("Error HASviolet-duck.json: {} missing.".format(str(e)))
    def update(self):
        self.config["SIMPLE"]["message"] = self.simple_message
        self.config["SIMPLE"]["interval"] = self.simple_interval
        self.config["SIMPLE"]["action"] = self.simple_action
        self.config["SIMPLE"]["trigger"] = self.simple_trigger
        self.config["HARDER"]["message"] = self.harder_message
        self.config["HARDER"]["interval"] = self.harder_interval
        self.config["HARDER"]["action"] = self.harder_action
        self.config["HARDER"]["trigger"] = self.harder_trigger
        self.config["HARDCORE"]["message"] = self.hardcore_message
        self.config["HARDCORE"]["interval"] = self.hardcore_interval
        self.config["HARDCORE"]["action"] = self.hardcore_action
        self.config["HARDCORE"]["trigger"] = self.hardcore_trigger

duck = geese()

def main_menu():
    os.system("clear")
    print ()
    print ('------- duckhunt Config Tool -------')
    print ()
    print ('- - - SIMPLE MODE - - - - - - - - - -')
    print ('      1       Message ',duck.simple_message)
    print ('      2      Interval ',duck.simple_interval)
    print ('      3       Trigger ',duck.simple_trigger)
    print ('      4       Action ',duck.simple_action)
    print ()
    print ('- - - HARDER MODE - - - - - - - - - -')
    print ('     11       Message ',duck.harder_message)
    print ('     12      Interval ',duck.harder_interval)
    print ('     13       Trigger ',duck.harder_trigger)
    print ('     14       Action ',duck.harder_action)
    print ()
    #print ('- - - HARDCORE MODE - - - - - - - - -')
    #print ('     21       Message ',duck.hardcore_message)
    #print ('     22      Interval ',duck.hardcore_interval)
    #print ('     23       Trigger ',duck.hardcore_trigger)
    #print ('     24       Action ',duck.hardcore_action)
    #print ()
    print ('- - - - - - - - - - - - - - - -')
    print()
    print ('      7  About the MODES')
    print ('      8  About the Tool')
    print ('      9   Write changes ')
    print ('      0    Exit Menu ')
    print ()
    fun = input('Select option: ')  
    if fun=="1":
        duck.simple_message = do_set_message()
    elif fun=="2":
        duck.simple_interval = do_set_interval()
    elif fun=="3":
        duck.simple_trigger = do_set_trigger()
    elif fun=="4":
        duck.simple_action = do_set_action()
    elif fun=="11":
        duck.harder_message = do_set_message()
    elif fun=="12":
        duck.harder_interval = do_set_interval()
    elif fun=="13":
        duck.harder_trigger = do_set_trigger()
    elif fun=="14":
        duck.harder_action = do_set_action()
    #elif fun=="21":
    #    duck.hardcore_message = do_set_message()
    #elif fun=="22":
    #    duck.hardcore_interval = do_set_interval()
    #elif fun=="23":
    #    duck.hardcore_trigger = do_set_trigger()
    #elif fun=="24":
        duck.hardcore_action = do_set_action()
    elif fun=="7":
        do_about_modes()
    elif fun=="8":
        do_about()
    elif fun=="9":
        write_changes(duck)
    elif fun=="0":
        exit(0)
    else:
        print ("Programmer error: unrecognized option")
    pass

def do_print_json():
    duck.update()
    print (duck.config)
    print ('--')
    print(duck.config["SIMPLE"]["message"])
    print(duck.config["SIMPLE"]["interval"])
    print(duck.config["SIMPLE"]["action"])
    print(duck.config["SIMPLE"]["trigger"])
    print(duck.config["HARDER"]["message"])
    print(duck.config["HARDER"]["interval"])
    print(duck.config["HARDER"]["action"])
    print(duck.config["HARDER"]["trigger"])
    print(duck.config["HARDCORE"]["message"])
    print(duck.config["HARDCORE"]["interval"])
    print(duck.config["HARDCORE"]["action"])
    print(duck.config["HARDCORE"]["trigger"])

    programPause = input("Press the <ENTER> key to continue...")
    return 

def do_about_modes():
    os.system("clear")
    print ()
    print ('SIMPLE MODE')
    print ('- Traditional Radio Direction Finding')
    print ('- Set the message and at what intervals (seconds)duck should transmit')
    print ()
    print ('HARDER MODE')
    print ('- Given a trigger, a duck can take an Action')
    print ('- Triggers include time, sensors. duck changes message/interval')
    print ()
    print ('HARDCORE MODE  (Under Development)')
    print ('- Fudds (hunters) need to TX a signal for a duck to quack')
    print ('- duck has multiple triggers and actions .. buhhhWAHAHAHAH')
    print ()
    programPause = input("Press the <ENTER> key to continue...")
    return   

def do_about():
    print ()
    print ('-- About HASviolet-duckconfig.py')
    print ('--')
    print ('-- Quick and dirty application to update your HASviolet-duck.ini file')
    print ()
    programPause = input("Press the <ENTER> key to continue...")
    return

def write_changes(self):
    print ('Writing to HASviolet-duck.json')
    with open('HASviolet-duck.json', 'w+', encoding='utf-8') as configfile:
        json.dump(duck.config, configfile, ensure_ascii=False, indent=4)
    time.sleep(3)

def write_changes_ini(self):
    self.config.set("SIMPLE", "message", duck.simple_message)
    self.config.set("SIMPLE", "interval", duck.simple_interval)
    self.config.set("SIMPLE", "action", duck.simple_action)
    self.config.set("SIMPLE", "trigger", duck.simple_trigger)
    self.config.set("HARDER", "message", duck.harder_message)
    self.config.set("HARDER", "interval", duck.harder_interval)
    self.config.set("HARDER", "trigger", duck.harder_trigger)
    self.config.set("HARDER", "action", duck.harder_action)
    self.config.set("HARDCORE", "message", duck.hardcore_message)
    self.config.set("HARDCORE", "interval", duck.hardcore_interval)
    self.config.set("HARDCORE", "trigger", duck.hardcore_trigger)
    self.config.set("HARDCORE", "action", duck.hardcore_action)
    print ('Writing to HASviolet-duck.ini')
    with open('HASviolet-duck.ini', 'w+') as configfile:
        self.config.write(configfile)
    time.sleep(3)

def do_set_interval():
    print ()
    print ('--')
    fun = input('Enter seconds between messages: ')  
    return(fun)

def do_set_message():
    print ()
    print ('--')
    fun = input('-- Enter message: ')  
    return(fun)

def do_set_trigger():
    print ()
    print ('-- Trigger Type: ')  
    print ('-- ')  
    funnier = input('-- (T)ime, (E)lapsed time, or (S)ensor: ')
    funnier = funnier.upper()
    if funnier=="T":
        funtime = input('-- Enter UTC Time 00:00:00 ')
        funtime = funtime.upper()
        funnier = funnier + "," + funtime
    elif funnier=="E":
        funtime = input('-- Enter minutes')
        funnier = funnier + "," + funtime
    elif funnier=="S":
        funtime = input('-- Enter Sensor')
        funtime = funtime.upper()
        funnier = funnier + "," + funtime
    else:
        return("none")
    print ()
    funniest = input ('-- Trigger Reset (Y/N): ')
    funniest = funniest.upper()
    if funniest=="Y":
        funnier = funnier + ", 1"
    else:
        funnier = funnier + ", 0"
    return(funnier)

def do_set_action():
    print ()
    print ('-- Action Type: ')  
    print ('-- ')
    funnier = input('-- (E)vade, (C)onfuse, or C(o)nspire: ')
    funnier = funnier.upper()
    if funnier=="E":
        funtime = input('-- (M)utara or (H)oudini')
        funtime = funtime.upper()
        funnier = funnier + "," + funtime
    elif funnier=="C":
        funtime = input('-- (P)icard or (R)ick-roll')
        funtime = funtime.upper()
        funnier = funnier + "," + funtime
    elif funnier=="O":
        funtime = input('-- (V)asily or (K)han')
        funtime = funtime.upper()
        funnier = funnier + "," + funtime
    else:
        return("none")
    return(funnier)
    
    
#
# SETUP
#


#
# MAIN
#
while True:
    main_menu()  

