#!/usr/bin/python3
#
# HASviolet-config
#
# 20200807-1355
#
# Usage: HASviolet-config.py
#
#  OPTIONS
#      -h, --help      show this help message and exit
#
#


#
# Import Libraries
#

import argparse 
import configparser
import os
import sys
import time


#
# IMPORT SETTINGS
#

iniconfig = configparser.ConfigParser()
iniconfig.sections()
iniconfig.read('HASviolet.ini')
try:
    radio = str(iniconfig["CURRENT"]["radio"])
    node_address = int(iniconfig["CURRENT"]["node_address"])
    freqmhz = float(iniconfig["CURRENT"]["freqmhz"])
    txpwr = int(iniconfig["CURRENT"]["txpwr"])
    modemcfg = str(iniconfig["CURRENT"]["modemcfg"])
    mycall = str(iniconfig["CURRENT"]["mycall"])
    myssid = int(iniconfig["CURRENT"]["myssid"])
    mybeacon = str(iniconfig["CURRENT"]["mybeacon"])
except KeyError as e:
    raise LookupError("Error HASviolet-cayman.ini[DEFAULT] : {} missing.".format(str(e)))
if radio=="RFM95":
    try:
        radio_cs = int(iniconfig["RFM95"]["rfm_cs"])
        radio_irq = int(iniconfig["RFM95"]["rfm_irq"])
        radio_nodeaddress = int(iniconfig["RFM95"]["node_address"])
        radio_modemcfg = str(iniconfig["RFM95"]["modemcfg"])
        radio_bandwidth = float(iniconfig["RFM95"]["bandwidth"])
        radio_spreadfactor = int(iniconfig["RFM95"]["spreadfactor"])
        radio_codingrate = int(iniconfig["RFM95"]["codingrate"])
        radio_crc = int(iniconfig["RFM95"]["rfm_crc"])
    except KeyError as e:
        raise LookupError("Error HASviolet.ini[DEFAULT] : {} missing.".format(str(e)))
if radio=="SX1262":
    try:
        radio_cs = int(iniconfig["SX1262"]["rfm_cs"])
        radio_irq = int(iniconfig["SX1262"]["rfm_irq"])
        radio_nodeaddress = int(iniconfig["SX1262"]["node_address"])
        radio_modemcfg = str(iniconfig["SX1262"]["modemcfg"])
        radio_bandwidth = float(iniconfig["SX1262"]["bandwidth"])
        radio_spreadfactor = int(iniconfig["SX1262"]["spreadfactor"])
        radio_codingrate = int(iniconfig["SX1262"]["codingrate"])
        radio_crc = int(iniconfig["SX1262"]["rfm_crc"])
    except KeyError as e:
        raise LookupError("Error HASviolet.ini[DEFAULT] : {} missing.".format(str(e)))

#
# FUNCTIONSs
#

def do_set_mycall():
    print (' ')
    fun = input('-- Enter callsign or handle: ')
    fun.upper()  
    return(fun)

def do_set_myssid():
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

def do_set_freqmhz():
    print (' ')
    print ('-- Change Frequency')
    print ('-- ')
    print ('-- You can choose between 863 t0 870 (EU), 902 to 928 (US) or follow ')
    print ('-- the frequencies used by the LoRa Alliance Channel Standards as listed below.')
    print ('-- ')
    print ('-- ')
    print ('--     US Frequencies                EU Frequencies')
    print ('-- ')
    print ('-- CH_00_900 | 903.08 MHz        CH_10_868 | 865.20 MHz')
    print ('-- CH_01_900 | 905.24 MHz        CH_11_868 | 865.50 MHz')
    print ('-- CH_02_900 | 907.40 MHz        CH_12_868 | 865.80 MHz')
    print ('-- CH_03_900 | 909.56 MHz        CH_13_868 | 866.10 MHz')
    print ('-- CH_04_900 | 911.72 MHz        CH_14_868 | 866.40 MHz')
    print ('-- CH_05_900 | 913.88 MHz        CH_15_868 | 866.70 MHz')
    print ('-- CH_06_900 | 916.04 MHz        CH_16_868 | 867 MHz')
    print ('-- CH_07_900 | 918.20 MHz        CH_17_868 | 868 MHz')
    print ('-- CH_08_900 | 920.36 MHz')
    print ('-- CH_09_900 | 922.52 MHz')
    print ('-- CH_10_900 | 924.68 MHz')
    print ('-- CH_11_900 | 926.84 MHz')
    print ('-- CH_12_900 | 915 MHz')
    print ('-- ')
    print ('-- ')
    fun = input('-- Enter new Frequency in MHz: ')  
    if float(fun) < 863:
        fun = 863
    elif float(fun) > 928:
        fun = 928
    return(fun)

def do_set_txpwr():
    print (' ')
    fun = input('-- Enter TX power (5 to 23): ')
    if int(fun) < 5:
        fun = 5
    elif int(fun) > 23:
        fun = 23      
    return(fun)

def do_set_radio_nodeaddress():
    print (' ')
    fun = input('-- Enter LoRa Node Address (1 to 254): ')
    if int(fun) < 1:
        fun = 1
    elif int(fun) > 254:
        fun = 1      
    return(fun)

def do_set_radio_bandwidth():
    print (' ')
    fun = input('-- Enter LoRa Bandwidth (in KHz): ')
    if int(fun) < 1:
        fun = 1
    elif int(fun) > 254:
        fun = 1      
    return(fun)

def do_set_radio_spreadfactor():
    print (' ')
    fun = input('-- Enter LoRa Spread Factor: ')     
    return(fun)

def do_set_radio_codingrate():
    print (' ')
    fun = input('-- Enter LoRa Coding Rate: ')     
    return(fun)

