# RC (Release Candidate)
  
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

### HASvioletHID
* Library used by HASviolet apps that contains all HID Module related classes and methods

### HASvioletRF
* Library used by HASviolet apps that contains all RF Module related classes and methods


## HASviolet Applications

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

### HASviolet-handheld.py
  Currently only a menu demo of Hanheld feature

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
