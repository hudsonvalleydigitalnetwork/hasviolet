# HASviolet

## Development

Project HASviolet, brought to you by HVDN, the letter Q and numbers 8, 4 and 5. 
All code in this directory is under active development. USE AT YOUR OWN RISK !!

### font5x8.bin
* Font file for the Adafruit OLED display

### HASviolet.ini
* Config file used by HASviolet apps. File may contain new options-parameters

### HASviolet-headless.service
* Used to start HASviolent-duckhunt.py on startup.
* stored in /lib/systemd/system

### HASviolet-duckhunt.py
  ```
  Runs on RPI Z WH startup through systemd as HASviolet-headless.service
  Left button runs beacon, Right button receives, Middle button quits
  ```


### rf95.py
* RFM95 library used by hvdncom apps ending in rf95.py
* Sourced from https://github.com/ladecadence/pyRF95

Svol;
