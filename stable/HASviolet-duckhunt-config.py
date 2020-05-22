#!/usr/bin/python3
#
# HASviolet-duckhunt-config
#
#
# Usage: HASviolet-duckhunt-config.py
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
# IMPORT SETTINGS
#

config = configparser.ConfigParser()
config.sections()
config.read('HASviolet-duckhunt.ini')
try:
   duck_simple_message = str(config["SIMPLE"]["message"])
   duck_simple_interval = int(config["SIMPLE"]["interval"])
   duck_harder_message = str(config["HARDER"]["message"])
   duck_harder_interval = int(config["HARDER"]["interval"])
   duck_harder_message2 = str(config["HARDER"]["message2"])
   duck_harder_interval2 = int(config["HARDER"]["interval2"])
except KeyError as e:
   raise LookupError("Error HASviolet-duckhunt.ini : {} missing.".format(str(e)))
   exit (1)


#
# IMPORT ARGS
#


#
# FUNCTIONS
#

def do_set_interval():
    print (' ')
    print ('--')
    fun = input('Enter seconds between transmissions: ')  
    return(fun)

def do_set_message():
    print (' ')
    print ('--')
    fun = input('-- Enter new message: ')  
    return(fun)

def do_about():
    print (' ')
    print ('-- About HASviolet-duckhunt-config.py')
    print ('--')
    print ('-- Quick and dirty application to update your HASviolet-duckhunt.ini file')
    print (' ')
    time.sleep (3)

def pause():
    programPause = input("Press the <ENTER> key to continue...")

def HASmenu():
    os.system("clear")
    print (' ')
    print ('----- HASviolet Duckhunt INI Config Tool -----     ')
    print (' ')
    print (' ')
    print ('  SIMPLE GAME')
    print ('  ---------------')
    print ('      1       Message ',duck_simple_message)
    print ('      2   TX Interval ',duck_simple_interval)
    print (' ')
    print (' ')
    print ('  HARDER GAME')
    print ('  ---------------')
    print ('      3       Message ',duck_harder_message)
    print ('      4   TX Interval ',duck_harder_interval)
    print ('      5      Message2 ',duck_harder_message2)
    print ('      6  TX Interval2 ',duck_harder_interval2)
    print (' ')
    print (' ')
    print ('  HARDCORE GAME')
    print ('  ---------------')
    print ('      Coming soon')
    print (' ')
    print (' ')
    print ('  - - - - - - - -- - - - - - - -')
    print ('      8  About Duckhunt ')
    print ('      9   Write changes ')
    print ('      0    Exit program ')
    print (' ')


#
# SETUP
#

# Backup INI file
#
with open('HASviolet-duckhunt.ini.bk1', 'w+') as configfile:
    config.write(configfile)


#
# MAIN
#
while True:
    HASmenu()  
    fun = input('(1-12) Select which value you want to change: ')  
    if fun=="1":
        duck_simple_message = do_set_message()
    elif fun=="2":
        duck_simple_interval = do_set_interval()
    elif fun=="3":
        duck_harder_message = do_set_message()
    elif fun=="4":
        duck_harder_interval = do_set_interval()
    elif fun=="5":
        duck_harder_message2 = do_set_message()
    elif fun=="6":
        duck_harder_interval2 = do_set_interval()
    elif fun=="8":
        do_about()
    elif fun=="9":
        config.set("SIMPLE", "message", duck_simple_message)
        config.set("SIMPLE", "interval", duck_simple_interval)
        config.set("HARDER", "message", duck_harder_message)
        config.set("HARDER", "interval", duck_harder_interval)
        config.set("HARDER", "message2", duck_harder_message2)
        config.set("HARDER", "interval2", duck_harder_interval2)
        print ('Writing to HASviolet-duckhunt.ini')
        with open('HASviolet-duckhunt.ini', 'w+') as configfile:
            config.write(configfile)
        time.sleep(3)
    elif fun=="0":
        exit(0)
    else:
        print ("Programmer error: unrecognized option")
    pass
