#!/usr/bin/python3
#
# HASviolet-config
#
#
#   USAGE: HASviolet-config.py
#
#   OPTIONS
#      -h, --help      show this help message and exit
#
#   REVISION: 20220601-0200
#
#


#
# IMPORT LIBRARIES
#

import argparse 
import configparser
import os
import sys
import time
import json
from HASvioletRF import HASrf
from HASvioletHID import HAShid


#
# STATICS
#

HASviolet_RXLOCK = False                                               # True = RX is running
HASviolet_TXLOCK = False                                               # True = TX is running
HASviolet_CFGDIR = "../hasviolet-config/"                              # Config file is in JSON format
HASviolet_SRVDIR = HASviolet_CFGDIR + "server/"                        # Path to files. Change when Pi
HASviolet_ETC = HASviolet_CFGDIR + "etc/"                              # Config file is in JSON format
HASviolet_CONFIG = HASviolet_ETC + "HASviolet.json"                    # Config file is in JSON format
HASviolet_SSL_KEY = HASviolet_ETC + "HASviolet.key"                    # SSL Key
HASviolet_SSL_CRT = HASviolet_ETC + "HASviolet.crt"                    # Cert Key
HASviolet_PWF = HASviolet_ETC + "HASviolet.pwf"                        # Password file  user:hashedpasswd
HASviolet_MSGS = HASviolet_SRVDIR + "msgs/HASviolet.msgs"              # radio writes msgs received here   
HASviolet_LOGIN = HASviolet_SRVDIR + "static/HASviolet_LOGIN.html"
HASviolet_LOGINCSS = HASviolet_SRVDIR + "static/HASviolet_LOGIN.css"
HASviolet_INDEX = HASviolet_SRVDIR + "static/HASviolet_INDEX.html"
HASviolet_INDEXCSS = HASviolet_SRVDIR + "static/HASviolet.css"
HASvioletjs = HASviolet_SRVDIR + "static/HASviolet.js"
HVDN_LOGO = HASviolet_ETC + "HVDN_logo.xbm"



#
# VARIABLES
#


#
# FUNCTIONS
#

def do_set_call():
    print (' ')
    fun = input('-- Enter callsign or handle: ')
    fun.upper()  
    return(fun)

def do_set_ssid():
    print (' ')
    fun = input('-- Enter SSID (50-99): ')  
    return(fun)

def do_set_mybeacon():
    print (' ')
    fun = input('-- Enter new beacon message: ')
    return(fun)

def do_set_radio():
    print (' ')
    fun = input('-- Enter Radio (RFM95, SX126X, DUMMYRF): ')  
    return(fun)

def do_set_radio_modem():
    print (' ')
    print ('--')
    print ('	Modem Choices:')
    print ('--')
    print ('0: Bw125Cr45Sf128" "MEDIUM", spreadfactor: 7, codingrate4: 8, bandwidth: 125000')
    print ('1: Bw500Cr45Sf128" "FAST-SHRT", spreadfactor: 7, codingrate4: 5, bandwidth: 500000')
    print ('2: Bw31_25Cr48Sf512" "SLOW-LNG1", spreadfactor: 7, codingrate4: 8, bandwidth: 31250')
    print ('3: Bw125Cr48Sf4096" "SLOW-LNG2", spreadfactor: 12, codingrate4: 8, bandwidth: 125000')
    print ('4: Bw125Cr45Sf2048" "SLOW-LNG3", spreadfactor: 8, codingrate4: 5, bandwidth: 125000')
    print ('-- ')
    print ('-- ')
    fun = input('-- Enter Modem Selection (0-4)): ') 
    return(fun)

def do_set_frequency():
    print (' ')
    print ('-- Change Frequency')
    print ('-- ')
    print ('-- Know your countries laws on frequency allocation')
    print ('-- Radio supports 863.0 to 870.0 MHz and 902 to 928 MHz')
    print ('-- ')
    print ('-- ')
    print ('-- ')
    fun = int(input('-- Enter new Frequency in Hz (Yes in Hz!): '))
    if int(fun) < 863000000:
        fun = 863000000
    elif int(fun) > 928000000:
        fun = 928000000
    return(fun)

def do_set_txpwr():
    print (' ')
    fun = int(input('-- Enter TX power (5 to 20): '))
    if int(fun) < 5:
        fun = 5
    elif int(fun) > 20:
        fun = 20
    else:
        fun = 10
    return(fun)

def do_set_radio_bandwidth():
    print (' ')
    fun = int(input('-- Enter LoRa Bandwidth (in Hz): '))
    if fun < 7800:
        fun = 7800
    elif fun > 512000000:
        fun = 512000000      
    return(fun)

def do_set_radio_spreadfactor():
    print (' ')
    fun = input('-- Enter LoRa Spread Factor: ')  
    if fun < 6:
        fun = 6
    elif fun > 12:
        fun = 12        
    return(fun)

def do_set_radio_codingrate4():
    print (' ')
    fun = input('-- Enter LoRa Coding Rate: ')     
    if fun < 4:
        fun = 4
    elif fun > 8:
        fun = 8        
    return(fun)

