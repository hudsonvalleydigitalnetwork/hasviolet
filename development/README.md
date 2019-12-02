# HAS Violet
Project HAS Violet, brought to you by HVDN, the letter Q and numbers 8, 4 and 5. 

DEVELOPMENT

All code in this directory remains experiental. Use at your own risk.


font5x8.bin
- Font file for the Adafruit OLED display

hvdn-comm.ini
- Config file used by hvdncomm apps (differs from stable version)

hvdncomm-lora-chat.py
- Half-duplex LoRa messgaing app (255)
- Usage: ./hvdncomm-lora-chat
- %1 is number of times to repeat, %2 is message in double quotes
- Uses raspi-lora library which needs to be installed ( sudo pip3 install raspi-lora )
- More info at https://pypi.org/project/raspi-lora/

rf95.py
- RFM95 library used by hvdncom apps ending in rf95.py
- Sourced from https://github.com/ladecadence/pyRF95

test.py
- Test program that verifies board and demonstrates how to display text
- Adapted from : https://learn.adafruit.com/lora-and-lorawan-for-raspberry-pi
