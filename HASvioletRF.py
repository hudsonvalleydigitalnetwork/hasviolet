#!/usr/bin/python3
#
# HASviolet RF Library 
#
#   REVISION: 20210312-1400
#
#

#
# Import Libraries
#

import argparse 
import configparser
import signal
import sys
import time
import json
import subprocess
from HASrf95 import RF95, Bw125Cr45Sf128
from pyLoraRFM9x import LoRa, ModemConfig
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
HASviolet_LOGIN = HASviolet_SRVDIR + "HASviolet_LOGIN.html"
HASviolet_LOGINCSS = HASviolet_SRVDIR + "HASviolet_LOGIN.css"
HASviolet_INDEX = HASviolet_SRVDIR + "HASviolet_INDEX.html"
HASviolet_INDEXCSS = HASviolet_SRVDIR + "HASviolet.css"
HASvioletjs = HASviolet_SRVDIR + "HASviolet.js"
HVDN_LOGO = HASviolet_ETC + "HVDN_logo.xbm"


#
# VARIABLES
#


#
# CLASSES
#

class HASrf:
    def __init__(self):
        self.cfgjson = HASviolet_CONFIG
        with open(self.cfgjson) as configFileJson:
            jsonConfig = json.load(configFileJson)
        self.radio = jsonConfig["RADIO"]["rfmodule"]
        self.modemconfig = jsonConfig["RADIO"]["modemconfig"]
        self.modem = jsonConfig["RADIO"]["modem"]
        self.frequency = jsonConfig["RADIO"]["frequency"]
        self.spreadfactor = jsonConfig["RADIO"]["spreadfactor"]
        self.codingrate4 = jsonConfig["RADIO"]["codingrate4"]
        self.bandwidth = jsonConfig["RADIO"]["bandwidth"]
        self.txpwr = jsonConfig["RADIO"]["txpwr"]
        self.mycall = jsonConfig["CONTACT"]["mycall"]
        self.myssid = jsonConfig["CONTACT"]["myssid"]
        self.mybeacon = jsonConfig["CONTACT"]["mybeacon"]
        self.dstcall = jsonConfig["CONTACT"]["dstcall"]
        self.dstssid = jsonConfig["CONTACT"]["dstssid"]
        self.mystation = self.mycall + "-" + str(self.myssid)
        
        self.bw_dict = {        # Bandwidth in Hz
            7800: 0x00,
            10000: 0x10,
            15000: 0x20,
            20000: 0x30,
            31250: 0x40,
            41700: 0x50,
            62500: 0x60,
            125000: 0x70,
            250000: 0x80,
            500000: 0x90
        }
        self.cr_dict = {        # Coding Rate
            5: 0x02,            # 4_5
            6: 0x04,            # 4_6
            7: 0x06,            # 4_7
            8: 0x08             # 4_8
        }
        self.imphead_dict = {
            True: 0x00,
            False: 0x01
        }
        self.sf_dict = {        # Spread factor
            6: 0x60,            # 64 CPS
            7: 0x70,            # 128 CPS
            8: 0x80,            # 256 CPS
            9: 0x90,            # 512 CPS
            10: 0xa0,           # 1024 CPS
            11: 0xb0,           # 2048 CPS
            12: 0xc0            # 4096 CPS
        }
        self.txcont_dict = {    # TX Continuous mode
            True: 0x08,
            False: 0x00
        }
        self.crc_dict = {       # Payload CRC
            True: 0x04,
            False: 0x00
        }
        self.agc_dict = {       # AGC On
            True: 0x04,
            False: 0x00
        }
        self.symbtimeout = 0x03
        return

    def startradio(self):       # rf95 Library
        if self.radio == "RFM9X":
            self.radio_cs = 1
            self.radio_irq = 22
            self.radio_nodeaddress = 1
            self.rfm = RF95(cs=self.radio_cs, int_pin=self.radio_irq, reset_pin=None)
            #self.rfm.set_modem_config(self.modemconfig)
            self.rfm.set_frequency(self.frequency/1000000)
            self.rfm.set_tx_power(self.txpwr)
            self.rfm.init()
        return

    def startradio_pyl(self):   # pyLoraRFM9x Library
        if self.radio == "RFM9X":
            self.radio_cs = 1
            self.radio_irq = 22
            self.radio_nodeaddress = 1
            self.rfm = LoRa(1, self.radio_irq, 2, reset_pin = self.radio_cs, freq=(self.frequency/1000000), modem_config=ModemConfig.Bw125Cr45Sf128, tx_power=14, acks=False)
        return

    def showmodemconfig(self, bw, cr, sf):       # rf95 Library
        lbandwidth = self.bw_dict[bw]
        lcoding_rate = self.cr_dict[cr]
        limplicit_header= self.imphead_dict[True]
        lspreadfactor = self.sf_dict[sf]
        ltxcont = self.txcont_dict[False]
        lcrc = self.crc_dict[True]
        lsymb_timeout = self.symbtimeout
        lagc_auto = self.agc_dict[False]
        print ("--")
        print ("-- ModemConfig Registers")
        print ("--")
        print ("                     Bandwidth = ", hex(lbandwidth))
        print ("                    CodingRate = ", hex(lcoding_rate))
        print ("                   ImplicitHDR = ", hex(limplicit_header))
        print ("- - - - - - - - - - - - - - - - - - - - - -")
        print ("spi_write(REG_1D_MODEM_CONFIG1 = ", hex(lbandwidth|lcoding_rate|limplicit_header))
        print (" ")
        print ("                  SpreadFactor = ", hex(lspreadfactor))
        print ("                 TX Continuous = ", hex(ltxcont))
        print ("                    CRC Enable = ", hex(lcrc))
        print ("                   SymbTimeout = ", hex(lsymb_timeout))
        print ("- - - - - - - - - - - - - - - - - - - - - -")
        print ("spi_write(REG_1E_MODEM_CONFIG2 = ", hex(lspreadfactor|ltxcont|lcrc|lsymb_timeout))
        print (" ")
        print ("                      AGC Auto = ", hex(lagc_auto))
        print ("- - - - - - - - - - - - - - - - - - - - - -")
        print ("spi_write(REG_26_MODEM_CONFIG3 = ",hex(lagc_auto))
        print (" ")
        return

    def custommodemconfig(self, bw, cr, sf):     # rf95 Library
        lbandwidth = self.bw_dict[bw]
        lcoding_rate = self.cr_dict[cr]
        limplicit_header= self.imphead_dict[True]
        lspreadfactor = self.sf_dict[sf]
        ltxcont = self.txcont_dict[False]
        lcrc = self.crc_dict[True]
        lsymb_timeout = self.symbtimeout
        lagc_auto = self.agc_dict[False]
        self.rfm.spi_write(REG_1D_MODEM_CONFIG1, lbandwidth | lcoding_rate | limplicit_header)
        self.rfm.spi_write(REG_1E_MODEM_CONFIG2, lspreadfactor | ltxcont | lcrc | lsymb_timeout)
        self.rfm.spi_write(REG_26_MODEM_CONFIG3, lagc_auto)    
        return

    def cleanup(self):              # rf95 Library
        self.rfm.cleanup()

    def cleanup_pyl(self):          # pyLoraRFM9x Library
        self.rfm.close()

    def rx(self):                   # rf95 Library
        if self.radio=="RFM9X":
            while not self.rfm.available():
                pass
            self.receive = self.rfm.recv()
            self.receive_rssi = str(int(self.rfm.last_rssi))
            self.receive_string = str(self.receive)
            self.receive_ascii=""
            for i in self.receive:
                self.receive_ascii=self.receive_ascii+chr(i)
        return

    def onreceive(payload):         # pyLoraRFM9x Library
        if self.radio=="RFM9X":
            if (arg_signal_rssi):
                #datadisplay_string = 'RX:'+ HASit.receive_ascii +':RSSI:'+HASit.receive-rssi
                print (payload.message,':RSSI:',payload.rssi,":SNR:", payload.snr)
            else:
                print (HASit.receive_ascii)

    def transmit(self, data):       # rf95 Library
        # Send message
        self.rfm.send(self.str_to_data(data))
        self.rfm.wait_packet_sent()

    def ontransmit(self, data):     # pyLoraRFM9x Library
        # Send message
        self.rfm.send(data, 1, 255, 0)
        self.rfm.wait_packet_sent()

    # helper method to send bytes
    @staticmethod
    def bytes_to_data(bytelist):
        return list(bytelist)

    # helper method to send strings
    @staticmethod
    def str_to_data(string):
        return [ord(c) for c in string]
