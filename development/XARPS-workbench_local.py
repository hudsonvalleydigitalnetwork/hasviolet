#!/usr/bin/python3
#
# XARPS Workbench
#
#
# Usage: XARPS-workbench.py
#
#


#
# Import Libraries
#

import time
import sys
import struct
import binascii
import pynmea2
#from HASvioletRF import HASrf
#from HASvioletHID import HAShid
import XARPS
from XARPS import XARPS


#
# Variables
#

#HASit = HASrf()
#HAShat = HAShid()
XARPS = XARPS()
xpayload = "XARPS.packet"

#
# FUNCTIONS
#

def about_workbench():
    print (' ')
    print ('-- About XARPS-Workbench.py')
    print ('--')
    print ('-- Quick and dirty application to create and send XARPS payloads')
    print (' ')
    time.sleep (3)
    return

def about_xarps():
    print()
    print("XARPS -  eXtensible  Amateur Radio Payload Specification")
    print()
    print()
    print("PAYLOAD FIELDS")
    print()
    print("|   Source   | Destination |  Options  |  Data Type  |    Data      |")
    print("| ---------- | ----------- | --------- | ----------- | ------------ |")
    print("|   9 bytes  |   9 bytes   |  1 byte   |   1 byte    |  235 bytes   |")
    print("|  (string)  |  (string)   | (integer) |  (integer)  |  (string)    |")
    print()
    print("Source and Destination")
    print()
    print(" Each contain callsign/handle with SSID. Field size supports IARU")
    print(" decision for 7 character callsigns. Right justifed tex with left side")
    print(" padding used. Examples, GB2ABC50, WA1BCDE50, PURPLE53.")
    print()
    print(" BEACON99 is a reserved word in the destination field for broadcasts")
    print(" messages. The 99 SSID can be changed to another number for multicasts")
    print()
    print("Options Field")
    print()
    print("|    Value     |        Option        |             Description          |")
    print("| ------------ | -------------------- | -------------------------------- |")
    print("|  0x00-0x05   |       Reserved       |                                  |")
    print("|     0x06     |     ACK Response     |  ACK reply                       |")
    print("|     0x07     |     ACK Request      |  Send ACK                        |")
    print()
    print("Data Type Field")
    print()
    print("|    Value     |         Type         |             Description          |")
    print("| ------------ | -------------------- | -------------------------------- |")
    print("|     0x00     |       Reserved       |  Reserved                        |")
    print("|     0x01     |        Battery       |  Battery voltage update          |")
    print("|     0x02     |         Time         |  Current time payload            |")
    print("|     0x03     |    Position Update   |  GPS position update             |")
    print("|     0x04     |     Weather Update   |  Weather station data            |")
    print("|     0x05     |     Text Message     |  Text message between stations   |")
    print("|     0x06     |      Broadcast       |  Broadcast Message to all        |")
    print("|     0x07     |  Last Seen Stations  |  Digest of recent stations       |")
    print("|     0x08     |      Binary Data     |  Binary Data Transport           |")
    print("|  0x09-0x0F   |        Reserved      |  Reserved                        |")
    print("|     0x50     |         HTTP         |  HTTP                            |")
    print("|     0x71     |        Ident         |  Ident                           |")
    print()
    print("Data")
    print()
    print(" TYPE 01 Battery Message")
    print()
    print("|    Voltage    |    Current    |   Capacity    |")
    print("|               |  Consumption  |               |")
    print("| ------------- | ------------- | ------------- |")
    print("|    8 bytes    |    8 bytes    |    1 byte     |")
    print("|    (float)    |    (float)    |   (Integer)   |")
    print()
    print()
    print(" TYPE 02 Time Message")
    print()
    print("|     EPOC      |    Systems    |      Local    |")
    print("|   Time(sec)   |  Uptime(sec)  |      Time     |")
    print("| ------------- | ------------- | ------------- |")
    print("|    8 bytes    |    8 bytes    |    28 byte    |")
    print("|    (float)    |    (float)    |    (String)   |")
    print()
    print()
    print(" TYPE 03 Position Message (NMEA2) ")
    print()
    print("| Timestamp | Latitude |  Longitude  | Altitude | Latitude  |   Local   | Number of  |   Data   |  Station  |")
    print("|   (EPOC)  |          |             |          | Direction | Direction | Satellites |    Age   |   Type    |")
    print("| --------- | -------- | ----------- | -------- | --------- | --------- | ---------- | -------- | --------- |")
    print("|  8 bytes  |  8 bytes |   8 bytes   |  8 bytes |  8 bytes  |  8 bytes  |   1 byte   |  8 bytes |  1 byte   |")
    print("|  (float)  |  (float) |   (float)   |  (float) |  (float)  |  (float)  |  (integer) |  (float) | (integer) |")
    print()
    print()
    print(" TYPE_04 Weather Update")
    print()
    print("| Timestamp | Latitude |  Longitude  | Temperature |   Humidity  |  Barometer  |    Wind    |    Wind    |")
    print("|   (EPOC)  |          |             |             |             |             | Direction  |    Speed   |")
    print("| --------- | -------- | ----------- | ----------- | ----------- | ----------- | ---------- | ---------- |")
    print("|  8 bytes  |  8 bytes |   8 bytes   |   1 byte    |   1 byte    |   8 bytes   |   1 byte   |   1 byte   |")
    print("|  (float)  |  (float) |   (float)   |  (integer)  |  (integer)  |   (float)   |  (integer) |  (integer) |")
    print()
    print()
    print("TYPE_05 TEXT Message (default)")
    print()
    print("|          Message       |")
    print("|  --------------------- |")
    print("|   235 bytes (string)   |")
    print()
    print()
    print(" TYPE_6 Broadcast Message")
    print()
    print("|          Message       |")
    print("|  --------------------- |")
    print("|   235 bytes (string)   |")
    print()
    print(" Default Destination is BEACON-99 but SSID could be used in a multicast fashion as below")
    print()
    print("|  BEACON-XX  |         Target         |")
    print("|  ---------- | ---------------------- |")
    print("|     99      |      ALL stations      |")
    print("|     88      |      ALL gateways      |")
    print("|     77      | ALL Local RAN stations |")
    print("|     66      |    All Club Members    |")
    print()
    print(" TYPE_7 Last Seen Stations")
    print()
    print(" Comma delimitted list of stations heard in the last 15 minutes")
    print()
    print("|  Station(0)  |  Timestamp  |  Station(..)  |  Timestamp(..)  |  Station(14)  |  Timestamp(14) |")
    print("| ------------ | ----------- | ------------- | --------------- | ------------- | -------------- |")
    print("|    9 bytes   |   8 bytes   |     9 bytes   |      8 bytes    |     9 bytes   |     8 bytes    |")
    print("|   (string)   |   (float)   |    (string)   |      (float)    |    (string)   |     (float)    |")
    print()
    print()
    programPause = input("Press the <ENTER> key to continue...")
    return

