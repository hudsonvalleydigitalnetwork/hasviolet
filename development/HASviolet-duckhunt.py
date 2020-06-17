#!/usr/bin/python3
#
# HASviolet-duckhunt-config
#
#
# Usage: HASviolet-duckhunt.py
#
#  OPTIONS
#      -h, --help      show this help message and exit
#
#
#  RELEASE: BERMUDA
#
#


#
# Import Libraries
#

import argparse 
import configparser
import curses
import os
import sys
import time


#
# Variables and Classes
#

class ducks:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.sections()
        self.config.read('HASviolet-duckhunt.ini')
        try:
            self.simple_message = str(self.config["SIMPLE"]["message"])
            self.simple_interval = str(self.config["SIMPLE"]["interval"])
            self.simple_action = str(self.config["SIMPLE"]["Action"])
            self.simple_trigger = str(self.config["SIMPLE"]["trigger"])
            self.harder_message = str(self.config["HARDER"]["message"])
            self.harder_interval = str(self.config["HARDER"]["interval"])
            self.harder_trigger = str(self.config["HARDER"]["trigger"])
            self.harder_action = str(self.config["HARDER"]["Action"])
            self.hardcore_message = str(self.config["HARDCORE"]["message"])
            self.hardcore_interval = str(self.config["HARDCORE"]["interval"])
            self.hardcore_trigger = str(self.config["HARDCORE"]["trigger"])
            self.hardcore_action = str(self.config["HARDCORE"]["Action"])
        except KeyError as e:
            raise LookupError("Error HASviolet-duckhunt.ini: {} missing.".format(str(e)))
        
Duck = ducks()

#
# FUNCTIONS
#

def pause():
    programPause = input("Press the <ENTER> key to continue...")

def main_menu():
    os.system("clear")
    print ()
    print ('------- Duckhunt Config Tool -------')
    print ()
    print ('- - - SIMPLE MODE - - - - - - - - - -')
    print ('      1       Message ',Duck.simple_message)
    print ('      2      Interval ',Duck.simple_interval)
    #print ('      3       Trigger ',Duck.simple_trigger)
    #print ('      4       Action ',Duck.simple_action)
    print ()
    print ('- - - HARDER MODE - - - - - - - - - -')
    print ('     11       Message ',Duck.harder_message)
    print ('     12      Interval ',Duck.harder_interval)
    #print ('     13       Trigger ',Duck.harder_trigger)
    #print ('     14       Action ',Duck.harder_action)
    print ()
    #print ('- - - HARDCORE MODE - - - - - - - - -')
    #print ('     21       Message ',Duck.hardcore_message)
    #print ('     22      Interval ',Duck.hardcore_interval)
    #print ('     23       Trigger ',Duck.hardcore_trigger)
    #print ('     24       Action ',Duck.hardcore_action)
    #print ()
    print ('- - - - - - - - - - - - - - - -')
    print ('      7  About the MODES')
    print ('      8  About the Tool')
    print ('      9   Write changes ')
    print ('      0    Exit Menu ')
    print ()
    fun = input('Select option: ')  
    if fun=="1":
        Duck.simple_message = do_set_message()
    elif fun=="2":
        Duck.simple_interval = do_set_interval()
    elif fun=="3":
        Duck.simple_trigger = do_set_trigger()
    elif fun=="4":
        Duck.simple_action = do_set_action()
    elif fun=="11":
        Duck.harder_message = do_set_message()
    elif fun=="12":
        Duck.harder_interval = do_set_interval()
    elif fun=="13":
        Duck.harder_trigger = do_set_trigger()
    elif fun=="14":
        Duck.harder_action = do_set_action()
    elif fun=="21":
        Duck.hardcore_message = do_set_message()
    elif fun=="22":
        Duck.hardcore_interval = do_set_interval()
    elif fun=="23":
        Duck.hardcore_trigger = do_set_trigger()
    elif fun=="24":
        Duck.hardcore_action = do_set_action()
    elif fun=="7":
        do_about_modes()
    elif fun=="8":
        do_about()
    elif fun=="9":
        write_changes(Duck)
    elif fun=="0":
        exit(0)
    else:
        print ("Programmer error: unrecognized option")
    pass

def do_about_modes():
    os.system("clear")
    print ()
    print ('SIMPLE MODE')
    print ('- Traditional Radio Direction Finding')
    print ('- Set the message and at what intervals (seconds)Duck should transmit')
    print ()
    print ('HARDER MODE')
    print ('- Given a trigger, a Duck can take an Action')
    print ('- Triggers include time, sensors. Duck changes message/interval')
    print ()
    programPause = input("Press the <ENTER> key to continue...")
    return   

def do_about():
    print ()
    print ('-- About HASviolet-duckhunt-config.py')
    print ('--')
    print ('-- Quick and dirty application to update your HASviolet-duckhunt.ini file')
    print ()
    programPause = input("Press the <ENTER> key to continue...")
    return

def write_changes(self):
    self.config.set("SIMPLE", "message", Duck.simple_message)
    self.config.set("SIMPLE", "interval", Duck.simple_interval)
    self.config.set("SIMPLE", "action", Duck.simple_action)
    self.config.set("SIMPLE", "trigger", Duck.simple_trigger)
    self.config.set("HARDER", "message", Duck.harder_message)
    self.config.set("HARDER", "interval", Duck.harder_interval)
    self.config.set("HARDER", "trigger", Duck.harder_trigger)
    self.config.set("HARDER", "action", Duck.harder_action)
    self.config.set("HARDCORE", "message", Duck.hardcore_message)
    self.config.set("HARDCORE", "interval", Duck.hardcore_interval)
    self.config.set("HARDCORE", "trigger", Duck.hardcore_trigger)
    self.config.set("HARDCORE", "action", Duck.hardcore_action)
    print ('Writing to HASviolet-duckhunt.ini')
    with open('HASviolet-duckhunt.ini', 'w+') as configfile:
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

