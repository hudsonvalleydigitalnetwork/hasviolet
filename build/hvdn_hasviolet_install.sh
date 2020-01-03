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
##

##
## INIT VARIABLES 
##

# HVDN LocalRepo Home Directory
hvdn_localrepo=$HOME/hvdn-repo

# HVDN Communicator LocalRepo (GitHub clone)
hvdn_hasviolet_localrepo=$HOME/hvdn-repo/hasviolet

# HVDN Communicator install path
hvdn_hasviolet_install=$HOME/hvdn-comm

# HVDN Communicator INI file
hvdn_hasviolet_ini=$hvdn_hasviolet_install/hvdn-comm.ini

# HVDN HASviolet GitHub Repo
hvdn_hasviolet_repo="https://github.com/hudsonvalleydigitalnetwork/hasviolet.git"

# pyRF95 Library repo
pyrf95_repo="https://github.com/ladecadence/pyRF95"

# pyRF95 LocalRepo (GitHub clone)
pyrf95_localrepo=$hvdn_localrepo/pyRF95

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

echo " "
echo "- Install Python Libraries"
echo " "

sudo apt-get install python3-pil
sudo pip3 install aprs
sudo pip3 install aprslib
#sudo pip3 install adafruit-circuitpython-rfm69
#sudo pip3 install adafruit-circuitpython-rfm9x
sudo pip3 install adafruit-circuitpython-ssd1306
sudo pip3 install adafruit-circuitpython-framebuf

echo " "
echo "- Create HVDN LocalRepo and HVDN-Comm directories"
echo " "

cd $HOME
mkdir $hvdn_localrepo
mkdir $hvdn_hasviolet_localrepo
mkdir $hvdn_hasviolet_install

echo " "
echo "- Clone HVDN Repo"
echo " "

cd $hvdn_localrepo
git clone $hvdn_hasviolet_repo

echo " "
echo "- Clone pyRF95 Repo"
echo " "

git clone $pyrf95_repo

echo " "
echo "- Install HVDN-Comm"
echo " "

cp -R $hvdn_hasviolet_localrepo/stable/* $hvdn_hasviolet_install

#Customize Environment
sudo cat >/etc/motd <<EOL
 _          _
| |___ ____| |_ _
| ' \ V / _` | ' \
|_||_\_/\__,_|_||_|
-------------------
Alpha version 20200103

EOL


echo " "
echo "HVDN-Comm is installed in $hvdn_hasviolet_install"
echo " "

exit 0
