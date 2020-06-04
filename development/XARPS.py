#!/usr/bin/python3
#
# XARPS Library - 20200603
#
#
# XARPS stands for eXtensible Amateur Radio Payload Specification. Referencing the
# Open Systems Interconnection model (OSI model), XARPS is an application layer protocol 
# with link-level awareness for use by RF systems providing application level connectivity 
# to other networked systems. ASCII (UTF-8) is used throughout the specification
#

#
# LIBRARIES
#

import time
import struct
import binascii
import pynmea2
import metar
from metar import Metar

# 
# FIELDS
#

#|     Source      |   Destination   |   Options    |   Data Type  |         Data       |
#| --------------- | --------------- | ------------ | ------------ | ------------------ |
#| 9 byte (string) | 9 byte (string) | 1 byte (int) | 1 byte (int) | 235 bytes (string) |


#
# Source and Destination
#
#
# Each contain callsign/handle with SSID. Field size supports IARU decision for 7 character
# callsigns. Right justifed text with left side padding used. Examples, GB2ABC50, WA1BCDE50, PURPLE53
#
# BEACON99 is a reserved word in the destination field for messages to ALL (Broadcast).
# You can change the SSID (99) to another number for multicast purposesn.
#
#|  BEACON-XX  |         Target         |
#|  ---------- | ---------------------- |
#|     99      |      ALL stations      |
#|     89      |      ALL gateways      |
#|     79      |    ALL RAN stations    |
#|     69      | ALL Local RAN Stations |


#
# Options Field
#
#|    Value     |        Option        |             Description          |
#| ------------ | -------------------- | -------------------------------- |
#|  0x00-0x05   |       Reserved       |                                  |
#|     0x06     |     ACK Response     |  ACK reply                       |
#|     0x07     |     ACK Request      |  Send ACK                        |


#
# Data Type Field
#
#|    Value     |         Type         |            Description              |
#| ------------ | -------------------- | ----------------------------------- |
#|     0x00     |       Reserved       |  Reserved                           |
#|     0x01     |        Battery       |  Battery voltage update             |
#|     0x02     |         Time         |  Current time payload               |
#|     0x03     |    Position Update   |  GPS position update                |
#|     0x04     |     Weather Update   |  Weather station data               |
#|     0x05     |       Telemetry      |  Telemetry                          |
#|     0x06     |      Binary Data     |  Binary Data Transport              |
#|     0x07     |     Text Message     |  Text message between stations      |
#|     0x08     |         APRS         |  APRS encapsulates                  |
#|     0x09     |  Last Seen Stations  |  Digest of recent stations          |
#|   0x0A-0x23  |        Reserved      |  Reserved                           |
#|     0x50     |         HTTP         |  HTTP                               |
#|     0x71     |        Ident         |  Ident                              |


#
# TYPE 01 Battery Message
#
#|    Voltage    |    Current    |   Capacity    |
#|               |  Consumption  |               |
#| ------------- | ------------- | ------------- |
#|    8 bytes    |    8 bytes    |    1 byte     |
#|    (float)    |    (float)    |   (integer)   |


#
# TYPE 02 Time Message
#
#|     EPOC      |    Systems    |      Local    |
#|   Time(sec)   |  Uptime(sec)  |      Time     |
#| ------------- | ------------- | ------------- |
#|    8 bytes    |    8 bytes    |    28 byte    |
#|    (float)    |    (float)    |    (String)   |


#
# TYPE 03 Position Message
#
#| Timestamp |   Object  |  Latitude  |  Longitude  | Altitude | Altitude  | 
#|   (EPOC)  |    Type   |            |             |          |   Units   | 
#| --------- | --------- | ---------- | ----------- | -------- | --------- | 
#|  8 bytes  |  1 byte   |   8 bytes  |   8 bytes   |  8 bytes |  1 byte   |  
#|  (float)  | (integer) |   (float)  |   (float)   |  (float) | (integer) |


