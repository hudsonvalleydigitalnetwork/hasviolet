## HASviolet RPi Hats Guide

Adafruit LoRa Radio Bonnet with OLED-RFM95W @ 915 MHz
https://www.adafruit.com/product/4074


### Radio

* RST - Radio reset pin, connected to GPIO25 (pin 22) on the Pi
* CS - Radio SPI Chip Select pin, connected to SPI0 CE1 (pin 26/GPIO7)on the Pi
* CLK - Radio SPI Clock pin, connected to SPI0 SCLK (pin 23/GPIO11) on the Pi
* DI - Radio SPI data in pin, connected to SPI0 MOSI (pin 19/GPIO 10)on the Pi
* DO - Radio SPI data out pin, connected to SPI0 MISO (pin 21/GPIO 9) on the Pi
* DIO0 - Radio digital IO #0 pin, we use this for status or IRQs. 
       It's required for all our examples. Connected to GPIO 22 (pin 15) on the Pi
* DIO1 - Radio digital IO #1 pin, we use this for status. 
       This is not used for our basic CircuitPython code, but is used by some more
       advanced libraries. You can cut this trace if you want to use the Pi pin for
       other devices. Connected to GPIO 23 (pin 16) on the Pi
* DIO2 - Radio digital IO #2 pin, we use this for status. 
       This is not used for our basic CircuitPython code, but is used by some more
       advanced libraries. You can cut this trace if you want to use the Pi pin for
       other devices. Connected to GPIO 24 (pin 18) on the Pi
* DIO3 - Radio digital IO #3, not connected or used at this time.
* DIO4 - Radio digital IO #3, not connected or used at this time.

### OLED 128x32

* SCL is connected to SCL (pin 5/GPIO3) on the Pi
* SDA is connected to SDA (pin 3/GPIO2) on the Pi

### BUTTONS

* Button 1: Connected to GPIO 5 (pin 29) on the Pi
* Button 2: Connected to GPIO 6 (pin 31) on the Pi
* Button 3: Connected to GPIO 12 (pin 32/PWM0)on the Pi

