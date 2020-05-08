#!/bin/bash

###
### HASVIOLET-DINSTALL
###

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
## Adafruit LoRa Radio Bonnet with OLED RFM95W @ 9145 MHz
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
## INIT VARIABLES 
##

# HVDN LocalRepo Home Directory
hvdn_localrepo=$HOME/HVDN-repo

# HASviolet LocalRepo (GitHub clone)
#hasviolet_localrepo=$HOME/HVDN-repo/hasviolet
hasviolet_localrepo=$HOME/HVDN-repo/hasty-banana

# HASviolet Working directorydr@mBUI3
hasviolet_install=$HOME/HASviolet

# HASviolet Dev Directoy
hasviolet_dev=$HOME/DEVviolet

# HASviolet INI file
hasviolet_ini=$hasviolet_install/HASviolet.ini

# HASviolet update
hasviolet_update=0

# HASviolet GitHub Repo
#hasviolet_github_repo="https://github.com/hudsonvalleydigitalnetwork/hasviolet.git"
hasviolet_github_repo="https://github.com/joecupano/hasty-banana.git"

##
##  START 
##

echo " "
echo "HASviolet Install"
echo " "
echo "- Install Raspbian Packages"
echo " "

sudo apt-get -y install git
sudo apt-get -y install python3-pip
sudo apt-get -y install python3-pil

echo " "
echo "- Install Python Libraries"
echo " "

sudo pip3 install spidev
sudo pip3 install pynmea2
sudo pip3 install sparkfun-qwiic
sudo pip3 install adafruit-circuitpython-ssd1306
sudo pip3 install adafruit-circuitpython-framebuf

if [ -f $hasviolet_ini ]; then
    cp $hasviolet_ini ~/HASviolet.ini.bk1
fi

#
# Ensure this is HASviolet clean
#

sudo rm -rf $hvdn_localrepo >/dev/null 2>&1
sudo rm -rf $hasviolet_install >/dev/null 2>&1
sudo rm -rf $hasviolet_dev >/dev/null 2>&1

echo " "
echo "- Clone HASviolet Repository"
echo " "

mkdir $hvdn_localrepo
cd $hvdn_localrepo
git clone $hasviolet_github_repo

echo " "
echo "- Create HASviolet working directory"
echo " "
mkdir $hasviolet_install
cp -R $hasviolet_localrepo/released/* $hasviolet_install
if [ -f $hasviolet_ini ]; then
    cp ~/HASviolet.ini.bk1 $hasviolet_ini >/dev/null 2>&1
fi




if [ $1 == "dev"] ; then
    echo " "
    echo "- Creating DEVviolet working directory"
    echo " "
    sudo rm -rf $hasviolet_dev
    mkdir $hasviolet_dev
    cp $hasviolet_localrepo/active/* $hasviolet_dev
    cp $hasviolet_localrepo/RC2/* $hasviolet_dev
    cp $hasviolet_install/rf95.py $hasviolet_dev
    cp $hasviolet_install/font5x8.bin $hasviolet_dev
    cp $hasviolet_install/HASviolet.ini $hasviolet_dev
fi

echo " "
echo "HASviolet installation complete."
echo " "
echo "- The HASviolet repo has been cloned to $hasviolet_localrepo"
echo "- A working directory with released apps is installed in $hasviolet_install"
if [ $1 == "dev"] ; then
    echo "- A working DEV directory with released plus dev apps is installed in $hasviolet_dev"
fi
echo " "
echo "To run the apps, you must be in the $hasviolet_install directory and"
echo "prefix the app name with ./<app-name>"
echo " "
echo "for example:       ./HASviolet-rx.py"
echo " "

cd $hasviolet_install

echo " "
echo "Enjoy! -- The HASviolet Team at HVDN "
echo " "
echo " "

sleep 3
exit 0
