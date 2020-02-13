#!/bin/bash

###
### HVDN_HASVIOLET_INSTALL
###

##
##
## This script is part of the HASviolet project.
##
## Given a Raspbian Lite image, this script will install all the packegs, libraries, and github repo
## required to implement the HVDN Communicator.
##
## The HVDN Communicator hardware required includes Raspberry Pi Zero Wireles plus the
## Adafruit LoRa Radio Bonnet with OLED RFM95W @ 9145 MHz
##
## https://www.adafruit.com/product/4074
##

##
## VERSION
##
## 2019-09-13	Genesis of script
## 2019-09-14	Includes pyRF95 repo
## 2020-02-12   Permission error for MOTD, Changing working app path, Clean up script

##
## INIT VARIABLES 
##

# HVDN LocalRepo Home Directory
hvdn_localrepo=$HOME/hvdn-repo

# HAS Violet LocalRepo (GitHub clone)
hasviolet_localrepo=$HOME/hvdn-repo/hasviolet

# HAS Violet install path
hasviolet_install=$HOME/hvdn

# HAS Violet INI file
hasviolet_ini=$hasviolet_install/hvdn-comm.ini

# HASviolet GitHub Repo
hvdn_hasviolet_repo="https://github.com/hudsonvalleydigitalnetwork/hasviolet.git"


##
##  START 
##

echo " "
echo "HVDN HASviolet Install"
echo " "
echo "- Install Raspbian Packages"
echo " "

sudo apt-get install python3-pip
sudo apt-get install git
sudo apt-get install vim

echo " "
echo "- Install Python Libraries"
echo " "

sudo apt-get install python3-pil
sudo pip3 install aprs
sudo pip3 install aprslib
sudo pip3 install adafruit-circuitpython-rfm69
sudo pip3 install adafruit-circuitpython-rfm9x
sudo pip3 install adafruit-circuitpython-ssd1306
sudo pip3 install adafruit-circuitpython-framebuf

echo " "
echo "- Install HVDN Repo"
echo " "

cd $HOME
mkdir $hvdn_localrepo
mkdir $hasviolet_localrepo
mkdir $hasviolet_install
cd $hvdn_localrepo
git clone $hvdn_hasviolet_repo

echo " "
echo "- Create HVDN working directory"
echo " "

cp -R $hasviolet_localrepo/stable/* $hvdn_hasviolet_install

echo " "
echo "HAS Violet installation complete. All apps are in $hasviolet_install"
echo " "

exit 0
