#!/bin/bash

###
### HVDN_HASVIOLET_INSTALL
###

##
##
## This script is part of the HASviolet project.
##
## Given a Raspbian Lite image, this script will install all the required packages, libraries, and github repos
## required to implement the HVDN Communicator.
##
## The HVDN Communicator hardware requirments include
##
##        Raspberry Pi Zero Wireles
##        Adafruit LoRa Radio Bonnet with OLED RFM95W @ 9145 MHz
##
##        https://www.adafruit.com/product/4074
##

##
## VERSION
##
## 2019-09-13	Genesis of script
##

##
## INIT VARIABLES 
##

# HVDN LocalRepo Home Directory
hvdn_localrepo=$HOME/hvdn

# HVDN Communicator LocalRepo (GitHub clone)
hvdn_hasviolet_localrepo=$HOME/hvdn/hasviolet

# HVDN Communicator install path
hvdn_hasviolet_install=$HOME/hvdn-comm

# HVDN Communicator INI file
hvdn_hasviolet_ini=$hvdn_hasviolet_install/hvdn-comm.ini

# HVDN HASviolet GitHub Repo
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
sudo apt-get install nginx

echo " "
echo "- Install Python Libraries"
echo " "

#sudo pip3 install adafruit-circuitpython-rfm69
sudo pip3 install adafruit-circuitpython-rfm9x
sudo pip3 install adafruit-circuitpython-ssd1306
sudo pip3 install adafruit-circuitpython-framebuf
sudo pip3 install aprs
sudo pip3 install aprslib

echo " "
echo "- Create HVDN LocalRepo and HVDN-Comm directories"
echo " "

cd $HOME
mkdir $hvdn_localrepo
mkdir $hvdn_hasviolet_localrepo
mkdir $hvdn_hasviolet_install

echo " "
echo "- Clone HVDN Repos"
echo " "

cd $hvdn_localrepo
git clone $hvdn_hasviolet_repo

echo " "
echo "- Install HVDN-Comm"
echo " "

cp -R $hvdn_hasviolet_localrepo/stable/* $hvdn_hasviolet_install

# Generate hvdn-comm.ini file

gpio_rfm_cs=1
gpio_rfm_irq=22
node_address=1
freqmhz=911.25
txpwr=5

echo " "
echo "- Create hvdn-comm.ini file"
echo " "

echo " "
echo "What will be the node address for this device (1-254):"
read node_address

echo " "
echo "What TXpower level will you use (5-23):"
read txpwr

cat >$hvdn_hasviolet_ini <<EOL
[DEFAULT]
gpio_rfm_cs=${gpio_rfm_cs}
gpio_rfm_irq=${gpio_rfm_irq}
node_address=${node_address}
freqmhz=${freqmhz}
txpwr=${txpwr}
EOL

echo " "
echo "HVDN-Comm is installed in $hvdn_hasviolet_install"
echo " "

exit 0
