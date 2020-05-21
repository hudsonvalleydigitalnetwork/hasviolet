#!/bin/bash

###
### HASviolet-install
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
## INIT VARIABLES 
##

# HVDN LocalRepo Home Directory
hvdn_localrepo=$HOME/HVDN-repo

# HASviolet LocalRepo (GitHub clone)
hasviolet_localrepo=$HOME/HVDN-repo/hasviolet

# HASviolet Working directorydr@mBUI3
hasviolet_install=$HOME/HASviolet

# HASviolet INI file
hasviolet_ini=$hasviolet_install/HASviolet.ini

# HASviolet Duckhunt INI file
hasvioletduckhunt_ini=$hasviolet_install/HASviolet-duckhunt.ini

# HASviolet GitHub Repo
hasviolet_github_repo="https://github.com/hudsonvalleydigitalnetwork/hasviolet.git"

# HASviolet Private Daily Dev Repo
# devviolet_github_repo="https://github.com/joecupano/hasty-banana.git"

##
##  START 
##


if [ ${args[1]} = "refresh" ];then
    echo " "
    echo "HASviolet Refresh"
    echo " "
    cp $hasviolet_ini ~/hasviolet.ini.bk1
    cp $hasvioletduckhunt_ini ~/hasviolet-duckhunt.ini.bk1
else
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
    sudo pip3 install urwid

#
# Ensure this is HASviolet clean
#

sudo rm -rf $hvdn_localrepo >/dev/null 2>&1
sudo rm -rf $hasviolet_install >/dev/null 2>&1

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
cp -R $hasviolet_localrepo/stable/* $hasviolet_install

if [ -f ~/HASviolet.ini.bk1 ]; then
    cp ~/HASviolet.ini.bk1 $hasviolet_ini >/dev/null 2>&1
    cp ~/HASviolet-duckhunt.ini.bk1 $hasvioletduckhunt_ini >/dev/null 2>&1
fi

echo " "
echo " Installing HASviolet Service (systemd)"
echo " "

if [ -f /lib/systemd/system/HASviolet.service ]; then
    sudo systemctl stop HASviolet.service
    sudo systemctl disable HASviolet.service
    sudo rm -rf /lib/systemd/system/HASviolet.service
fi

echo " "
echo "- By default HASviolet is configured to boot ready for portable operation"
echo " "
echo "- In a few seconds you will see the HVDN logo on the OLED and then the MAIN MENU."
echo "- To disable portable operation, from the MAIN MENU select OPTIONS then QUIT."
echo "- To disable permanently you need to SSH into HASviolet and run the following command"
echo " "
echo "           ./HASviolet-service.sh kill"
echo " "

sleep 3

sudo cp $hasviolet_install/HASviolet.service /lib/systemd/system/HASviolet.service
sudo chown root:root /lib/systemd/system/HASviolet.service
sudo chmod 644 /lib/systemd/system/HASviolet.service
sudo systemctl daemon-reload
sudo systemctl enable HASviolet.service
sudo systemctl start HASviolet.service
sudo sync

echo " "
echo "- The repo has been cloned to $hasviolet_localrepo"
echo "- A working directory with all the apps is installed in $hasviolet_install"
echo " "
echo "- To run the apps, you must be in the $hasviolet_install directory and"
echo "- prefix the app name with ./<app-name>.for example:       ./HASviolet-rx.py"
echo " "
echo "- Enjoy! -- The HASviolet Team at HVDN "
echo " "
echo " "
exit 0