def menu_main():
    print()
    print("------------ XARPS Workbench -----------")
    print()
    print("  1       Craft Payloads")
    print("  2     Analyze Payloads")
    print()
    print("  8       XARPS Diagram")
    print("  9       About Workbench")
    print("  0        Exit program")
    print()
    return

def menu_package():
    while True:
        print()
        print("------------ XARPS Generator -----------")
        print()
        print("  1        source :", XARPS.source)
        print("  2   destination :", XARPS.destination)
        print("  3       options :", XARPS.options)
        print("  4         dtype :", XARPS.dtype)
        print("  5  Edit message :")
        print()
        print("          message :", XARPS.message)
        print("           (Bytes):", len(XARPS.message))
        print()
        print("  6  Pack and Save payload :")
        #print("  7    Pack and TX payload :")
        print()
        print("  0      Exit Menu:")
        print()
        fun = input('Select menu item: ')  
        if fun=="1":
            XARPS.source = set_source()
        elif fun=="2":
            XARPS.destination = set_destination()
        elif fun=="3":
            XARPS.options = set_options()
        elif fun=="4":
            XARPS.dtype = set_dtype()
        elif fun=="5":
            if XARPS.dtype == 1: # Battery
                set_dtype01()
            if XARPS.dtype == 2: # Time
                set_dtype02()
            if XARPS.dtype == 3: # Position
                set_dtype03()
            if XARPS.dtype == 4: # WX Update
                set_dtype04()
            if XARPS.dtype == 5: # Telemetry
                set_dtype05()
            if XARPS.dtype == 6: # Binary Data
                set_dtype06()
            if XARPS.dtype == 7: # Text (Default)
                set_dtype07()
            if XARPS.dtype == 8: # APRS
                set_dtype08()
            if XARPS.dtype == 9: # Last Seen Stations
                set_dtype09()
            if XARPS.dtype == 80:  # HTTP
                set_dtype50()
            if XARPS.dtype == 113: # Identd
                set_dtype71()
        elif fun=="6": # Pack and Save
            XARPS.payload = XARPS.pack()
            if len(XARPS.payload) > MAX_PAYLOAD_LENGTH:
                print ('ERROR - Payload too big')
                exit(0)
            print ('Writing to XARPS.packet')
            xarpsfile = open("XARPS.packet", "w")
            xarpsfile.write(XARPS.payload)
            xarpsfile.close
            time.sleep(3)
        #elif fun=="7": # Pack and TX
        #    XARPS.payload = XARPS.pack()
        #    HASit.tx(XARPS.payload)
        #    time.sleep(3)
        elif fun=="0":
            return
        else:
            print ("Programmer error: unrecognized menu")
    return

