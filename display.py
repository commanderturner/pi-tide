#!/usr/bin/env python
# -*- coding: utf-8 -*-
# See LICENSE.rst for details.
# PYTHON_ARGCOMPLETE_OK

"""
Displays the current playing track on volumio
"""

import os
# from demo_opts import get_device
from PIL import ImageFont
from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.oled.device import sh1106
# from luma.oled.device import ssd1306, ssd1309, ssd1325, ssd1331, sh1106

font_path1 = os.path.abspath(os.path.join(os.path.dirname(__file__),'fonts', 'DejaVuSansMono.ttf'))
# font_path2 = os.path.abspath(os.path.join(os.path.dirname(__file__),'fonts', 'DejaVuSans.ttf'))
font1 = ImageFont.truetype(font_path1, 14)
# font2 = ImageFont.truetype(font_path2, 11)
StatLine = 0
# DataLine = 17         # allow one line for weird ascenders and accent marks
# LineSpace = 16

class Display:

    def __init__(self):
        print('initialising display...')
        # if __name__ == "__main__":
        try:
            # rev.1 users set port=0
            # substitute spi(device=0, port=0) below if using that interface
            # substitute ssd1331(...) or sh1106(...) below if using that device
            # device = get_device()
            print('setting up 1106...')
            serial = i2c(port=1, address=0x3C)
            self.device = sh1106(serial)
            # if self.device:
            #     print('found sh1106 device')
            #     main()
        except KeyboardInterrupt:
            pass

    # def writeText(self, textArray):
    #     # print 'checking track info...'
    #     if len(textArray):
    #         self.device.show()
    #         print('writing text:', textArray)
    #         with canvas(self.device) as draw:
    #             if textArray[0]:
    #                 draw.text((1, 0), text=textArray[0], font=font1, fill="white") 
    #             if textArray[1]:
    #                 draw.text((1, 17), text=textArray[1], font=font1, fill="white")
    #     else:
    #         self.off()
    def writeText(self, text):
        # print 'checking track info...'
        self.device.show()
        print('writing text:', text)
        with canvas(self.device) as draw:
            if text:
                draw.text((1, 0), text=text, font=font1, fill="white") 

    def writeTideTime(self, item, date):
        self.device.show()
        print('writing tide data...')
        with canvas(self.device) as draw:
            if item:
                high1Time = item["high_1_time"]
                high2Time = item["high_2_time"]
                low1Time = item["low_1_time"]
                low2Time = item["low_2_time"]
                draw.text((1, 0), text="high", font=font1, fill="white")
                if high1Time:
                    draw.text((40,0), text=high1Time, font=font1, fill="white")
                if high2Time:
                    draw.text((85,0), text=high2Time, font=font1, fill="white")
                draw.text((1, 25), text="low", font=font1, fill="white")
                if low1Time:
                    draw.text((40, 25), text=low1Time, font=font1, fill="white")
                if low2Time:
                    draw.text((85, 25), text=low2Time, font=font1, fill="white")
                draw.text((30, 50), text=date, font=font1, fill="white")

    def off(self):
        print('turning off display')
        self.device.hide()

    # def main():
    #     print('initialising display...')
    #     output_track()
        # while True:
        #     time.sleep(5)
        #     output_track()


