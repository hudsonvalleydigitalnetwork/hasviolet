# HAS Violet
Project HAS Violet, brought to you by HVDN, the letter Q and numbers 8, 4 and 5. 

DEVELOPMENT

All code in this directory remains experiental. Use at your own risk.


font5x8.bin
- Font file for the Adafruit OLED display

hvdn-comm.ini
- Config file used by hvdncomm apps

hvdncomm-lora-broadcast_rdl.py
- Sends message to LoRa broadcast address (255)
- Usage: ./hvdncomm-lora-broadcast_rdla.py %1 %2
- %1 is number of times to repeat, %2 is message in double quotes
- Uses raspi-lora library which needs to be installed ( sudo pip3 install raspi-lora )
- More info at https://pypi.org/project/raspi-lora/

hvdncomm-lora-message_rdl.py
- Sends message to another LoRa station
- Usage: ./hvdncomm-lora-message_rdl.py %1 %2
- %1 is node address of destination (1-255), %2 is message in double quotes
- Uses pyRF95 library (rf95.py)

hvdncomm-lora-rx_ada.py
- Listens for messages from other LoRa stations
- Usage: ./hvdncomm-lora-rx_ada.py
- Uses raspi-lora library which needs to be installed ( sudo pip3 install raspi-lora )
- More info at https://pypi.org/project/raspi-lora/

rf95.py
- RFM95 library used by hvdncom apps ending in rf95.py
- Sourced from https://github.com/ladecadence/pyRF95

test.py
- Test program that verifies board and demonstrates how to display text
- Adapted from : https://learn.adafruit.com/lora-and-lorawan-for-raspberry-pi