def menu_analyze():
    global xpayload
    while True:
        print()
        print("------------ XARPS Analyzer -----------")
        print()
        print("  1  payload source :", xpayload)
        print("  2    Run Analyzer")
        print("  0       Exit Menu")
        print()
        fun = input('Select menu item: ')  
        if fun=="1":
            funnier = input("Open a (F)ile or via (R)eceiver")
            funnier = funnier.upper()
            if funnier == "F":
                xpayload = input("Filename: ")
            elif funnier == "R":
                xpayload = "RX"
        elif fun=="2":
            if xpayload == "RX":
                analyze_rx()
            else:
                analyze_file()
        elif fun=="0":
            return  
    return

def set_source():
    print('--')
    fun1 = input('--      Enter source: ')
    fun2 = int(input('-- Enter SSID (50-99): '))
    fun1 = fun1.upper()
    fun = fun1 + str(fun2)
    fun = fun.rjust(9, ' ')
    return(fun)

def set_destination():
    print('--')
    fun1 = input('-- Enter destination: ')
    fun2 = int(input('-- Enter SSID (50-99): '))
    fun1 = fun1.upper()
    fun = fun1 + str(fun2)
    fun = fun.rjust(9, ' ')
    return(fun)

def set_options():
    print('--')
    print("-- Which options would you like to select")
    fun = int(input("   6 for ACKREPLY, 7 for ACK, 0 for none (default): "))
    if fun == 6:
        XARPS.OPT_06_ACKREPLY = True
        XARPS.OPT_07_ACK = False
    if fun == 7:
        XARPS.OPT_06_ACKREPLY = False
        XARPS.OPT_07_ACK = True
    if fun < 6 or fun > 7:
        XARPS.OPT_06_ACKREPLY = False
        XARPS.OPT_07_ACK = False
        fun = 0
    return(fun)

def set_dtype():
    print ('--')
    fun = int(input('-- Enter Data Type: '))
    return(fun)

def set_dtype01():
    print()
    print("------ XARPS TYPE 01 Battery Message ------")
    print()
    print("---------------- Payload ------------------")
    print()
    print("   1    Voltage:", XARPS.dtype01_voltage)
    print("   2    Current:", XARPS.dtype01_current)
    print("   3   Capacity:", XARPS.dtype01_capacity)
    print()
    print('- - - - - - - - - - - - - - - - - - - - - -')
    print('   0       Back to Main Menu')
    print(' ')
    funny = input('Select menu item: ')
    while True:
        if funny=="1":
            voltage = float(input('-- Enter Voltage (5.0 - 14.1): '))
            XARPS.dtype01_voltage = int(voltage*100)/100
        elif funny=="2":
            current = float(input('-- Enter Current Draw (0.001 - 1.1): '))
            XARPS.dtype01_current = int(current*100)/100
        elif funny=="3":
            capacity = float(input('-- Enter Capacity (1.0 - 100.0): '))
            XARPS.dtype01_capacity = int(capacity*10)/10
        elif funny=="0":
            XARPS.message = XARPS.dtype01_pack()
            return
        else:
            print ("Programmer error: unrecognized option")
    return

