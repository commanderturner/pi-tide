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
# font_path2 = os.path.abspath(os.path.join(os.path.dirname(__file__),'fonts', 'DejaVuSans.ttf'))
fontNormal = ImageFont.truetype(fontNormalPath, 12)
fontLight = ImageFont.truetype(fontLightPath, 12)
fontInfo = ImageFont.truetype(fontInfoPath, 10)
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
            draw.text((24, 0), text=dateFormatted, font=fontInfo, fill="white")
            # 2nd add high
            # 3rd add low
            # text.draw(x, y) (1,0) = top left corner 128x64
            if item:
                high1Time = item.get("high_1_time")
                high2Time = item.get("high_2_time")
                low1Time = item.get("low_1_time")
                low2Time = item.get("low_2_time")
                draw.text((1, 16), text="~~~~~_", font=fontInfo, fill="white")
                if high1Time:
                    draw.text((40,16), text=high1Time, font=fontInfo, fill="white")
                if high2Time:
                    draw.text((85,16), text=high2Time, font=fontInfo, fill="white")
                draw.text((1, 33), text="~~____", font=fontInfo, fill="white")
                if low1Time:
                    draw.text((40, 32), text=low1Time, font=fontInfo, fill="white")
                if low2Time:
                    draw.text((85, 32), text=low2Time, font=fontInfo, fill="white")
                # 4th add beach name ====   Perranporth  ====
                beachLine = "Perranporth"
                draw.text((32, 54), text=beachLine, font=fontInfo, fill="white")
                
    def writeSunRiseSunset(self, item: TideDatum, dateFormatted:str):
        self.device.show()
        print('writing sunrise/sunset data...')
        with canvas(self.device) as draw:
            # 1st do ==== 26th Sept 2022 ====
            draw.text((24, 0), text=dateFormatted, font=fontInfo, fill="white")
            if item:
                sunrise = item.get("sunrise")
                sunset= item.get("sunset")
                if sunrise:
                    draw.text((20,16), text="sunrise: " + sunrise, font=fontInfo, fill="white")
                if sunset:
                     draw.text((20,32), text="sunset: " + sunset, font=fontInfo, fill="white")
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


