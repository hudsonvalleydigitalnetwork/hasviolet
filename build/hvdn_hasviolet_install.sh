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
hvdn_hasviolet_ini=$hvdn_hasviolet_install/"hvdn-comm.ini"

# HVDN Install Flag - Null file created when this script has completed successfuly.
hvdn_hasviolet_flag=$hvdn_hasviolet_install/"hvdn_flag_prep.txt";

# HVDN HASviolet GitHub Repo
hvdn_hasviolet_repo="https://github.com/hudsonvalleydigitalnetwork/hasviolet.git"

##
##  START 
##

echo "# Install Raspbian Packages"
echo " "

sudo apt-get install python3-pip
sudo apt-get install git
sudo apt-get install nginx

echo "# Install Python Libraries"
echo " "

#sudo pip3 install adafruit-circuitpython-rfm69
sudo pip3 install adafruit-circuitpython-rfm9x
sudo pip3 install adafruit-circuitpython-ssd1306
sudo pip3 install adafruit-circuitpython-framebuf
sudo pip3 install aprs
sudo pip3 install aprslib

echo "# Create HVDN LocalRepo and HVDN-Comm directories"
echo " "

cd $HOME
mkdir $hvdn_localrepo
mkdir $hvdn_hasviolet_localrepo
mkdir $hvdn_hasviolet_install

echo "# Clone HVDN Repos"
echo " "

cd $hvdn_localrepo
github clone $hvdn_hasviolet_repo

echo "# Install HVDN-Comm"
echo " "

if [ -f $hvdn_hasviolet_ini ]; then
    echo "#Moving (Move any existing install to .old directory and copy INI to new install)"
    echo " "


    mv $hvdn_hasviolet_install $hvdn_hasviolet_install/old
    cp $hvdn_hasviolet_localrepo/stable $hvdn_hasviolet_install
    cp $hvdn_hasviolet_install/old/hvdn-comm.ini $hvdn_hasviolet_install
    echo "# HVDN-Comm is installed using your existing hvdn-comm.ini file."
    echo " "
    exit 1
fi

cp $hvdn_hasviolet_localrepo/* $hvdn_hasviolet_install

# Generate hvdn-comm.ini file

gpio_rfm_cs=1
gpio_rfm_irq=22
node_address=1
freqmhz=911.25
txpwr=5

echo "# Create hvdn-comm.ini file"
echo " "

echo " "
echo "What will be the node address for this device (1-254):"
read node_address

echo " "
echo "What TXpower level will you use (5-23):"
read txpwr

cat >$hvdn_hasviolet_ini <<EOL
[DEFAULT]
gpio_rfm_cs=$1
gpio_rfm_irq=${gpio_rfm_irq}
node_address=${node_address}
freqmhz=${freqmhz}
txpwr=${txpwr}
EOL

echo " "
echo "Following hvdn-comm.ini has been generated:"
echo " "

cat $hvdn_hasviolet_ini

echo "# HVDN-Comm is installed."
echo " "

exit 0
