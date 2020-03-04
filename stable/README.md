# HASviolet

## Stable

Project HASviolet, brought to you by HVDN, the letter Q and numbers 8, 4 and 5. 
All code in this directory has been tested as functional and stable.

### font5x8.bin
* Font file for the Adafruit OLED display

### HASviolet.ini
* Config file used by HASviolet apps

### HASviolet-beacon.py
  Beacon a LoRa message

  ```
  Usage: HASviolet-beacon.py -c COUNT -t DELAY "message"

  OPTIONS
           -c Number of times to repeat MESSAGE
           -t NUmber of seconds before repeat MESSAGE
           MESSAGE is message to be send within double quotes
  ```

### HASviolet-tx.py
  Send a LoRa message

  ```
  Usage: HASviolet-tx.py -d DESTINATION "message"

  OPTIONS
           -d Destination ID
           MESSAGE is message to be send within double quotes
  ```

### HASviolet-rx.py
 Listens for messages from other LoRa stations

  ```
  Usage: ./HASviolet-rx.py -r -s

  OPTIONS
	  -h, --help      show this help message and exit
	  -r, --raw_data  Receive raw data
	  -s, --signal    Signal Strength
  ```
  
### rf95.py
* RFM95 library used by hvdncom apps ending in rf95.py
* Sourced from https://github.com/ladecadence/pyRF95

