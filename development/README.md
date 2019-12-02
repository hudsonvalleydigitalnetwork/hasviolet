# HAS Violet
Project HAS Violet, brought to you by HVDN, the letter Q and numbers 8, 4 and 5. 

DEVELOPMENT

All code in this directory remains experiental. Use at your own risk.


font5x8.bin
- Font file for the Adafruit OLED display

hvdn-comm.ini
- Config file used by hvdncomm apps (differs from stable version)

hvdncomm-lora-chat.py
- Half-duplex LoRa messaging app
- Usage: ./hvdncomm-lora-chat
- Starts and loops in Listening Mode until CTRL-Z hit to send a message or CTRL-C to exit program
- When in send mode
--- Recipient is node id (255 = broadcast address)
--- Message is whatever message followed by enter
--- Message is sent, return to listening mode

rf95.py
- RFM95 library used by hvdncom apps
- Sourced from https://github.com/ladecadence/pyRF95