def set_dtype02():
    with open('/proc/uptime', 'r') as f:
        uptime_seconds = float(f.readline().split()[0])
    f.close
    XARPS.dtype02_time = int(time.time())  # Time since Epoc
    XARPS.dtype02_uptime = int(uptime_seconds)
    XARPS.dtype02_ctime = str(time.ctime())
    print()
    print("-------- XARPS TYPE 02 Time Message -------")
    print()
    print("------------------- Payload ---------------")
    print()
    print("     Timestamp (EPOC): ", XARPS.dtype02_time)
    print("  System Uptime (sec): ", XARPS.dtype02_uptime)
    print("           Local time: ", XARPS.dtype02_ctime)
    print()
    print()
    print('- - - - - - - - - - - - - - - - - - - - - -')
    print()
    print("  Payload sourced from this system")
    programPause = input("Press the <ENTER> key to continue...")
    print(' ')
    XARPS.message = XARPS.dtype02_pack()
    return

def set_dtype03():
    XARPS.dtype03_timestamp = int(time.time())  # Time since Epoc
    print()
    print("----- XARPS TYPE 03 Position Message -----")
    print()
    print("---------------- Payload -----------------")
    print()
    print("   1      Timestamp:", XARPS.dtype03_timestamp)
    print("   2    Object Type:", XARPS.dtype03_object)
    print("   3       Latitude:", XARPS.dtype03_lat)
    print("   4      Longitude:", XARPS.dtype03_lon)
    print()
    print("   5       Altitude:", XARPS.dtype03_altitude)
    print("   6      Alt Units:", XARPS.dtype03_altunits)
    print()
    print('- - - - - - - - - - - - - - - - - - - - -')
    print('   0       Back to Main Menu')
    print(' ')
    while True:
        funny = input('Select menu item: ')
        if funny=="2":
            shinyobj = int(input('-- Object Type (0 - 15): '))
            XARPS.dtype03_object = shinyobj
        elif funny=="3":
            laddy = float(input('-- Enter Latitude in decimal: '))
            XARPS.dtype03_lat = laddy
        elif funny=="4":
            longy = float(input('-- Enter Longitude in decimal: '))
            XARPS.dtype03_lon = longy
        elif funny=="5":
            alddy = float(input('-- Enter Altitude in decimal: '))
            XARPS.dtype03_altitude = float(int(alddy*100)/100)
        elif funny=="6":
            aldduns = input('-- Enter Altitude Units in (F)oot, (M)eters, mi(L)es, or (K)ilometers:')
            aldduns = aldduns.upper()
            if aldduns=="F":
                XARPS.dtype03_altunits = ord(b'F')
            elif aldduns=="M":
                XARPS.dtype03_altunits = ord(b'M')
            elif aldduns=="L":
                XARPS.dtype03_altunits = ord(b'L')
            elif aldduns=="K":
                XARPS.dtype03_altunits = ord(b'K')
            else:
                XARPS.dtype03_altunits = ord(b'F')
        elif funny=="0":
            XARPS.message = XARPS.dtype03_pack()
            return
        else:
            print ("Programmer error: unrecognized option")
    return

def set_dtype04():
    XARPS.dtype04_timestamp = int(time.time())  # Time since Epoc
    print()
    print("-------- XARPS TYPE 04 WX Message --------")
    print()
    print("------------------- Payload --------------")
    print()
    print("   1         Timestamp:", XARPS.dtype04_timestamp)
    print("   2          Latitude:", XARPS.dtype04_lat)
    print("   3         Longitude:", XARPS.dtype04_lon)
    print("   4       Temperature:", XARPS.dtype04_temperature)
    print("   5       Temp Units:", XARPS.dtype04_tempunits)
    print("   6          Humidity:", XARPS.dtype04_humidity)
    print("   7         Barometer:", XARPS.dtype04_barometer)
    print("   8    Wind Direction:", XARPS.dtype04_winddir)
    print("   9        Wind Speed:", XARPS.dtype04_windspeed)
    print("  10  Wind Speed Units:", XARPS.dtype04_windspun)
    print()
    print('- - - - - - - - - - - - - - - - - - - - -')
    print('   0       Back to Main Menu')
    print()
    while True:
        funny = input('Select menu item: ')
        if funny=="2":
            laddy = float(input('-- Enter Latitude in decimal: '))
            XARPS.dtype04_lat = laddy
        elif funny=="3":
            longy = float(input('-- Enter Longitude in decimal: '))
            XARPS.dtype04_long = longy
        elif funny=="4":
            alddy = float(input('-- Enter Temperature in decimal: '))
            XARPS.dtype04_temperature = float(int(alddy*10)/10)
        elif funny=="5":
            aldduns = (input('-- Enter Temperature Units (F)ahrenheit or (C)elsius:'))
            aldduns = aldduns.upper()
            if aldduns=="F":
                XARPS.dtype04_tempunits = ord(b'F')
            elif aldduns=="C":
                XARPS.dtype04_tempunits = ord(b'C')
            else:
                XARPS.dtype04_tempunits = ord(b'F')
        elif funny=="6":
            hummer = float(input('-- Enter Humidity in decimal: '))
            XARPS.dtype04_humidity = float(int(hummer*10)/10)
        elif funny=="7":
            barry = float(input('-- Enter Barometric Pressure in decimal: '))
            XARPS.dtype04_barometer = float(int(barry*100)/100)
        elif funny=="8":
            windder = float(input('-- Enter Wind Direction (degrees): '))
            XARPS.dtype04_winddir = float(int(windder*100)/100)
        elif funny=="9":
            windy = float(input('-- Enter Wind Speed in decimal: '))
            XARPS.dtype04_windspeed = float(int(windy*100)/100)
        elif funny=="10":
            aldduns = (input('-- Enter Wind Speed Units (M)PH (K)PH:'))
            aldduns = aldduns.upper()
            if aldduns=="M":
                XARPS.dtype04_windspun = ord(b'M')
            elif aldduns=="K":
                XARPS.dtype04_windspun = ord(b'K')
        elif funny=="0":
            XARPS.message = XARPS.dtype04_pack()
            return
        else:
            print ("Programmer error: unrecognized option")
    return

