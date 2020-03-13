#!/bin/bash

###
### HASVIOLET_UPDATE
###

##
##
## This script is part of the HASviolet project.
##
## Given previous HASviolet build, update only deltas to latest release
##
## The HASviolet hardware required includes Raspberry Pi Zero Wireless plus the
## Adafruit LoRa Radio Bonnet with OLED RFM95W @ 915 MHz
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
echo "HASviolet Update"
echo " "
#echo "- Install Raspbian Packages"
#echo " "
#
#sudo apt-get -y install python3-pip
#sudo apt-get -y install git
#sudo apt-get -y install vim
#
#echo " "
#echo "- Install Python Libraries"
#echo " "
#
#sudo apt-get -y install python3-pil
#sudo pip3 install aprs
#sudo pip3 install aprslib
#sudo pip3 install adafruit-circuitpython-rfm69
#sudo pip3 install adafruit-circuitpython-rfm9x
#sudo pip3 install adafruit-circuitpython-ssd1306
#sudo pip3 install adafruit-circuitpython-framebuf

echo " "
echo "- Clone HASviolet Repository"
echo " "

mkdir $hvdn_localrepo
cd $hvdn_localrepo
git pull $hasviolet_github_repo

echo " "
echo "- Backup HASviolet.ini file"
echo " "

cd $hasviolet_install
mv HASviolet.ini HASviolet.ini.$(date +"%Y%m%d")

echo " "
echo "- Update HASviolet working directory"
echo " "

cp -R $hasviolet_localrepo/stable/* $hasviolet_install
rm HASviolet.ini

echo " "
echo "- Restore HASviolet.ini file"
echo " "

mv HASviolet.ini.$(date +"%Y%m%d") HASviolet.ini

echo " "
echo "HASviolet Update complete."
echo " "
echo "- The HASviolet repo has been updated in $hasviolet_localrepo"
echo "- The working directory $hasviolet_install has been updated
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