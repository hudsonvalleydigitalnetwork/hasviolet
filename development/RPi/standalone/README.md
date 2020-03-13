# HASviolet

## Standalone

All files for HASviolet to run standalone

### HASviolet-service-install.sh
* HASviolet.servce in installer

### HASviolet.service
* Service starts HASviolent-duckhunt.py on startup

### HASviolet-service.sh {start | stop}
* Start and stop HASviolet.service from shell
* Service must be stopped in any interactive shell session when using other HASvbiolet apps

### HASviolet-duckhunt.py
* Runs on RPI Z WH startup through systemd as HASviolet.service
* Left button runs beacon, Right button receives, Middle button quits

### rf95.py
* RFM95 library used by hvdncom apps ending in rf95.py
* Sourced from https://github.com/ladecadence/pyRF95

### font5x8.bin
* Font file for the Adafruit OLED display

### HASviolet.ini
* Config file used by HASviolet apps. File may contain new options-parameters
