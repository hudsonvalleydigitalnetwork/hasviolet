#!/usr/bin/python3

# Test program that verifies board and demonstrates how to display text
# Adapted from : https://learn.adafruit.com/lora-and-lorawan-for-raspberry-pi
# Author: Brent Rubell for Adafruit Industries

# Import Python System Libraries
import time
# Import Blinka Libraries
import busio
from digitalio import DigitalInOut, Direction, Pull
import board
# Import the SSD1306 module.
import adafruit_ssd1306
# Import RFM9x
import adafruit_rfm9x

# Button A
btnA = DigitalInOut(board.D5)
btnA.direction = Direction.INPUT
btnA.pull = Pull.UP

# Button B
btnB = DigitalInOut(board.D6)
btnB.direction = Direction.INPUT
btnB.pull = Pull.UP

# Button C
btnC = DigitalInOut(board.D12)
btnC.direction = Direction.INPUT
btnC.pull = Pull.UP

# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)

# 128x32 OLED Display
display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, addr=0x3c)
# Clear the display.
display.fill(0)
display.show()
width = display.width
height = display.height

# Configure LoRa Radio
CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0)
rfm9x.tx_power = 23
prev_packet = None

print("rfm9x board working")
print("SSD1306 Module working")
print("Please press a board button")

# Only do loop for 10 seconds
t_end = time.time() + 10

while time.time() < t_end:

    # draw a box to clear the image
    display.fill(0)
    display.text('Press button', 35, 0, 1)

    if not btnA.value:
        # Button A
        display.fill(0)
        display.text('Button A!', 25, 15, 1)
        print("Button A!")
    elif not btnB.value:
        # Button B
        display.fill(0)
        display.text('Button B!', 25, 15, 1)
        print("Button B!")
    elif not btnC.value:
        # Button C
        display.fill(0)
        display.text('Button C!', 25, 15, 1)
        print("Button C!")

    display.show()
    time.sleep(0.1)

# Clear the display
display.fill(0)
display.show()

print("now exiting")
