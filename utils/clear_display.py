#!/usr/bin/python3

# Will clear the display. You may want to do this after terminating program (
# ctrl-c ) in which text is left on the screen.
#
# Adapted from : https://learn.adafruit.com/lora-and-lorawan-for-raspberry-pi
# Author: Brent Rubell for Adafruit Industries

# Import Blinka Libraries
import busio
from digitalio import DigitalInOut, Direction, Pull
import board
# Import the SSD1306 module.
import adafruit_ssd1306
# Import RFM9x
import adafruit_rfm9x

# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)

# 128x32 OLED Display
display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, addr=0x3c)
# Clear the display.
display.fill(0)
display.show()

print("Cleared")
