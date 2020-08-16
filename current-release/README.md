# Workspace
  
All code in this folder is under development.

## Dependencies

### font5x8.bin
* Font file for the Adafruit OLED display

### hvdn-logo.xbm
* Banner image displayed on 128x32 OLED during startup. Substitute your own if you wish!

### rf95.py
* RFM95 library
* Sourced from https://github.com/ladecadence/pyRF95

### sx1262.py
* sx1262 library
* Sourced from https://github.com/ehong-tl/micropySX126X

### HASviolet.ini
* Config file used by HASviolet apps

### HASvioletHID
* Library used by HASviolet apps that contains all HID Module related classes and methods

### HASvioletRF
* Library used by HASviolet apps that contains all RF Module related classes and methods


## Core Applications

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
  HASviolet.ini config tool

### HASviolet-handheld.py
  Run as handheld device. All HID via HAT.

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
### HASviolet.service
  Systemd service file for HASviolet-handheld.py to run on startup

### HASviolet-service.sh
  Scrip to to start/stop/remove HASviolet.service

## Sensor Applications

### HASviolet-atmos.py
  Test with Sparkfun Atmospheric Sensor (BME280)

### HASviolet-distance.py
  Test with Sparkfun Distance Sensor Breakout - 4 Meter VL53L1X

### HASviolet-gps.py
  Test with GPS/GLONASS (USB)

### HASviolet-sensors.py
  Test with Atmospheric Sensor, Distance Sensor and GPS/GLONASS (USB)  