def set_dtype05():
    print ()
    print("-------- XARPS TYPE 05 Telemetry -----")
    print()
    print("-------------- Payload ---------------")
    print()
    XARPS.message = input("-- Enter test data message: ")
    print (' ')
    XARPS.message = XARPS.dtype05_pack()
    return

def set_dtype06():
    print()
    print("--- XARPS TYPE 06 Binary Data Transfer ---")
    print()
    print("-------------- TO BE ADDED ---------------")
    print()
    print(' ')
    #XARPS.message = XARPS.dtype06_pack()
    programPause = input("Press the <ENTER> key to continue...")
    return

def set_dtype07():
    print()
    print("----- XARPS TYPE 07 Text Message -----")
    print()
    print("-------------- Payload ---------------")
    print()
    XARPS.message = input("-- Enter your message: ")
    print (' ')
    XARPS.message = XARPS.dtype07_pack()
    return

def set_dtype08():
    print()
    print("----- XARPS TYPE 08  APRS Encapsulation -----")
    print()
    print("---------------- TO BE ADDED ----------------")
    print()
    print(' ')
    #XARPS.message = XARPS.dtype08_pack()
    programPause = input("Press the <ENTER> key to continue...")
    return

def set_dtype09():
    XARPS.dtype09_heard = [' NOCALL00',' NOCALL01',' NOCALL02',' NOCALL03',' NOCALL04',' NOCALL05',' NOCALL06'\
        ,' NOCALL07',' NOCALL08',' NOCALL09',' NOCALL10',' NOCALL11',' NOCALL12',' NOCALL13',' NOCALL14']
    XARPS.dtype09_heardtime = [900, 900, 900, 900, 900, 900, 900, 900, 900, 900, 900, 900, 900, 900, 900, 900]
    print()
    print("--- XARPS TYPE 09 Last Seen Stations ---")
    print()
    print("-------------- Payload -----------------")
    print()
    print("        Heard   Time")
    print(" ---  --------- ----")
    print("  0  ", XARPS.dtype09_heard[0], XARPS.dtype09_heardtime[0])
    print("  1  ", XARPS.dtype09_heard[1], XARPS.dtype09_heardtime[1])
    print("  2  ", XARPS.dtype09_heard[2], XARPS.dtype09_heardtime[2])
    print("  3  ", XARPS.dtype09_heard[3], XARPS.dtype09_heardtime[3])
    print("  4  ", XARPS.dtype09_heard[4], XARPS.dtype09_heardtime[4])
    print("  5  ", XARPS.dtype09_heard[5], XARPS.dtype09_heardtime[5])
    print("  6  ", XARPS.dtype09_heard[6], XARPS.dtype09_heardtime[6])
    print("  7  ", XARPS.dtype09_heard[7], XARPS.dtype09_heardtime[7])
    print("  8  ", XARPS.dtype09_heard[8], XARPS.dtype09_heardtime[8])
    print("  9  ", XARPS.dtype09_heard[9], XARPS.dtype09_heardtime[9])
    print(" 10  ", XARPS.dtype09_heard[10], XARPS.dtype09_heardtime[10])
    print(" 11  ", XARPS.dtype09_heard[11], XARPS.dtype09_heardtime[11])
    print(" 12  ", XARPS.dtype09_heard[12], XARPS.dtype09_heardtime[12])
    print(" 13  ", XARPS.dtype09_heard[13], XARPS.dtype09_heardtime[13])
    print(" 14  ", XARPS.dtype09_heard[14], XARPS.dtype09_heardtime[14])
    print()
    print()
    print('- - - - - - - - - - - - - - - - - - - - -')
    print('  0       Back to Main Menu')
    print(' ')
    XARPS.message = XARPS.dtype09_pack()
    return

