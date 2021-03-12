#!/bin/bash

###
### HASviolet_install_fresh
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
## - Flattened footprint dropping repo folder
## - Added install of pyLoraRFM9x library for interrupt driven LoRa
## - Generate SSLv3/TLS cert/key for (Tornado) websox server and future use
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
echo "HASviolet Install Fresh"
echo " "
echo "- Install Raspbian Packages"
echo " "
sudo apt-get -y install git
sudo apt-get -y install python3-pip
sudo apt-get -y install python3-pil
sudo apt-get -y install libatlas-base-dev        # Numpy Dependency
echo " "
echo "- Install Python Libraries"
echo " "
sudo pip3 install tornado
sudo pip3 install RPI.GPIO
sudo pip3 install spidev
sudo pip3 install pynmea2
sudo pip3 install python-metar
sudo pip3 install adafruit-circuitpython-ssd1306
sudo pip3 install adafruit-circuitpython-framebuf
sudo pip3 install adafruit-circuitpython-rfm9x
sudo pip3 install numpy                          # pyLoraRFM9x dependency
sudo pip3 install pyLoraRFM9x
sudo pip3 install sparkfun-qwiic
sudo pip3 install sparkfun-qwiic-bme280
sudo pip3 install sparkfun-qwiic-vl53l1x

cd $HOME

echo " "
echo "- Clone Repository"
echo " "
git clone $hasviolet_github_repo

echo " "
echo "- Generating self-signed SSL certificate --  /C=US/ST=New York/L=Hudson Valley/O=Hudson Valley Digital Network/OU=HASviolet/CN=hvdn.org"
echo " "
sudo openssl req -x509 -nodes -days 1095 -newkey rsa:2048 -subj "/C=US/ST=New York/L=Hudson Valley/O=Hudson Valley Digital Network/OU=HASviolet/CN=hvdn.org" -keyout $hasviolet_install/hasviolet_api.key -out $hasviolet_install/hasviolet_api.crt
sudo chown pi:pi $hasviolet_install/hasviolet_api.key >/dev/null 2>&1
sudo chown pi:pi $hasviolet_install/hasviolet_api.crt >/dev/null 2>&1

echo " "
echo "HASviolet Install Fresh complete"
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
