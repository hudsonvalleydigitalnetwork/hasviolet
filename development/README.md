# Development
  
All code in this folder is candidate for next release.

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
* Config file used by Duckhunt game

### HASvioletHID
* Library used by HASviolet apps that contains all HID Module related classes and methods

### HASvioletRF
* Library used by HASviolet apps that contains all RF Module related classes and methods


## Standalone applications

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
* Configuration tool to configure HASviolet.ini

### HASviolet-duckhunt-config.py
* Configuration tool to configure HASviolet-duckhunt.ini for Duckhunt game

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

## Proof of Concept Sensor Applications

* HASviolet-atmos.py
* HASviolet-gps.py
* HASviolet-distance.py


## Portable operations

HASviolet_install.sh installs a systemd service that runs on bootup that enables you to run
simple RX and TX actvities with the OLED and three HAT buttons. The program the service runs
is called HASviolet-handheld.py. 

### HASviolet.service
* Service files required by systemd. Installed by HASviolet-install.sh

### HASviolet-service.sh
 Start, stop, or remove the HASviolet service that starts HASviolet-handheld on bootup

  ```
  Usage: ./HASviolet-services.sh [ start | stop | remove ]
  ```

## XARPS eXtensible Amateur Radio Payload Specification (DRAFT)

