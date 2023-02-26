#!/usr/bin/env python
# -*- coding: utf-8 -*-
# See LICENSE.rst for details.
# PYTHON_ARGCOMPLETE_OK

"""
Displays the tide data for specified date on sh1106 display
"""

import os
# from demo_opts import get_device
from PIL import ImageFont
from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.oled.device import sh1106
from typings import TideDatum
# from luma.oled.device import ssd1306, ssd1309, ssd1325, ssd1331, sh1106

fontNormalPath = os.path.abspath(os.path.join(os.path.dirname(__file__),'fonts', 'DejaVuSans.ttf'))
fontLightPath = os.path.abspath(os.path.join(os.path.dirname(__file__),'fonts', 'DejaVuSans-ExtraLight.ttf'))
fontInfoPath = os.path.abspath(os.path.join(os.path.dirname(__file__),'fonts', 'FreePixel.ttf'))
fontNotoPath = os.path.abspath(os.path.join(os.path.dirname(__file__),'fonts', 'NotoEmoji-VariableFont_wght.ttf'))
fontAwesomePath = os.path.abspath(os.path.join(os.path.dirname(__file__),'fonts', 'fontawesome-webfont.ttf'))
# font_path2 = os.path.abspath(os.path.join(os.path.dirname(__file__),'fonts', 'DejaVuSans.ttf'))
fontNormal = ImageFont.truetype(fontNormalPath, 11)
fontLight = ImageFont.truetype(fontLightPath, 12)
fontInfo = ImageFont.truetype(fontInfoPath, 11)
fontForWave = ImageFont.truetype(fontNormalPath, 11)
fontNoto = ImageFont.truetype(fontNotoPath, 11, encoding="unic")
fontAwesome = ImageFont.truetype(fontAwesomePath, 11, encoding="unic")
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
            if self.device:
                print('found sh1106 device')
            #     main()
        except KeyboardInterrupt:
            pass

    def writeText(self, text):
        # print 'checking track info...'
        self.device.show()
        print('writing text:', text)
        with canvas(self.device) as draw:
            if text:
                draw.text((1, 0), text=text, font=fontNormal, fill="white") 

    def writeTideTime(self, item: TideDatum, dateFormatted:str):
        self.device.show()
        print('writing tide data...')
        with canvas(self.device) as draw:
            # 1st do ==== 26th Sept 2022 ====
            draw.text((24, 3), text=dateFormatted, font=fontInfo, fill="white")
            draw.text((96, 2), text="~~~", font=fontForWave, fill="white")
            # draw.text((88, 0), text=u"\u01F30A", font=fontNoto, fill="white")
            # 2nd add high
            # 3rd add low
            # text.draw(x, y) (1,0) = top left corner 128x64
            if item:
                high1Time = item.get("high_1_time")
                high2Time = item.get("high_2_time")
                low1Time = item.get("low_1_time")
                low2Time = item.get("low_2_time")
                draw.text((1, 20), text="high tide", font=fontInfo, fill="white")
                if high1Time:
                    draw.text((60,20), text=high1Time, font=fontInfo, fill="white")
                if high2Time:
                    draw.text((95,20), text=high2Time, font=fontInfo, fill="white")
                draw.text((1, 36), text="low tide", font=fontInfo, fill="white")
                if low1Time:
                    draw.text((60, 36), text=low1Time, font=fontInfo, fill="white")
                if low2Time:
                    draw.text((95, 36), text=low2Time, font=fontInfo, fill="white")
                # 4th add beach name ====   Perranporth  ====
                beachLine = "Perranporth"
                draw.text((32, 54), text=beachLine, font=fontInfo, fill="white")
                
    def writeSunRiseSunset(self, item: TideDatum, dateFormatted:str):
        self.device.show()
        print('writing sunrise/sunset data...')
        with canvas(self.device) as draw:
            # 1st do ==== 26th Sept 2022 ====
            draw.text((24, 3), text=dateFormatted, font=fontInfo, fill="white")
            draw.text((96, 0), text=u"\uF185", font=fontAwesome, fill="white")
            if item:
                sunrise = item.get("sunrise")
                sunset= item.get("sunset")
                if sunrise:
                    draw.text((1,20), text="sunrise:", font=fontInfo, fill="white")
                    draw.text((50,20), text=sunrise, font=fontInfo, fill="white")
                if sunset:
                     draw.text((1,36), text="sunset:", font=fontInfo, fill="white")
                     draw.text((50,36), text=sunset, font=fontInfo, fill="white")
            beachLine = "Perranporth"
            draw.text((32, 54), text=beachLine, font=fontInfo, fill="white")
            
    def off(self):
        print('turning off display')
        self.device.hide()

    # def main():
    #     print('initialising display...')
    #     output_track()
        # while True:
        #     time.sleep(5)
        #     output_track()


