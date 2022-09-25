
from cProfile import run
import time
import json
from display import Display
from datetime import datetime
from typing import List
from typings import TideDatum

# def testDisplay():
    # display = Display()
    # trackNames = ["abba", "beatles", "coldplay", "david bowie", "eagles"]
    # trackIndex = 0
    # cycle = 1
    # print('ok here are the songs you be playing...')
    # while True:
    #     time.sleep(2)
    #     display.writeText(trackNames[trackIndex])
    #     trackIndex = trackIndex + 1
    #     if trackIndex == len(trackNames):
    #         trackIndex = 0
    #         cycle = cycle + 1
    #     if cycle == 3:
    #         display.off()
    #         print('not going to print out tracks no more!')
    #         break


   
def getData() -> List[TideDatum]:
    print("Reading file...")
    with open('data/tide-newquay-2022-2023.json', encoding='utf-8-sig') as tideFile:
        tideData = json.load(tideFile)
        print(tideData)
        return tideData

def getDataForDate(dateAsYYMMDD: str):
    tideData = getData()
    def first(iterable, default=None):
        for item in iterable:
            return item
        return default

    todayData = first(x for x in tideData if x.get("date") == dateAsYYMMDD)
    return todayData

def updateDisplay(display: Display, dateAsYYMMDD: str):
    dateData = getDataForDate(dateAsYYMMDD)
    if dateData:
        print ("Data found for ", dateAsYYMMDD)
        display.writeTideTime(dateData, dateAsYYMMDD)
    else:
        display.writeText('Alas no data')

# def runForever():
#     control = Control(1)
#     try:
#             while True:
#                 time.sleep(0.01)
#                 # count += 1;
#                 control.checkPins();
#                 # if(count == 30):
#                 #     count = 0
#                 #     control.checkPlayerState()
#     except KeyboardInterrupt:
#         control.end()

# testDisplay()


def runForever():
    display = Display()
    lastDateUsed = datetime.today().strftime('%Y-%m-%d')
    updateDisplay(display, lastDateUsed)
    try:
        while True:
            time.sleep(600)
            todayAsYYMMDD = datetime.today().strftime('%Y-%m-%d')
            if todayAsYYMMDD != lastDateUsed:
                lastDateUsed= todayAsYYMMDD
                updateDisplay(display, lastDateUsed)
    except KeyboardInterrupt:
        display.off()

runForever()