def do_set_radio_crc():
    print (' ')
    fun = input('-- Enter LoRa CRC: ')     
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
    print ('  Node')
    print ('  - - - - - - - - - - - - - - - - - - - - -')
    print ('  1        Change Callsign-Handle ',mycall)
    print ('  2                   Change SSID ',myssid)
    print ('  3                 Change Beacon ',mybeacon)
    print (' ')
    print ('  Radio')
    print ('  - - - - - - - - - - - - - - - - - - - - -')
    print (' 11                  Change Radio ',radio)
    print (' 12              Change Frequency ',freqmhz)
    print (' 13         Change Transmit Power ',txpwr)
    print (' 14                     Change CS ',radio_cs) 
    print (' 15                    Change IRQ ',radio_irq)
    print (' 16           Change Modem config ',radio_modemcfg)
    print (' ')
    print ('  LoRa')
    print ('  - - - - - - - - - - - - - - - - - - - - -')
    print (' 21    Change (LoRa) Node Address ',radio_nodeaddress )
    print (' 22              Change Bandwidth ',radio_bandwidth)
    print (' 23          Change Spread Factor ',radio_spreadfactor)
    print (' 24            Change Coding Rate ',radio_codingrate)
    print (' 25                    Change CRC ',radio_crc)
    print ('  - - - - - - - - - - - - - - - - - - - - -')
    print (' ')
    print (' 96      Show current HAScomm.ini ')
    print (' 97        About HASviolet-config ')
    print (' 98  Write changes to HAScomm.ini ')
    print ('  0                  Exit program ')
    print (' ')


#
# SETUP
#

# Backup INI file
#
with open('HASviolet.ini.bk1', 'w+') as configfile:
    iniconfig.write(configfile)


#
# MAIN
#
while True:
    HASmenu()  
    fun = input('Select menu item: ')  
    if fun=="1":
        mycall = do_set_mycall()
    elif fun=="2":
        myssid = do_set_myssid()
    elif fun=="3":
        mybeacon = do_set_mybeacon()
    elif fun=="11":
        radio = do_set_radio()
    elif fun=="12":
        freqmhz = do_set_freqmhz()
    elif fun=="13":
        txpwr = do_set_txpwr()
    elif fun=="14":
        radio_cs = do_set_radio_cs()
    elif fun=="15":
        radio_irq = do_set_radio_irq()
    elif fun=="16":
        radio_modemcfg = do_set_radio_modemcfg()
    elif fun=="21":
        radio_nodeaddress = do_set_radio_nodeaddress()
    elif fun=="22":
        radio_bandwidth = do_set_radio_bandwidth()
    elif fun=="23":
        radio_spreadfactor = do_set_radio_spreadfactor()
    elif fun=="24":
        radio_codingrate = do_set_radio_codingrate()
    elif fun=="25":
        radio_crc = do_set_radio_crc()
    elif fun=="96":
        print (' ')
        print ('Displaying HASviolet.ini')
        print ('========================')
        print (' ')
        f = open("HASviolet.ini", "r")
        vilete = f.read()
        print (vilete)
        f.close()
        pause()
    elif fun=="97":
        do_about()
    elif fun=="98":
        mycall = str(mycall)
        myssid = str(myssid)
        freqmhz = str(freqmhz)
        txpwr = str(txpwr)
        mybeacon = str(mybeacon)
        radio_cs = str(radio_cs)
        radio_irq = str(radio_irq)
        radio_nodeaddress = str(radio_nodeaddress)
        radio_modemcfg = str(radio_modemcfg)
        radio_bandwidth = str(radio_bandwidth)
        radio_spreadfactor = str(radio_spreadfactor)
        radio_codingrate = str(radio_codingrate)
        radio_crc = str(radio_crc)
        iniconfig.set("CURRENT", "mycall", mycall)
        iniconfig.set("CURRENT", "myssid", myssid)
        iniconfig.set("CURRENT", "freqmhz", freqmhz)
        iniconfig.set("CURRENT", "txpwr", txpwr)
        iniconfig.set("CURRENT", "mybeacon", mybeacon)
        if radio=="RFM95":
            iniconfig.set("RFM95", "rfm_cs", radio_cs)
            iniconfig.set("RFM95", "rfm_irq", radio_irq)
            iniconfig.set("RFM95", "node_address", radio_nodeaddress)
            iniconfig.set("RFM95", "modemcfg", radio_modemcfg)
            iniconfig.set("RFM95", "bandwidth", radio_bandwidth)
            iniconfig.set("RFM95", "spreadfactor", radio_spreadfactor)
            iniconfig.set("RFM95", "codingrate", radio_codingrate)
            iniconfig.set("RFM95", "rfm_crc", radio_crc)
        if radio=="SX1262":
            iniconfig.set("SX1262", "rfm_cs", radio_cs)
            iniconfig.set("SX1262", "rfm_irq", radio_irq)
            iniconfig.set("SX1262", "node_address", radio_nodeaddress)
            iniconfig.set("SX1262", "modemcfg", radio_modemcfg)
            iniconfig.set("SX1262", "bandwidth", radio_bandwidth)
            iniconfig.set("SX1262", "spreadfactor", radio_spreadfactor)
            iniconfig.set("SX1262", "codingrate", radio_codingrate)
            iniconfig.set("SX1262", "rfm_crc", radio_crc)
        print ('Writing to HASviolet.ini')
        with open('HASviolet.ini', 'w+') as configfile:
            iniconfig.write(configfile)
        time.sleep(3)
    elif fun=="0":
        exit(0)
    else:
        print ("Programmer error: unrecognized option")
    pass