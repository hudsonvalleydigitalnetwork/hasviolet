# HAS Violet

## Stable

Project HAS Violet, brought to you by HVDN, the letter Q and numbers 8, 4 and 5. 
All code in this directory has been tested as functional and stable.

### font5x8.bin
* Font file for the Adafruit OLED display

### hvdn-comm.ini
* Config file used by hvdncomm apps

### hvdn_lora-beacon.py
  Beacon a LoRa message

  ```
  Usage: hvdn_lora-beacon.py -c COUNT -t DELAY "message"

  OPTIONS
           -c Number of times to repeat MESSAGE
           -t NUmber of seconds before repeat MESSAGE
           MESSAGE is message to be send within double quotes
  ```

### hvdn_lora-chat.py
  Half-duplex LoRa messaging app
  
  ```
  Usage: ./hvdn_lora-chat [-r] [-s]

  OPTIONS
          -r Raw data instead of ASCII
          -s Show RSSI
  ```
  * Starts and loops in Listening Mode
  * CTRL-Z to send a message, CTRL-C to exit program
  * When in send mode
    * Recipient is node id (255 = broadcast address)
    * Message is whatever message followed by enter
    * Message is sent, return to listening mode

### hvdn_lora-tx.py
  Send a LoRa message

  ```
  Usage: hvdn_lora-tx.py -d DESTINATION "message"

  OPTIONS
           -d Destination ID
           MESSAGE is message to be send within double quotes
  ```

### hvdn_lora-rx.py
 Listens for messages from other LoRa stations

  ```
  Usage: ./hvdn_lora-rx.py -r -s

  OPTIONS
	  -h, --help      show this help message and exit
	  -r, --raw_data  Receive raw data
	  -s, --signal    Signal Strength
  ```
  
### rf95.py
* RFM95 library used by hvdncom apps ending in rf95.py
* Sourced from https://github.com/ladecadence/pyRF95

