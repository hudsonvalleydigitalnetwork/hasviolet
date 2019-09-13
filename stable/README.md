# hasviolet
Project HAS Violet, brought to you by HVDN, the letter Q and numbers 8, 4 and 5. 

STABLE Release

All code in this directory has been tested as functional and stable.

font5x8.bin
- Font file for the Adafruit OLED display

hvdn-comm.ini
- Config file used by hvdncomm apps

hvdncomm-lora-broadcast_ada.py
- Sends message to LoRa broadcast address (255)
- Usage: ./hvdncomm-lora-broadcast_ada.py %1 %2
- %1 is number of times to repeat, %2 is message in double quotes
- Uses Adafruit CircuitPython Library (adafruit_rfm9X)

hvdncomm-lora-broadcast_rf95.py
- Sends message to LoRa broadcast address (255)
- Usage: ./hvdncomm-lora-broadcast_ada.py %1 %2
- %1 is number of times to repeat, %2 is message in double quotes
- Uses pyRF95 library (rf95.py)

hvdncomm-lora-message_ada.py
- Sends message to another LoRa station
- Usage: ./hvdncomm-lora-message_ada.py %1 %2
- %1 is node address of destination (1-255), %2 is message in double quotes
- Uses Adafruit CircuitPython Library (adafruit_rfm9X)

hvdncomm-lora-message_rf95.py
- Sends message to another LoRa station
- Usage: ./hvdncomm-lora-message_rf95.py %1 %2
- %1 is node address of destination (1-255), %2 is message in double quotes
- Uses pyRF95 library (rf95.py)

hvdncomm-lora-rx_ada.py
- Listens for messages from other LoRa stations
- Usage: ./hvdncomm-lora-rx_ada.py
- Uses Adafruit CircuitPython Library (adafruit_rfm9X)

hvdncomm-lora-rx_rf95.py
- Listens for messages from other LoRa stations
- Usage: ./hvdncomm-lora-rx_rf95.py
- Uses pyRF95 library (rf95.py)

rf95.py
- RFM95 library used by hvdncom apps ending in rf95.py
- Sourced from https://github.com/ladecadence/pyRF95


