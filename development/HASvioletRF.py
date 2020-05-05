#!/usr/bin/python3
#
# HASvioletRF Library 2
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


class HASrf:
    def __init__(self):
        iniconfig = configparser.ConfigParser()
        iniconfig.sections()
        iniconfig.read('HASviolet.ini')
        try:
            self.gpio_rfm_cs = int(iniconfig["DEFAULT"]["gpio_rfm_cs"])
            self.gpio_rfm_irq = int(iniconfig["DEFAULT"]["gpio_rfm_irq"])
            self.node_address = int(iniconfig["DEFAULT"]["node_address"])
            self.freqmhz = float(iniconfig["DEFAULT"]["freqmhz"])
            self.txpwr = int(iniconfig["DEFAULT"]["txpwr"])
            self.modemcfg = str(iniconfig["DEFAULT"]["modemcfg"])
            self.mycall = str(iniconfig["DEFAULT"]["mycall"])
            self.ssid = int(iniconfig["DEFAULT"]["ssid"])
            self.beacon = str(iniconfig["DEFAULT"]["beacon"])
        except KeyError as e:
            raise LookupError("Error HASviolet.ini[DEFAULT] : {} missing.".format(str(e)))
            exit (1)
        self.station = self.mycall + "-" + str(self.ssid)
        self.rf95 = RF95(cs=self.gpio_rfm_cs, int_pin=self.gpio_rfm_irq, reset_pin=None)
        self.rf95.set_frequency(self.freqmhz)
        self.rf95.set_tx_power(self.txpwr)
        self.rf95.init()
        self.receive = ""
        self.receive_rssi = ""
        self.receive_string = ""
        self.receive_ascii=""
        
    def cleanup(self):
        self.rf95.cleanup()  

    def rx(self):
        while not self.rf95.available():
            pass
        self.receive = self.rf95.recv()
        self.receive_rssi = str(int(self.rf95.last_rssi))
        self.receive_string = str(self.receive)
        self.receive_ascii=""
        for i in self.receive:
            self.receive_ascii=self.receive_ascii+chr(i)
        return
   
    def tx(self, data):
        # Send message
        self.rf95.send(self.str_to_data(data))
        self.rf95.wait_packet_sent()
    
    # helper method to send bytes
    @staticmethod
    def bytes_to_data(bytelist):
        return list(bytelist)

    # helper method to send strings
    @staticmethod
    def str_to_data(string):
        return [ord(c) for c in string]

   