#!/usr/bin/python3
#
#
# HASduckhunt
#
#
#  Usage: HASduckhunt.py 
#
#  DESCRIPTION
#
#     Duckhunt Gane Library
#
#  OPTIONS
#
#  
#  RELEASE: CAYMAN
#


#
# Import Libraries
#

import argparse 
import configparser
import sys
import time


#
# IMPORT ARGS
#

parser = argparse.ArgumentParser(description='HASduckhunt')
parser.add_argument('-l','--level', help='level of game play  SIMPLE, HARDER, HARDCORE', required=True)
args = vars(parser.parse_args())
gamelevel = args['level']

#
# Initialise Classes
#


class ducks:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.sections()
        self.config.read('HASviolet-duckhunt.ini')
        try:
            self.simple_message = str(self.config["SIMPLE"]["message"])
            self.simple_interval = str(self.config["SIMPLE"]["interval"])
            self.simple_trigger = str(self.config["SIMPLE"]["trigger"])
            self.simple_trigger_val = str(self.config["SIMPLE"]["trigger_val"])
            self.simple_action = str(self.config["SIMPLE"]["action"])
            self.simple_action_val = str(self.config["SIMPLE"]["action_val"])
            self.harder_message = str(self.config["HARDER"]["message"])
            self.harder_interval = str(self.config["HARDER"]["interval"])
            self.harder_trigger = str(self.config["HARDER"]["trigger"])
            self.harder_trigger_val = str(self.config["HARDER"]["trigger_val"])
            self.harder_action = str(self.config["HARDER"]["action"])
            self.harder_action_val = str(self.config["HARDER"]["action_val"])
            self.hardcore_message = str(self.config["HARDCORE"]["message"])
            self.hardcore_interval = str(self.config["HARDCORE"]["interval"])
            self.hardcore_trigger = str(self.config["HARDCORE"]["trigger"])
            self.hardcore_trigger_val = str(self.config["HARDCORE"]["trigger_val"])
            self.hardcore_action = str(self.config["HARDCORE"]["action"])
            self.hardcore_action_val = str(self.config["HARDCORE"]["action_val"])
        except KeyError as e:
            raise LookupError("Error HASviolet-duckhunt.ini: {} missing.".format(str(e)))
    
    def simple_game():
        pass

    def harder_game():
        pass

    def hardcore_game():
        pass

    def cardiac_game():
        pass

    def message(blahblah):
        hasvheader = HASit.station + ">" + "BEACON-99"
        hasvpayload = hasvheader + " | " + blahblah
        HASit.tx(hasvpayload)
        HAShat.OLED.fill(0)
        HAShat.OLED.text(hasvheader, 0, 1, 1)
        HAShat.OLED.text(hasvpayload, 0, 9, 1)
        HAShat.OLED.show()

    def interval(sleepytime):
        time.sleep(sleepytime)

    def trigger(self, gamelevel):
        # Trigger: Time, Elapsed Time, Sensor
        if hairpin=="T":
            hairpin = time.time()
        elif hairpin=="E":
            hairpin = int(time.time()_ - 
        elif self.simple_trigger=="S":
           
    def action():
        # Action: Evade Confuse Conspire
        print(level)
        if duck.simple_action=="E":
            duck.simple_action
        elif duck.simple_action=="C":
            duck.simple_action
        elif duck.simple_action=="O":
        

#
# MAIN
#

HAShat.logo('hvdn-logo.xbm')

Duck = ducks()

# CTRL-C is SIGINT and closes program gracefully
signal.signal(signal.SIGINT, sigs_handler)
signal.signal(signal.SIGTERM, sigs_handler)

main_menu()

while True:
    happening = trigger(gamelevel)
    if happening:
        action(gamelevel)
