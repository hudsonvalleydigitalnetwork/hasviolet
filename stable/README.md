# HAS Violet

## Stable

Project HAS Violet, brought to you by HVDN, the letter Q and numbers 8, 4 and 5. 
All code in this directory has been tested as functional and stable.

### font5x8.bin
* Font file for the Adafruit OLED display

### hvdn-comm.ini
* Config file used by hvdncomm apps

### hvdncomm-lora-broadcast_rf95.py
* Sends message to LoRa broadcast address (255)
* Usage: ./hvdncomm-lora-broadcast_ada.py  -c COUNT -m MESSAGE
* COUNT is number of times to repeat, MESSAGE is message to send in double quotes
* Uses pyRF95 library (rf95.py)

### hvdncomm-lora-chat.py
* Half-duplex LoRa messaging app
* Usage: ./hvdncomm-lora-chat
* Starts and loops in Listening Mode
* CTRL-Z to send a message, CTRL-C to exit program
* When in send mode
  * Recipient is node id (255 = broadcast address)
  * Message is whatever message followed by enter
  * Message is sent, return to listening mode

### hvdncomm-lora-message_rf95.py
* Sends message to another LoRa station
* Usage: ./hvdncomm-lora-message_ada.py -d DESTINATION -m MESSAGE
* DESTINATION is node address of destination (1-255), MESSAGE is message to send in double quotes
* Uses pyRF95 library (rf95.py)

### hvdncomm-lora-rx_rf95.py
* Listens for messages from other LoRa stations
* Usage: ./hvdncomm-lora-rx_rf95.py
* Uses pyRF95 library (rf95.py)

### rf95.py
* RFM95 library used by hvdncom apps ending in rf95.py
* Sourced from https://github.com/ladecadence/pyRF95


