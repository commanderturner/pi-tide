
from ast import Or
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

def updateDisplay(display: Display, date: datetime):
    dateAsYYYYMMDD = date.strftime('%Y-%m-%d')
    dateData = getDataForDate(dateAsYYYYMMDD)
    if dateData:
        print ("Data found for ", dateAsYYYYMMDD)
        dateAsDDMonYYYY = date.strftime('%d %b %Y')
        display.writeTideTime(dateData, dateAsDDMonYYYY)
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

def updateDisplayIfRequired(display: Display, firstRun: bool):
    print('Checking if display needs updating...')
    today = datetime.today()
    if firstRun == True or today.date() != lastDateUsed.date():
        print('display needs updating...')
        lastDateUsed = today
        updateDisplay(display, lastDateUsed)

def runForever():
    print('commencing runForever method...')
    updateDisplayIfRequired(display, True)
    try:
        while True:
            print('will check to update in 10 mins...')
            time.sleep(600)
            updateDisplayIfRequired(display, False)
    except KeyboardInterrupt:
        display.off()

print('initialising')
lastDateUsed: datetime = datetime.today()
display = Display()
runForever()
# display.writeText('Alas no data')
# try:
#     while True:
#         print('will check to update in 10 mins...')
#         time.sleep(600)
# except KeyboardInterrupt:
#     display.off()