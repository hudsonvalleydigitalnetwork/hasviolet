#!/usr/bin/python3
#
# HASvioletRF Library
#
#
#
#
# TO-DO:
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
import subprocess
from rf95 import RF95, Bw31_25Cr48Sf512
from sx1262 import SX1262

class HASrf:
    def __init__(self):
        iniconfig = configparser.ConfigParser()
        iniconfig.sections()
        iniconfig.read('HASviolet.ini')
        try:
            self.radio = str(iniconfig["CURRENT"]["radio"])
            self.node_address = int(iniconfig["CURRENT"]["node_address"])
            self.freqmhz = float(iniconfig["CURRENT"]["freqmhz"])
            self.txpwr = int(iniconfig["CURRENT"]["txpwr"])
            self.modemcfg = str(iniconfig["CURRENT"]["modemcfg"])
            self.mycall = str(iniconfig["CURRENT"]["mycall"])
            self.myssid = int(iniconfig["CURRENT"]["myssid"])
            self.mybeacon = str(iniconfig["CURRENT"]["mybeacon"])
        except KeyError as e:
            raise LookupError("Error HASviolet-cayman.ini[DEFAULT] : {} missing.".format(str(e)))
        if self.radio=="RFM95":
            try:
                self.radio_cs = int(iniconfig["RFM95"]["rfm_cs"])
                self.radio_irq = int(iniconfig["RFM95"]["rfm_irq"])
                self.radio_nodeaddress = int(iniconfig["RFM95"]["node_address"])
                self.radio_modemcfg = str(iniconfig["RFM95"]["modemcfg"])
                self.radio_bandwidth = float(iniconfig["RFM95"]["bandwidth"])
                self.radio_spreadfactor = int(iniconfig["RFM95"]["spreadfactor"])
                self.radio_codingrate = int(iniconfig["RFM95"]["codingrate"])
                self.radio_crc = int(iniconfig["RFM95"]["rfm_crc"])
            except KeyError as e:
                raise LookupError("Error HASviolet.ini[DEFAULT] : {} missing.".format(str(e)))
        if self.radio=="SX1262":
            try:
                self.radio_cs = int(iniconfig["SX1262"]["rfm_cs"])
                self.radio_irq = int(iniconfig["SX1262"]["rfm_irq"])
                self.radio_nodeaddress = int(iniconfig["SX1262"]["node_address"])
                self.radio_modemcfg = str(iniconfig["SX1262"]["modemcfg"])
                self.radio_bandwidth = float(iniconfig["SX1262"]["bandwidth"])
                self.radio_spreadfactor = int(iniconfig["SX1262"]["spreadfactor"])
                self.radio_codingrate = int(iniconfig["SX1262"]["codingrate"])
                self.radio_crc = int(iniconfig["SX1262"]["rfm_crc"])
            except KeyError as e:
                raise LookupError("Error HASviolet.ini[DEFAULT] : {} missing.".format(str(e)))
        self.mystation = self.mycall + "-" + str(self.myssid)
        self.receive = ""
        self.receive_rssi = ""
        self.receive_string = ""
        self.receive_ascii=""
        if self.radio=="RFM95":
            self.rfm = RF95(cs=self.radio_cs, int_pin=self.radio_irq, reset_pin=None)
            self.rfm.set_frequency(self.freqmhz)
            self.rfm.set_tx_power(self.txpwr)
            self.rfm.init()
        if self.radio=="SX1262":
            self.rfm = SX1262(cs='P5',irq='P6',rst='P7',gpio='P8')
            self.rfm.begin(freq=self.freqmhz, bw=self.radio_bandwidth, sf=self.radio_spreadfactor, cr=self.radio_codingrate, 
                syncWord=0x12, power=self.txpwr, currentLimit=60.0, preambleLength=8,
                implicit=False, implicitLen=0xFF,
                crcOn=True, txIq=False, rxIq=False, 
                tcxoVoltage=1.6, useRegulatorLDO=False, blocking=True)
            self.rfm.set_frequency(self.freqmhz)
            self.rfm.set_tx_power(self.txpwr)
            self.rfm.init()

    def cleanup(self):
        self.rfm.cleanup()

    def rx(self):
        if self.radio=="RFM95":
            while not self.rfm.available():
                pass
            self.receive = self.rfm.recv()
            self.receive_rssi = str(int(self.rfm.last_rssi))
            self.receive_string = str(self.receive)
            self.receive_ascii=""
            for i in self.receive:
                self.receive_ascii=self.receive_ascii+chr(i)
        if self.radio=="SX1262":
            while True:
                msg = self.rfm.recv()
                if len(msg) > 0:
                    self.receive_ascii = msg
                pass
        return
   
    def tx(self, data):
        # Send message
        self.rfm.send(self.str_to_data(data))
        self.rfm.wait_packet_sent()

    # helper method to send bytes
    @staticmethod
    def bytes_to_data(bytelist):
        return list(bytelist)

    # helper method to send strings
    @staticmethod
    def str_to_data(string):
        return [ord(c) for c in string]

   