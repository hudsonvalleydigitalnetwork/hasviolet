#!/bin/bash

###
###  HASviolet.sh
###
### 

###
###  REVISION: 20220601-0200
### 

###
###  Usage:    HASviolet [ACTION] [TARGET]
###
###        ACTION  
###                 install   install current release
###                 config    configure HASviolet
###                 remove    remove installed TARGET
###                 purge     remove installed TARGET and purge configs
###                 update    check to see if new TARGET available
###                 upgrade   upgrade TARGET to latest release
###                 shell     provide SIGpi env variables around a TARGET
###
###        TARGET
###                 A HASviolet package or script
###


###
###
### HASviolet has been designed for the following hardware: 
###    Raspberry Pi Zero Wireless
###    Adafruit LoRa Radio Bonnet with OLED RFM95W @ 915 MHz https://www.adafruit.com/product/4074
###    Sensors connected via i2c
###    GPS USB modules
###
### Generic Python Libraries for i2c and SPI are installed as well as the following:
###
### Adafruit RFM9X Library
### https://github.com/adafruit/adafruit-circuitpython-rfm9x
###
### Adafruit Monochrome OLEDs based on SSD1306 drivers
### https://github.com/adafruit/Adafruit_SSD1306
###
### Adafruit_CircuitPython_framebuf
### https://github.com/adafruit/Adafruit_CircuitPython_framebuf
###
### Sparkfun Qwiic Python Package
### https://github.com/sparkfun/Qwiic_Py
###
### pyRF95
### https://github.com/ladecadence/pyRF95
###
###
###

##
## INIT VARIABLES AND DIRECTORIES
##

# HASviolet Directory tree
HASVIOLET_REPO="https://github.com/hudsonvalleydigitalnetwork/hasviolet.git"
HASVIOLET_HOME=$HOME/HASviolet
HASVIOLET_TEMPLATES=$HASVIOLET_HOME/templates
HASVIOLET_TEMPLATES_ETC=$HASVIOLET_TEMPLATES/etc
HASVIOLET_TEMPLATES_SRV=$HASVIOLET_TEMPLATES/server
HASVIOLET_CFGDIR=$HOME/.config/HASviolet
HASVIOLET_SRVDIR=$HASVIOLET_CFGDIR/server
HASVIOLET_ETC=$HASVIOLET_CFGDIR/etc
HASVIOLET_CONFIG=$HASVIOLET_ETC/HASviolet.json
HASVIOLET_SSL_KEY=$HASVIOLET_ETC/HASviolet.key
HASVIOLET_SSL_CRT=$HASVIOLET_ETC/HASviolet.crt
HASVIOLET_BANNER_COLOR="\e[0;104m\e[K"   # blue
HASVIOLET_BANNER_RESET="\e[0m"

# HASviolet Install Support files

# Detect architecture (x86, x86_64, aarch64, ARMv8, ARMv7)
HASVIOLET_HWARCH=`lscpu|grep Architecture|awk '{print $2}'`
# Detect Operating system (Raspberry Pi OS)
HASVIOLET_OSNAME=`cat /etc/os-release|grep "PRETTY_NAME"|awk -F'"' '{print $2}'`
# Is Platform good for install- true or false - we start with false
HASVIOLET_CERTIFIED="false"


###
### FUNCTIONS
###

hasviolet_update(){
    echo -e "${HASVIOLET_BANNER_COLOR}"
    echo -e "${HASVIOLET_BANNER_COLOR} ##  ERROR: Unkown action or package"
    echo -e "${HASVIOLET_BANNER_RESET}"
}

hasviolet_upgrade(){
    echo -e "${HASVIOLET_BANNER_COLOR}"
    echo -e "${HASVIOLET_BANNER_COLOR} ##  ERROR: Unkown action or package"
    echo -e "${HASVIOLET_BANNER_RESET}"
}

hasviolet_install(){
    echo " "
    echo "HASviolet FRESH Install"
    echo " "
    echo "- Install Dependencoes"
    echo " "
    sudo apt-get -y install git
    sudo apt-get -y install python3-pip
    sudo apt-get -y install python3-pil
    sudo apt-get -y install libatlas-base-dev        # Numpy Dependency
    echo " "
    echo "- Install Libraries"
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
    echo " "
    echo "- Create Directories"
    echo " "
    cd $HASVIOLET_HOME
    mkdir $HASVIOLET_CFGDIR
    mkdir $HASVIOLET_SRVDIR
    mkdir $HASVIOLET_ETC
    echo " "
    echo "- Copy config templates into $HASVIOLET_ETC"
    echo " "
    sudo cp $HASVIOLET_TEMPLATES_ETC/* $HASVIOLET_ETC
    echo " "
    echo "- Copy server templates into $HASVIOLET_SRVDIR"
    echo " "
    sudo cp $HASVIOLET_TEMPLATES_SRV/* $HASVIOLET_SRVDIR
    echo " "
    echo "- Generating self-signed SSL certificate --  /C=US/ST=New York/L=Hudson Valley/O=Hudson Valley Digital Network/OU=HASviolet/CN=hvdn.org"
    echo " "
    sudo openssl req -x509 -nodes -days 1095 -newkey rsa:2048 -subj "/C=US/ST=New York/L=Hudson Valley/O=Hudson Valley Digital Network/OU=HASviolet/CN=hvdn.org" -keyout $HASVIOLET_HOME/hasviolet_api.key -out $HASVIOLET_HOME/hasviolet_api.crt
    sudo chown pi:pi $HASVIOLET_ETC/hasviolet_api.key >/dev/null 2>&1
    sudo chown pi:pi $HASVIOLET_ETC/hasviolet_api.crt >/dev/null 2>&1

    echo " "
    echo "HASviolet FRESH Install complete"
    echo " "
}

###
###  MAIN
###

ACTION=$1
SPACKAGE=$2
SPKGSCRIPT="pkg_$2"
SCFGSCRIPT="cfg_$2"

case "$1" in 
    remove )
        echo -e "${HASVIOLET_BANNER_COLOR}"
        echo -e "${HASVIOLET_BANNER_COLOR} ##  Remove HASviolet"
        echo -e "${HASVIOLET_BANNER_RESET}"
        cd ~
        rm -rf $HASVIOLET_HOME
        ;;
    purge )
        echo -e "${HASVIOLET_BANNER_COLOR}"
        echo -e "${HASVIOLET_BANNER_COLOR} ##  Purge HASviolet"
        echo -e "${HASVIOLET_BANNER_RESET}"
        cd ~
        rm -rf $HASVIOLET_HOME
        rm -rf $HASVIOLET_CFGDIR
        ;;
    install )
        hasviolet_install
        ;;
    config )
        source $HASVIOLET_HOME/hasviolet_config.py
        ;;
    update )
        hasviolet_update
        ;;
    upgrade)
        hasviolet_upgrade
        ;;
    shell )
        source $2
        ;;
    * )
        echo -e "${HASVIOLET_BANNER_COLOR}"
        echo -e "${HASVIOLET_BANNER_COLOR} ##  ERROR: Unkown action or package"
        echo -e "${HASVIOLET_BANNER_RESET}"
        ;;
esac

exit 0