# 
# TYPE 03 Position Message - Object Type
#
#|  Value |     Description        |
#|  ----- | ---------------------- |
#|    0   |  static land station   |
#|    1   |  handheld              |
#|    2   |  pedestrian            |
#|    3   |  civilian vehicle      |
#|    4   |  commercial vehicle    |
#|    5   |  police vehicle        |
#|    6   |  medical vehicle       |
#|    7   |  fire vehicle          |
#|    8   |  Federal Vehicle       |
#|    9   |  Command vehicle       |
#|   10   |  marina                |
#|   11   |  float                 |
#|   12   |  swimmer               |
#|   13   |  civilian boat         |
#|   14   |  commercial boat       |
#|   15   |  police boat           |
#|   16   |  fire boat             |
#|   17   |  Coast Guard           |
#|   18   |  Command boat          |
#|   19   |  RESERVED future use   |
#|   20   |  Airport               |
#|   21   |  UAV                   |
#|   22   |  Experimental Manned   |    
#|   23   |  Civilian Helicopter   |
#|   24   |  Civilian Fixed Wing   |
#|   25   |  Commercial Fixed Wing |
#|   26   |  Police Helicopter     |
#|   27   |  Medical Helicopter    |
#|   28   |  Federal Helicopter    |
#|   29   |  RESERVED future use   |
#|   30   |  Active Emergency      |
#|   31   |  Traffic Stop          |
#|   32   |  Hazard Area           |
#| 33-255 |  RESERVED future use   |

# 
# TYPE_04 Weather Update
# 
#| Timestamp |  Latitude  |  Longitude  | Temperature |    Temp    |  Humidity  |  Barometer  |    Wind    |    Wind    |  Wind Speed  |
#|   (EPOC)  |            |             |             |    Units   |            |             | Direction  |   Speed    |  Direction   |
#| --------- | ---------- | ----------- | ----------- | ---------- | ---------- | ----------- | ---------- | ---------- | ------------ |
#|  8 bytes  |  8 bytes   |   8 bytes   |   1 byte    |   1 byte   |   8 bytes  |   8 bytes   |   8 bytes  |   8 bytes  |    1 byte    |
#|  (float)  |  (float)   |   (float)   |  (integer)  |  (integer) |   (float)  |   (float)   |   (float)  |   (float)  |   (integer)  |

# 
# TYPE_05 Telemetry
#
#|          Message       |
#|  --------------------- |
#|   235 bytes (string)   |

# 
# TYPE_6 Binary Data
# 
#|          Message       |
#|  --------------------- |
#|   235 bytes (string)   |
#


# 
# TYPE_7 Text Message (Default)
# 
#|          Message       |
#|  --------------------- |
#|   235 bytes (string)   |
#

# 
# TYPE_8 Binary Data
# 
#|          Message       |
#|  --------------------- |
#|   235 bytes (string)   |
#

# 
# TYPE_9 Last Seen Stations
#
# Comma delimitted list of stations heard in the last 15  (900 Seconds)
# 
#|  Station(0)  |  Timestamp  |  Station(..)  |  Timestamp(..)  |  Station(14)  |  Timestamp(14) |
#| ------------ | ----------- | ------------- | --------------- | ------------- | -------------- | 
#|    9 bytes   |   8 bytes   |     9 bytes   |      8 bytes    |     9 bytes   |     8 bytes    |
#|   (string)   |   (float)   |    (string)   |      (float)    |    (string)   |     (float)    |

# 
# TYPE_50 HTTP
# 
#|          Message       |
#|  --------------------- |
#|   235 bytes (string)   |
#

# 
# TYPE_71 IDENT
# 
#|          Message       |
#|  --------------------- |
#|   235 bytes (string)   |
#



#
# VARIABLES
#

MAX_PAYLOAD_LENGTH = 235


#
# CLASSES
#

