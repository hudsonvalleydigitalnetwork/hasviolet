#!/bin/bash

###
### HASVIOLET_INSTALL
###

##
##
## This script is part of the HASviolet project.
##
## Given a Raspbian Lite image, this script will install all the packegs, libraries, and github repo
## required to implement the HVDN Communicator.
##
## The HASviolet hardware required includes Raspberry Pi Zero Wireles plus the
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
## 2020-03-03   Rebrand
## 2020-03-07   Missing git clone command -- duh
## 2020-03-11   Missing mkdir command

##
## INIT VARIABLES 
##

# HVDN LocalRepo Home Directory
hvdn_localrepo=$HOME/HVDN-repo

# HASviolet LocalRepo (GitHub clone)
hasviolet_localrepo=$HOME/HVDN-repo/hasviolet

# HASviolet install path
hasviolet_install=$HOME/HASviolet

# HASviolet INI file
hasviolet_ini=$hasviolet_install/HASviolet.ini

# HASviolet GitHub Repo
hasviolet_github_repo="https://github.com/hudsonvalleydigitalnetwork/hasviolet.git"


##
##  START 
##

echo " "
echo "HASviolet Install"
echo " "
echo "- Install Raspbian Packages"
echo " "

sudo apt-get -y install python3-pip
sudo apt-get -y install git
sudo apt-get -y install vim

echo " "
echo "- Install Python Libraries"
echo " "

sudo apt-get -y install python3-pil
sudo pip3 install aprs
sudo pip3 install aprslib
sudo pip3 install adafruit-circuitpython-rfm69
sudo pip3 install adafruit-circuitpython-rfm9x
sudo pip3 install adafruit-circuitpython-ssd1306
sudo pip3 install adafruit-circuitpython-framebuf

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

echo " "
echo "HASviolet installation complete."
echo "All apps are in $hasviolet_install"
echo " "
echo "To run the apps, you must be in the $hasviolet_install directory and"
echo "prefix the app name with ./<app-name>"

cd $hasviolet_install
sleep 3
exit 0