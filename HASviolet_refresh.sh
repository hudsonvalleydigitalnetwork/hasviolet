#!/bin/bash

###
### HASviolet-refresh
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

#hasviolet_install=$HOME/DEVviolet
##
## INIT VARIABLES 
##

# HVDN LocalRepo Home Directory
hvdn_localrepo=$HOME/HVDN-repo

# LocalRepos (GitHub clone)
hasviolet_localrepo=$HOME/HVDN-repo/hasviolet

# Working directories
hasviolet_install=$HOME/HASviolet

# HASviolet INI file
hasviolet_ini=$hasviolet_install/HASviolet.ini

# HASviolet Duckhunt INI file
hasvioletduckhunt_ini=$hasviolet_install/HASviolet-duckhunt.ini

# GitHub Repos
hasviolet_github_repo="https://github.com/hudsonvalleydigitalnetwork/hasviolet.git"

##
##  START 
##


echo " "
echo "HASviolet Refresh"
echo " "

#
# Ensure this is DEVviolet clean
#
sudo cp $hasviolet_ini /tmp/$hasviolet_ini >/dev/null 2>&1
sudo cp $hasvioletduckhunt_ini /tmp/$hasvioletduckhunt_ini >/dev/null 2>&1
sudo rm -rf $hasviolet_localrepo >/dev/null 2>&1
sudo rm -rf $hasviolet_install >/dev/null 2>&1

echo " "
echo "- Suspend HASviolet (systemd) service"
echo " "
sudo systemctl stop HASviolet.service

echo " "
echo "- Clone HASviolet Repository"
echo " "

cd $hvdn_localrepo
git clone $hasviolet_github_repo

echo " "
echo "- Create HASviolet working directory"
echo " "

mkdir $hasviolet_install
cp -R $hasviolet_localrepo/current-release/* $hasviolet_install

echo " "
echo "- Resume HASviolet (systemd) service"
echo " "
sudo systemctl start HASviolet.service

sudo sync

echo " "
echo "HASviolet Install complete"
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