#!/usr/bin/env python
#-----------------------------------------------------------------------------
# qwiic_twist_ex1.py
#
# Simple Example for the Qwiic Twist Device
#------------------------------------------------------------------------
#
# Written by  SparkFun Electronics, May 2019
# 
# This python library supports the SparkFun Electroncis qwiic 
# qwiic sensor/board ecosystem on a Raspberry Pi (and compatable) single
# board computers. 
#
# More information on qwiic is at https://www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun. Buy a board!
#
#==================================================================================
# Copyright (c) 2019 SparkFun Electronics
#
# Permission is hereby granted, free of charge, to any person obtaining a copy 
# of this software and associated documentation files (the "Software"), to deal 
# in the Software without restriction, including without limitation the rights 
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
# copies of the Software, and to permit persons to whom the Software is 
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all 
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
# SOFTWARE.
#==================================================================================
# Example 1
#

from __future__ import print_function
import qwiic_twist
import time
import sys
import pygame
import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
from time import strftime, sleep
from numpy import random

import board

from adafruit_rgb_display.rgb import color565
import adafruit_rgb_display.st7789 as st7789
import webcolors
import pygame





def runExample():

    print("\nSparkFun qwiic Twist   Example 1\n")
    myTwist = qwiic_twist.QwiicTwist()

    if myTwist.connected == False:
        print("The Qwiic twist device isn't connected to the system. Please check your connection", \
        file=sys.stderr)
        return

    myTwist.begin()

	# Set the knob color to pink
    myTwist.set_color(255, 10, 10)
    
    def getFont(size):
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)
        return font

    def getRandomXY():
        x = random.randint(240, size=10)
        y = random.randint(135, size=10) 
        return x, y


    x, y = getRandomXY()
    red = True
    green = False
    count = 0

    pygame.init()
    screen = pygame.display.set_mode((400,400))
    weather = False
    Time = False

    while True:
        draw.rectangle((0, 0, width, height), outline=0, fill=0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:
                    myTwist.set_color(10, 255, 10)
                if event.key == pygame.K_r:
                    myTwist.set_color(255, 10, 10)
                if event.key == pygame.K_w:
                    weather = True
                    Time = False
                if event.key == pygame.K_t:
                    Time = True
                    weather = False
                    
        if weather:
            font = getFont(18)
            offset_x = 1
            offset_y = 1
            for i in range(10):
                draw.text((x[i], y[i]), "❄", font=font, fill="#0000FF")
                x[i] = x[i] + offset_x if x[i] + offset_x < width else x[i] + offset_x - width
                y[i] = y[i] + offset_y if y[i] + offset_y < height else y[i] + offset_y - height
        elif Time:
            date = strftime("%m/%d/%Y")
            timer = strftime("%H:%M:%S")
            font = getFont(44)
                    
            x_1 = width/2 - font.getsize(timer)[0]/2
            y_1 = height/2 - font.getsize(timer)[1]/2
            draw.text((x_1, y_1), timer, font=font, fill="#FFFFFF")

            font = getFont(18)
            x_2 = width/2 - font.getsize(date)[0]/2
            y_1 -= font.getsize(date)[1]
            draw.text((x_2, y_1), date, font=font, fill="#FFFFFF")

        disp.image(image, rotation)
        time.sleep(0.001)

if __name__ == '__main__':
    try:
        # Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
        cs_pin = digitalio.DigitalInOut(board.CE0)
        dc_pin = digitalio.DigitalInOut(board.D25)
        reset_pin = None

        # Config for display baudrate (default max is 24mhz):
        BAUDRATE = 64000000

        # Setup SPI bus using hardware SPI:
        spi = board.SPI()

        # Create the ST7789 display:
        disp = st7789.ST7789(
            spi,
            cs=cs_pin,
            dc=dc_pin,
            rst=reset_pin,
            baudrate=BAUDRATE,
            width=135,
            height=240,
            x_offset=53,
            y_offset=40,
        )

        backlight = digitalio.DigitalInOut(board.D22)
        backlight.switch_to_output()
        backlight.value = True
        buttonA = digitalio.DigitalInOut(board.D23)
        buttonB = digitalio.DigitalInOut(board.D24)
        buttonA.switch_to_input()
        buttonB.switch_to_input()

        # Create blank image for drawing.
        # Make sure to create image with mode 'RGB' for full color.
        height = disp.width  # we swap height/width to rotate it to landscape! 135
        width = disp.height #240
        image = Image.new("RGB", (width, height))
        rotation = 90

        # Get drawing object to draw on image.
        draw = ImageDraw.Draw(image)

        # Draw a black filled box to clear the image.
        draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
        disp.image(image, rotation)
        # Draw some shapes.
        # First define some constants to allow easy resizing of shapes.
        padding = -2
        top = padding
        bottom = height - padding
        # Move left to right keeping track of the current x position for drawing shapes.
        x = 0

        # Alternatively load a TTF font.  Make sure the .ttf font file is in the
        # same directory as the python script!
        # Some other nice fonts to try: http://www.dafont.com/bitmap.php
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 44)

        # Turn on the backlight
        backlight = digitalio.DigitalInOut(board.D22)
        backlight.switch_to_output()
        backlight.value = True
        runExample()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example 1")
        sys.exit(0)

