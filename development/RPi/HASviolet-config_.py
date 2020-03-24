#!/usr/bin/python3
#
# HASviolet-config
#
#
# Usage: HASviolet-config.py
#
#  OPTIONS
#      -h, --help      show this help message and exit
#
#
#  TO-DO:
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
config.read('HASviolet.ini')

try:
   gpio_rfm_cs = int(config["USER"]["gpio_rfm_cs"])
   gpio_rfm_irq = int(config["USER"]["gpio_rfm_irq"])
   node_address = int(config["USER"]["node_address"])
   freqmhz = float(config["USER"]["freqmhz"])
   txpwr = int(config["USER"]["txpwr"])
   modemcfg = str(config["USER"]["modemcfg"])
   mycall = str(config["USER"]["mycall"])
   ssid = int(config["USER"]["ssid"])
   beacon = str(config["USER"]["beacon"])
except KeyError as e:
   raise LookupError("Error HASviolet.ini[USER] : {} missing.".format(str(e)))
   exit (1)


#
# IMPORT ARGS
#

#parser = argparse.ArgumentParser(description='HASviolet-config')
#parser.add_argument('-r','--restore backup', help='Restore most recent config', action='store_true')
#args = vars(parser.parse_args())
#arg_hvdn_rawdata = args['raw_datFUNhis device will be set to (1-254)
# freqmhz - The freq of this device in MHz (911.250 MHz is recommended)
# txpwr - Transmit power. Can be set from 5 to 23
# modemcfg - What LoRa mode you want to use
# mycall - Your Amateur Radio callsign or handle ifyou have no license
# ssid - Number between 50 - 99 when appended to your callsign/handle uniqiely identifies this device
#        (example: N1JTA-50 , PURPLE-60)
# beacon - What text to send when device operating as a beacon. Must contain in quotes"
#


#
# FUNCTIONS
#

def do_set_call():
    print (' ')
    print ('-- Change Callsign or Handle')
    print ('--')
    fun = input('-- Enter callsign or handle: ')
    fun.upper()  
    return(fun)

def do_set_ssid():
    print (' ')
    print ('-- Change SSID')
    print ('--')
    fun = input('Enter SSID: 50-99: ')  
    return(fun)
    
def do_set_freqchannel():
    print (' ')
    print ('-- Change Frequency')
    print ('-- ')
    print ('-- You can chodse between 863 t0 870 (EU), 902 to 928 (US)')
    fun = input('-- Enter new Frequency in MHz: ')  
    if int(fun) < 863:
        fun = 863
    elif int(fun) > 928:
        fun = 928
    print ('-- Change TX power')
    print ('--')
    fun = input('-- Enter TX power - 5 to 23: ')
    if int(fun) < 5:
        fun = 5
    elif int(fun) > 23:
        fun = 23
    pass
    return(fun)

def do_set_beacon():
    print (' ')
    print ('-- Change Beacon')
    print ('--')
    fun = input('-- Enter new beacon message: ')  
    return(fun)

def do_about():
    print (' ')
    print ('-- About HASconfig.py')
    print ('--')
    print ('-- Quick and dirty application to update your INI file')
    print (' ')
    time.sleep (3)

def pause():
    programPause = input("Press the <ENTER> key to continue...")

def HASmenu():
    os.system("clear")
    print (' ')
    print ('----- HASviolet INI Config Tool (HASviolet-config) -----     ')
    print (' ')
    print ('  1    Change Callsign-Handle ',mycall)
    print ('  2               Change SSID ',ssid)
    print ('  3          Change Frequency ',freqmhz)
    print ('  4     Change Transmit Power ',txpwr)
    print ('  5             Change Beacon ',beacon)
    print ('  6              Change Modem ',modemcfg)
    print ('  7  Show current HAScomm.ini')
    print ('  - - - - - - - - - - - - - - - - - - - - -')
    print ('  8    About HASviolet-config')
    print ('  9      Write changes to HAScomm.ini')
    print ('  0              Exit program')
    print (' ')


#
# SETUP
#

# Backup INI file
#
with open('HASviolet.ini.bk1', 'w+') as configfile:
    config.write(configfile)


#
# MAIN
#
while True:
    HASmenu()  
    fun = input('Select menu item: ')  
    if fun=="1":
        mycall = do_set_call()
    elif fun=="2":
        ssid = do_set_ssid()
    elif fun=="3":
        freqmhz = do_set_freqchannel()
    elif fun=="4":
        txpwr = do_set_txpwr()
    elif fun=="5":
        beacon = do_set_beacon()
    elif fun=="6":
        modemcfg = do_set_modem()
    elif fun=="7":
        print (' ')
        print ('Displaying HASviolet.ini')
        print ('========================')
        print (' ')
        f = open("HASviolet.ini", "r")
        vilete = f.read()
        print (vilete)
        f.close()
        pause()
    elif fun=="8":
        do_about()
    elif fun=="9":
        config.set("USER", "mycall", mycall)
        config.set("USER", "ssid", ssid)
        config.set("USER", "freqmhz", freqmhz)
        config.set("USER", "txpwr", txpwr)
        config.set("USER", "beacon", beacon)
        config.set("USER", "modemcfg", modemcfg)
        print ('Writing to HASviolet.ini')
        with open('HASviolet.ini', 'w+') as configfile:
            config.write(configfile)
        time.sleep(3)
    elif fun=="0":
        exit(0)
    else:
        print ("Programmer error: unrecognized option")
    pass
