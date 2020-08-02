# Stable
  
All core application and supporting code in this folder is considered stable.

## Required Dependencies

Libraries and other files required by all HASviolet applications
ans libraries

### font5x8.bin
* Font file for the Adafruit OLED display

### hvdn-logo.xbm
* Banner image displayed on 128x32 OLED during startup. Substitute your own if you wish!

### rf95.py
* RFM95 library
* Sourced from https://github.com/ladecadence/pyRF95

### HASviolet.ini
* Config file used by HASviolet apps

### HASviolet-duckhunt.ini
* Config file used by DuckHunt

### HASvioletHID
* Library used by HASviolet apps that contains all HID Module related classes and methods

### HASvioletRF
* Library used by HASviolet apps that contains all RF Module related classes and methods

### HASviolet.service
* Systemd service file to start HASviolet-handheld.py


## HASviolet Core Applications

Standalone applications

### HASviolet-beacon.py
  Beacon a LoRa message

  ```
  Usage: HASviolet-beacon.py -c COUNT -t DELAY "message"

  OPTIONS
           -c Number of times to repeat MESSAGE
           -t NUmber of seconds before repeat MESSAGE
           MESSAGE is message to be send within double quotes
  ```

### HASviolet-chat.py
  Interactive half-duplex chat program

### HASviolet-config.py
  Setup HASviolet device. Generates HASviolet.ini

### HASviolet-duckhunt-config.py
  Setup DuckHunt. Generates HASviolet-duckhunt.ini

### HASviolet-handheld.py
  Background app started by systemd to use HASviolet with  HAT buttons and OLED

### HASviolet-service.sh
  Disable HASviolet-handheld from ssh session

### HASviolet-rx.py
 Listens for messages from other LoRa stations

  ```
  Usage: ./HASviolet-rx.py -r -s

  OPTIONS
	  -h, --help      show this help message and exit
	  -r, --raw_data  Receive raw data
	  -s, --signal    Signal Strength
  ```

### HASviolet-tx.py
  Send a LoRa message

  ```
  Usage: HASviolet-tx.py -d DESTINATION -m "message"

  OPTIONS
           -d Destination (if omitted BEACON-99 is default)
           -m message to be sent within double quotes
  ```

## HASviolet Handheld Use
With the OLED and three buttons on the bonnet, core functionality is available to you
on startup.

Systemd runs HASviolet.service on startup
HASviolet.service starts HASviolet-handheld.py

No other RF transmissions can occur when running as handheld. To disable you
can select EXIT from the OLED menu or SSH into the Pi and run

  HASviolet-service.sh stop

If you would like to remove from startup then

  HASviolet-service.sh remove


## Sample Applications

This includes applications used with USB and i2c based sensors

* HASviolet-atmos.py
* HASviolet-distance.py
* HASviolet-gps.py
* HASviolet-sensors.py