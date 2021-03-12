#!/bin/bash

###
### HASviolet_install_update
###
###

##
##    REVISION: 20210312-1400
## 

##
##
## This script is part of the HASviolet project.
##
## Given a Raspbian Lite image, this script will install all the packegs, libraries, and github repo
## required to implement the HVDN Communicator.
##
## HASviolet has been design with the Raspberry Pi Zero Wireless providing compute, Radio Modules
## accessible via SPI, sensors via i2c, and GPS via microUSB besides i2c. Generic Python Libraries
## for i2c and SPI are installed as well as Adafruit and Sparkfun for specific devcies that include
## the following.
## 
##
## Adafruit LoRa Radio Bonnet with OLED RFM95W @ 915 MHz
## https://www.adafruit.com/product/4074
##
## Adafruit Monochrome OLEDs based on SSD1306 drivers
## https://github.com/adafruit/Adafruit_SSD1306
##
## Adafruit_CircuitPython_framebuf
## https://github.com/adafruit/Adafruit_CircuitPython_framebuf
##
## Sparkfun Qwiic Python Package
## https://github.com/sparkfun/Qwiic_Py
##
## pyRF95
## https://github.com/ladecadence/pyRF95
##
##
## REVISION: 20210308-0900
##
##
##
##

##
## INIT VARIABLES 
##

# GitHub Repos
hasviolet_github_repo="https://github.com/hudsonvalleydigitalnetwork/hasviolet.git"

# Local (GitHub clone)
hasviolet_install=$HOME/hasviolet

# HASviolet JSON file
hasviolet_json=$hasviolet_install/cfg/hasVIOLET.json

# HASviolet SSL Cert and Key
hasviolet_ssl_key=$hasviolet_install/cfg/hasVIOLET.key
hasviolet_ssl_crt=$hasviolet_install/cfg/hasVIOLET.crt


##
##  START 
##

echo " "
echo "HASviolet Install Update"
echo " "

cd $HOME

#
# Ensure this is HASviolet clean
#
echo " "
echo "- Prep the environment"
echo " "
echo "-- Kill and remove HASviolet_websox service"
sudo systemctl stop HASviolet_websox.service >/dev/null 2>&1
sudo systemctl disable HASviolet_websox.service >/dev/null 2>&1
sudo rm -rf /lib/systemd/system/HASviolet.service >/dev/null 2>&1
echo "-- Backup JSON and SSL Cert/Key"
sudo cp $hasviolet_json /tmp/hasVIOLET.json >/dev/null 2>&1
sudo cp $hasviolet_ssl_key /tmp/hasVIOLET.key >/dev/null 2>&1
sudo cp $hasviolet_ssl_crt /tmp/hasVIOLET.crt >/dev/null 2>&1
echo "-- Remove working directory"
sudo rm -rf $hasviolet_install >/dev/null 2>&1

echo " "
echo "- Clone Repository"
echo " "
git clone $hasviolet_github_repo

echo " "
echo "-- Restore JSON and SSL Cert/Key"
echo " "
sudo cp /tmp/hasVIOLET.json $hasviolet_json >/dev/null 2>&1
sudo cp /tmp/hasVIOLET.key $hasviolet_ssl_key >/dev/null 2>&1
sudo cp /tmp/hasVIOLET.crt $hasviolet_ssl_crt >/dev/null 2>&1

echo " "
echo "HASviolet Install Update complete"
echo " "
echo "  To run the apps, you must be in the $hasviolet_install directory and"
echo "  prefix the app name with ./<app-name>.for example: ./HASviolet_RX.py"
echo " "
echo "  Next step is to configure the call and SSID of this device by running"
echo " "
echo "            ./HASviolet_config.py"
echo " " 
echo "  To install the Websox server as a daemon run"
echo " "
echo "           ./HASviolet_websox.sh install"
echo " "
echo "- Enjoy!"
echo "  -- The HASviolet Team at HVDN "
echo " "
exit 0