class XARPS:
    def __init__ (self, source = ' NOCALL00', destination = ' NOCALL00'):
        self.source = source.upper()
        self.destination = destination.upper()
        #
        self.options = int(0)
        self.OPT_05_RESERVED = False
        self.OPT_06_ACKREPLY = False
        self.OPT_07_ACK = False
        #
        self.dtype = int(5)
        #
        self.dtype01_voltage = float (13.1)
        self.dtype01_current = float (0.1)
        self.dtype01_capacity = float (100.0)
        #
        with open('/proc/uptime', 'r') as f:
            uptime_seconds = float(f.readline().split()[0])
        f.close
        self.dtype02_time = float(time.time())
        self.dtype02_uptime = float(uptime_seconds)
        self.dtype02_ctime = str(time.ctime())
        #
        self.dtype03_timestamp = float(time.time())
        self.dtype03_object = int(0)
        self.dtype03_lat = float (0)
        self.dtype03_lon = float (0)
        self.dtype03_altitude = int(0)
        self.dtype03_altunits = 'F'
        #
        self.dtype04_timestamp = float(time.time())
        self.dtype04_lat = float (0)
        self.dtype04_lon = float (0)
        self.dtype04_temperature = float (0)
        self.dtype04_tempunits = 'F'
        self.dtype04_humidity = float (0)
        self.dtype04_barometer = float (0)
        self.dtype04_winddir = float (0)
        self.dtype04_windspeed = float (0)
        self.dtype04_windspun = 'M'
        #
        self.dtype05_msg = ''
        #
        self.dtype06_msg = ''
         #
        self.dtype07_msg = ''
        #
        self.dtype08_msg = ''
        #
        self.dtype09_heard = [' NOCALL00',' NOCALL00',' NOCALL00',' NOCALL00',' NOCALL00',' NOCALL00',' NOCALL00'\
            ,' NOCALL00',' NOCALL00',' NOCALL00',' NOCALL00',' NOCALL00',' NOCALL00',' NOCALL00',' NOCALL00']
        self.dtype09_heardtime = [900, 900, 900, 900, 900, 900, 900, 900, 900, 900, 900, 900, 900, 900, 900, 900]
        #
        self.stype = 0
        self.message = ''
        
    def parse(self, data):
        self.source = data[0:9]
        self.destination = data[10:18]
        self.options = data[18]
        self.dtype = data[19]
        self.message = data[20:255]
    
    def pack(self):
        # pack payload
        if self.dtype == 1:
            self.message = self.dtype01_pack()
        elif self.dtype == 2:
            self.message = self.dtype02_pack()
        elif self.dtype == 3:
            self.message = self.dtype03_pack()
        elif self.dtype == 4:
            self.message = self.dtype04_pack()
        elif self.dtype == 5:
            self.message = str(self.message)
        elif self.dtype == 6:
            self.message = str(self.message)
        elif self.dtype == 7:
            self.message = self.dtype07_pack()
        elif self.dtype == 8:
            self.message = self.dtype08_pack()
        elif self.dtype == 9:
            self.message = self.dtype09_pack()
        elif self.dtype == 80:
            self.message = self.dtype50_pack()
        elif self.dtype == 113:
            self.message = self.dtype71_pack()
        else:
            exit(0)
        payload = str(self.source) + str(self.destination) + str(self.options) + str(self.dtype) + str(self.message)
        return(payload)

    def parse_options(self, data):
        self.OPT_01_RESERVED = False
        self.OPT_02_RESERVED = False
        self.OPT_03_RESERVED = False
        self.OPT_04_RESERVED = False
        self.OPT_05_RESERVED = False
        if data == 7:
            self.OPT_07_ACK = True
            self.OPT_06_ACKREPLY = False
        elif data == 6:
            self.OPT_07_ACK = False
            self.OPT_06_ACKREPLY = True
        else:
            self.OPT_07_ACK = False
            self.OPT_06_ACKREPLY = False
    
    def dtype01_parse(self, data):
        self.dtype01_voltage, self.dtype01_current, self.dtype01_capacity = data.split(',')

    def dtype01_pack(self):
        data = str(self.dtype01_voltage) + "," + str(self.dtype01_current) + "," + str(self.dtype01_capacity)
        return(data)

    def dtype02_parse(self, data):
        self.dtype02_time, self.dtype02_uptime, self.dtype02_ctime = data.split(',')
        return
    
    def dtype02_pack(self):
        data = (str(self.dtype02_time) + "," +  str(self.dtype02_uptime) + "," + str(self.dtype02_ctime))
        return (data)

    def dtype03_parse(self, data):
        self.dtype03_timestamp, self.dtype03_lat, self.dtype03_lon, \
        self.dtype03_altitude, self.dtype03_altunits = data.split(',')
    
    def dtype03_pack(self):
        data = (str(self.dtype03_timestamp) + "," + str(self.dtype03_lat) + "," + str(self.dtype03_lon)\
            + str(self.dtype03_altitude) + "," + str(self.dtype03_altunits))
        return(data)

    def dtype04_parse(self, data):
        self.dtype04_timestamp, self.dtype04_lat, self.dtype04_lon, self.dtype04_temperature, self.dtype04_tempunits,\
             self.dtype04_humidity, self.dtype04_barometer, self.dtype04_windir, self.dtype04_windspeed, self.dtype04_windspun = data.split(',')
    
    def dtype04_pack(self):
        data = (str(self.dtype04_timestamp) + "," + str(self.dtype04_lat) + "," + str(self.dtype04_lon) + "," + str(self.dtype04_temperature)\
            + "," + str(self.dtype04_tempunits) + "," + str(self.dtype04_humidity) + "," + str(self.dtype04_barometer)\
                 + "," + str(self.dtype04_winddir) + "," + str(self.dtype04_windspeed) + "," + str(self.dtype04_windspun))
        return(data)

    def dtype05_parse(self, data):
        data = data
    def dtype05_pack(self):
        return(self.message)

    def dtype06_parse(self, data):
        data = data
    def dtype06_pack(self):
        return(self.message)

    def dtype07_parse(self, data):
        data = data
    def dtype07_pack(self):
        return(self.message)

    def dtype08_parse(self, data):
        data = data
    def dtype08_pack(self):
        return(self.message)

    def dtype09_parse(self, data):
        lastheard = data.split(',')
        self.dtype09_heard[0] = lastheard[0]
        self.dtype09_heardtime[0] = int(lastheard[1])
        self.dtype09_heard[1] = lastheard[2]
        self.dtype09_heardtime[1] = int(lastheard[3])
        self.dtype09_heard[2] = lastheard[4]
        self.dtype09_heardtime[2] = int(lastheard[5])
        self.dtype09_heard[3] = lastheard[6]
        self.dtype09_heardtime[3] = int(lastheard[7])
        self.dtype09_heard[4] = lastheard[8]
        self.dtype09_heardtime[4] = int(lastheard[9])
        self.dtype09_heard[5] = lastheard[10]
        self.dtype09_heardtime[5] = int(lastheard[11])
        self.dtype09_heard[6] = lastheard[12]
        self.dtype09_heardtime[6] = int(lastheard[13])
        self.dtype09_heard[7] = lastheard[14]
        self.dtype09_heardtime[7] = int(lastheard[15])
        self.dtype09_heard[8] = lastheard[16]
        self.dtype09_heardtime[8] = int(lastheard[17])
        self.dtype09_heard[9] = lastheard[18]
        self.dtype09_heardtime[9] = int(lastheard[19])
        self.dtype09_heard[10] = lastheard[20]
        self.dtype09_heardtime[10] = int(lastheard[21])
        self.dtype09_heard[11] = lastheard[22]
        self.dtype09_heardtime[11] = int(lastheard[23])
        self.dtype09_heard[12] = lastheard[24]
        self.dtype09_heardtime[12] = int(lastheard[25])
        self.dtype09_heard[13] = lastheard[26]
        self.dtype09_heardtime[13] = int(lastheard[27])
        self.dtype09_heard[14] = lastheard[28]
        self.dtype09_heardtime[14] = int(lastheard[29])
        return

    def dtype09_pack(self):
        data = self.dtype09_heard[0] + "," + str(self.dtype09_heardtime[0]) + ","\
             + self.dtype09_heard[1] + "," + str(self.dtype09_heardtime[1]) + ","\
             + self.dtype09_heard[2] + "," + str(self.dtype09_heardtime[2]) + ","\
             + self.dtype09_heard[3] + "," + str(self.dtype09_heardtime[3]) + ","\
             + self.dtype09_heard[4] + "," + str(self.dtype09_heardtime[4]) + ","\
             + self.dtype09_heard[5] + "," + str(self.dtype09_heardtime[5]) + ","\
             + self.dtype09_heard[6] + "," + str(self.dtype09_heardtime[6]) + ","\
             + self.dtype09_heard[7] + "," + str(self.dtype09_heardtime[7]) + ","\
             + self.dtype09_heard[8] + "," + str(self.dtype09_heardtime[8]) + ","\
             + self.dtype09_heard[9] + "," + str(self.dtype09_heardtime[9]) + ","\
             + self.dtype09_heard[10] + "," + str(self.dtype09_heardtime[10]) + ","\
             + self.dtype09_heard[11] + "," + str(self.dtype09_heardtime[11]) + ","\
             + self.dtype09_heard[12] + "," + str(self.dtype09_heardtime[12]) + ","\
             + self.dtype09_heard[13] + "," + str(self.dtype09_heardtime[13]) + ","\
             + self.dtype09_heard[14] + "," + str(self.dtype09_heardtime[14])
        return(data)

    def dtype50_parse(self, data):
        data = data
    def dtype50_pack(self):
        return(self.message)

    def dtype71_parse(self, data):
        data = data
    def dtype71_pack(self):
        return(self.message)

    def debug(self):
        print()
        print("---------------- XARPS ------------------")
        print()
        print("---------------- HEADER -----------------")
        print("            source :", self.source)
        print("       destination :", self.destination)
        print("           options :", self.options)
        print("         data type :", self.dtype)
        print()
        print("---------------- OPTIONS ----------------")
        print("   OPT_06_ACKREPLY :", self.OPT_06_ACKREPLY)
        print("        OPT_07_ACK :", self.OPT_07_ACK)
        print()
        print("---------------- PAYLOAD ----------------")
        print(self.message)
        print()
        return

    def dtype01_debug(self, data):
        print("-----------------------------------------")
        print("------ DATA TYPE 01 Battery Message -----")
        print("-----------------------------------------")
        print("          Voltage :", self.dtype01_voltage)
        print("          Current :", self.dtype01_current)
        print("         Capacity :", self.dtype01_capacity)
        print("-----------------------------------------")
        return

    def dtype02_debug(self, data):
        print("-----------------------------------------")
        print("-------- DATA TYPE 02 Time Message ------")
        print("-----------------------------------------")
        print("   EPOC Time (sec): ", self.dtype02_time)
        print("  Sys Uptime (sec): ", self.dtype02_uptime)
        print("        Local time: ", self.dtype02_ctime)
        print("-----------------------------------------")
        return
          
    def dtype03_debug(self, data):
        print("-----------------------------------------")
        print("------ DATA TYPE 03 Position Update -----")
        print("-----------------------------------------")
        print("         Timestamp:", self.dtype03_timestamp)
        print("       Object Type:", self.dtype03_object)
        print("          Latitude:", self.dtype03_lat)
        print("         Longitude:", self.dtype03_lon)
        print()
        print("          Altitude:", self.dtype03_altitude)
        print("         Alt Units:", self.dtype03_altunits)
        print("-----------------------------------------")
        return

    def dtype04_debug(self, data):
        print("-----------------------------------------")
        print("-------- DATA TYPE 04 WX Message --------")
        print("-----------------------------------------")
        print("         Timestamp:", self.dtype04_timestamp)
        print("          Latitude:", self.dtype04_lat)
        print("         Longitude:", self.dtype04_lon)
        print("       Temperature:", self.dtype04_temperature)
        print("        Temp Units:", self.dtype04_tempunits)
        print("          Humidity:", self.dtype04_humidity)
        print("         Barometer:", self.dtype04_barometer)
        print("    Wind Direction:", self.dtype04_winddir)
        print("        Wind Speed:", self.dtype04_windspeed)
        print("  Wind Speed Units:", self.dtype04_windspun)
        print("-----------------------------------------")    