def do_about():
    print (' ')
    print ('-- About HASconfig.py')
    print ('--')
    print ('-- Quick and dirty application to update your HASviolet config file')
    print (' ')
    time.sleep (3)

def pause():
    programPause = input("Press the <ENTER> key to continue...")

def HASmenu():
    os.system("clear")
    print (' ')
    print ('      -===- HASviolet Config Tool -===- ')
    print (' ')
    print ('  - - - - - - - - - - - - - - - - - - - - -')
    print ('  1     Change my Call / Handle ',HASit.mycall)
    print ('  2              Change my SSID ',HASit.myssid)
    print ('  3            Change my Beacon ',HASit.mybeacon)
    print ('  4   Change dest Call / Handle ',HASit.dstcall)
    print ('  5            Change dest SSID ',HASit.dstssid)
    print ('  - - - - - - - - - - - - - - - - - - - - -')
    print (' 11                Change Radio ',HASit.radio)
    print (' 12       Change Frequency (Hz) ',HASit.frequency)
    print (' 13       Change Transmit Power ',HASit.txpwr)
    print (' 14                Change Modem ',HASit.modem)
    print (' 15       Change Bandwidth (Hz) ',HASit.bandwidth)
    print (' 16        Change Spread Factor ',HASit.spreadfactor)
    print (' 17          Change Coding Rate ',HASit.codingrate4)
    print ('  - - - - - - - - - - - - - - - - - - - - -')
    print (' 40      Show current HASviolet.json ')
    print (' 41  Generate ModemRegister settings ')
    print ('  - - - - - - - - - - - - - - - - - - - - -')
    print (' 51  Write changes to hasVIOLET.json ')
    print ('  - - - - - - - - - - - - - - - - - - - - -')
    print (' 99           About HASviolet-config ')  
    print ('  0                     Exit program ')
    print (' ')


#
# SETUP
#

# Import HASviolet.json
HASit = HASrf()

# Backup JSON file
#os.popen('cp HASviolet_CONFIG HASviolet_ETC/HASviolet.json.bk1')

#
# MAIN
#

while True:
    HASmenu()  
    fun = input('Select menu item: ')  
    if fun=="1":
        HASit.mycall = do_set_call()
    elif fun=="2":
        HASit.myssid = do_set_ssid()
    elif fun=="3":
        HASit.mybeacon = do_set_mybeacon()
    elif fun=="4":
        HASit.dstcall = do_set_call()
    elif fun=="5":
        HASit.dstssid = do_set_ssid()
    elif fun=="11":
        HASit.radio = do_set_radio()
    elif fun=="12":
        HASit.frequency = do_set_frequency()
    elif fun=="13":
        HASit.txpwr = do_set_txpwr()
    elif fun=="14":
        HASit.radio_modem = do_set_radio_modem()
    elif fun=="15":
        HASit.radio_bandwidth = do_set_radio_bandwidth()
    elif fun=="16":
        HASit.radio_spreadfactor = do_set_radio_spreadfactor()
    elif fun=="17":
        HASit.radio_codingrate4 = do_set_radio_codingrate4()
    elif fun=="40":
        print (' ')
        print ('Displaying HASviolet.json')
        print ('========================')
        print (' ')
        f = open(HASviolet_CONFIG, "r")
        vilete = f.read()
        print (vilete)
        f.close()
        pause()
    elif fun=="41":
        HASit.showmodemconfig(int(HASit.bandwidth), int(HASit.codingrate4), int(HASit.spreadfactor))
        pause()
    elif fun=="51":
        print ('Opening HASviolet.json')
        with open(HASviolet_CONFIG) as configReadFile:
            data = json.load(configReadFile)
        time.sleep(3)           
        data["RADIO"]["rfmodule"] = HASit.radio
        #data["RADIO"]["channel"] = HASit.channel
        #data["RADIO"]["channelname"] = HASit.channelname
        data["RADIO"]["frequency"] = HASit.frequency
        data["RADIO"]["modem"] = HASit.modem
        data["RADIO"]["txpwr"] = HASit.txpwr
        data["RADIO"]["spreadfactor"] = HASit.spreadfactor
        data["RADIO"]["codingrate4"] = HASit.codingrate4
        data["RADIO"]["bandwidth"] = HASit.bandwidth
        data["CONTACT"]["mycall"] = HASit.mycall
        data["CONTACT"]["myssid"] = HASit.myssid
        data["CONTACT"]["mybeacon"] = HASit.mybeacon
        data["CONTACT"]["dstcall"] = HASit.dstcall
        data["CONTACT"]["dstssid"] = HASit.dstssid
        print ('Updating HASviolet.json')
        with open(HASVIOLET_CONFIG, 'w') as configWriteFile:
            json.dump(data, configWriteFile, indent=3)
        time.sleep(3)
    elif fun=="99":
        do_about()
    elif fun=="0":
        exit(0)
    else:
        print ("Programmer error: unrecognized option")
    pass