# HASviolet Duck ESP32

This is development code for HASviolet Duck for the ESP32. It is a replica of the IDE workspace under [PlatformIO](https://platformio.org/) on [Visual Studio Code](https://code.visualstudio.com/) with [Heltec ESP32 support](https://docs.platformio.org/en/latest/boards/espressif32/heltec_wifi_lora_32_V2.html).

All code run and tested on [Heltec WiFi LoRa 32 (V2)](https://heltec-automation-docs.readthedocs.io/en/latest/esp32/wifi_lora_32/hardware_update_log.html#v2)
as purchased on [Amazon](https://www.amazon.com/gp/product/B07WHRS2XG)

## Duck Setup (first time Use)
* Power up the ESP32 and connect the serial monitor to watch debug output
* Once you see the HVDN logo a WiFi AP will become available called Duck
* Connect to the Duck AP with the password 123456789
* Open a web browser and connect to 192.168.4.1
* You will have the following menu selections
  * Send
  * Receive (disabled)
  * show duck.cfg
  * show duckhunt.cfg
  * set duck.cfg
  * set duckhunt.cfg
* Go to "set duck.cfg", make changes, and engage
* Go to "set duckhunt.cfg", make changes, and engage
* press RST button on ESP32

## Duck behavior
The default behavior is for the Duck to beacon on startup. 'Send' function can be used to insert
additional one time messages. Changes to Duckhunt.cfg will occur real time for messages and triggers
that have yet to been tripped. Other changes requires reset RST button pressed on your ESP32.