# ESP32

This is BETA code for HASviolet Duck for the ESP32.

HARDWARE: Heltec WiFi LoRa 32 (V2)
https://heltec-automation-docs.readthedocs.io/en/latest/esp32/wifi_lora_32/hardware_update_log.html#v2
https://heltec.org/project/wifi-lora-32/
https://www.amazon.com/gp/product/B07WHRS2XG

IDE: PlatformIO on VS Code

**INSTALLATION:
To use the code on your ESP32 you will need to install VS Code and PlatformIO plus board drivers and libraries. Then
access this folder as workspace. All this is necessary to compile and upload the binaries to your ESP32. This code should
work on any ESP32 with SX1276 LoRa module and a 0.96in OLED attached. Use at your own risk.

**FIRST TIME USE:
- Power up the ESP32 and connect to the serial monitor
- Once you see the HVDN logo a WiFi AP will become available called Duck
- Connect to the Duck AP with the password 123456789
- Open a web browser and connect to 192.168.4.1
- You will have the following menu selections

    Send
    Receive
    show duck.cfg
    show duckhunt.cfg
    set duck.cfg
    set duckhunt.cfg

- Go to "set duck.cfg", make changes, and engage
- Go to "set duckhunt.cfg", make changes, and engage
- press RST button on ESP32

The default behavior is for the Duck to beacon on startup. The 'Send' function works if you want to 
slip a message in. 'Receive' is not available at this time.


