#!/usr/bin/python3
#
# HASvioletHID Library 2
#
#
#
#
# TO-DO:
#
#


#
# Import Libraries
#

import signal
import sys
import time
import subprocess

import argparse
import board
from board import SCL, SDA
import busio
import adafruit_ssd1306

import configparser
from digitalio import DigitalInOut, Direction, Pull
from PIL import Image, ImageDraw, ImageFont


class HAShid:
    def __init__(self):
        iniconfig = configparser.ConfigParser()
        iniconfig.sections()
        iniconfig.read('HASviolet.ini')
        try:
            self.mycall = str(iniconfig["DEFAULT"]["mycall"])
            self.ssid = int(iniconfig["DEFAULT"]["ssid"])
            self.beacon = str(iniconfig["DEFAULT"]["beacon"])
        except KeyError as e:
            raise LookupError("Error HASviolet.ini[DEFAULT] : {} missing.".format(str(e)))
            exit (1)
        self.station = self.mycall + "-" + str(self.ssid)
        self.receive = ""
        self.receive_rssi = ""
        self.receive_string = ""
        self.receive_ascii=""
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.OLED = adafruit_ssd1306.SSD1306_I2C(128, 32, self.i2c, addr=0x3c)
        self.OLED.fill(0)
        self.OLED.show()
        self.btnLeft = DigitalInOut(board.D5)
        self.btnLeft.direction = Direction.INPUT
        self.btnLeft.pull = Pull.UP
        self.btnMid = DigitalInOut(board.D6)
        self.btnMid.direction = Direction.INPUT
        self.btnMid.pull = Pull.UP
        self.btnRight = DigitalInOut(board.D12)
        self.btnRight.direction = Direction.INPUT
        self.btnRight.pull = Pull.UP
        self.setCursorX = 0
        self.setCursorY = 1


    def logo(self, logoimg):       
        # Create blank image for drawing.
        # Make sure to create image with mode '1' for 1-bit color.
        width = self.OLED.width
        height = self.OLED.height
        image = Image.new("1", (width, height))
        
        # Get drawing object to draw on image.
        draw = ImageDraw.Draw(image)
        
        # Draw some shapes.
        # # First define some constants to allow easy resizing of shapes.
        padding = -2
        top = padding
        bottom = height - padding

        # Move left to right keeping track of the current x position for drawing shapes.
        x = 0

        # Open, resize, and convert image to Black and White
        image = (
            Image.open(logoimg)
            .resize((self.OLED.width, self.OLED.height))
            .convert("1")
        )
        
        # Display the converted image
        self.OLED.image(image)
        self.OLED.show()
        time.sleep (0.5)
        #self.OLED.fill(0)
        #self.OLED.show()
        
        font = ImageFont.load_default()
        text = "HAS Violet"
        (font_width, font_height) = font.getsize(text)
        self.OLED.text(text,(self.OLED.width//2 - font_width//2), (self.OLED.height//2 - font_height//2),2)
        
        self.OLED.show()
        time.sleep (1)
        self.OLED.fill(0)
        self.OLED.show()



