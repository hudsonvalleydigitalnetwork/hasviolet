# HAS Violet

## RPi Development

All code in this directory remains experimental. Use at your own risk.

### font5x8.bin
* Font file for the Adafruit OLED display

### hvdn-comm.ini
* Config file used by hvdncomm apps
  
### hvdn_lora-chat.py
  Half-duplex LoRa messaging app
  
  ```
  Usage: ./hvdn_lora-chat [-r] [-s]

  OPTIONS
	  -h, --help      show this help message and exit
	  -r, --raw_data  Receive raw data
	  -s, --signal    Signal Strength
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