def set_dtype50():
    print()
    print("----- XARPS TYPE 50 HTTP -----")
    print()
    print("-------- TO BE ADDED ---------")
    print()
    print(' ')
    #XARPS.message = XARPS.dtype50_pack()
    programPause = input("Press the <ENTER> key to continue...")
    return

def set_dtype71():
    print()
    print("----- XARPS TYPE 71 Ident -----")
    print()
    print("-------- TO BE ADDED ----------")
    print()
    print(' ')
    #XARPS.message = XARPS.dtype71_pack()
    programPause = input("Press the <ENTER> key to continue...")
    return

def analyze_rx():
    while True:
        HASit.rx()
        XARPS.parse(HASit.receive_ascii)
        XARPS.debug()
        if XARPS.dtype == 1: # Battery
            XARPS.type01_debug()
        if XARPS.dtype == 2: # Time
            XARPS.type02_debug()
        if XARPS.dtype == 3: # Position
            XARPS.type03_debug()
        if XARPS.dtype == 4: # WX Update
            XARPS.type04_debug()
        if XARPS.dtype == 5: # Telemetry
            XARPS.type05_debug()
        if XARPS.dtype == 6: # Binary Data
            XARPS.type06_debug()
        if XARPS.dtype == 7: # Text (Default)
            XARPS.type07_debug()
        if XARPS.dtype == 8: # APRS
            XARPS.type08_debug()
        if XARPS.dtype == 9: # Last Seen Stations
            XARPS.type09_debug()
        if XARPS.dtype == 80:  # HTTP
            XARPS.type50_debug()
        if XARPS.dtype == 113: # Identd
            XARPS.type71_debug()

def analyze_file():
    global xpayload
    with open(xpayload, 'r') as fp:
        for line in fp:
            XARPS.parse(line)
            XARPS.debug()
            if XARPS.dtype == 1: # Battery
                XARPS.dtype01_debug(XARPS.message)
            if XARPS.dtype == 2: # Time
                XARPS.dtype02_debug(XARPS.message)
            if XARPS.dtype == 3: # Position
                XARPS.dtype03_debug(XARPS.message)
            if XARPS.dtype == 4: # WX Update
                XARPS.dtype04_debug(XARPS.message)
            if XARPS.dtype == 5: # Telemetry
                XARPS.dtype05_debug(XARPS.message)
            if XARPS.dtype == 6: # Binary Data
                XARPS.dtype06_debug(XARPS.message)
            if XARPS.dtype == 7: # Text (Default)
                XARPS.dtype07_debug(XARPS.message)
            if XARPS.dtype == 8: # APRS
                XARPS.dtype08_debug(XARPS.message)
            if XARPS.dtype == 9: # Last Seen Stations
                XARPS.dtype09_debug(XARPS.message)
            if XARPS.dtype == 80:  # HTTP
                XARPS.dtype50_debug(XARPS.message)
            if XARPS.dtype == 113: # Identd
                XARPS.dtype71_debug(XARPS.message)
        fp.close

#
# SETUP
#

MAX_PAYLOAD_LENGTH = 235

#
# MAIN
#
while True:
    menu_main()
    fun = input('Select menu item: ')  
    if fun=="1":
        menu_package()  
    elif fun=="2":
        menu_analyze()
    elif fun=="8": # XARPS Diagram
        about_xarps()
    elif fun=="9":
        XARPS.debug()
        #about_prog()
    elif fun=="0":
        exit(0)
    else:
        print ("Programmer error: unrecognized menu")
    pass
