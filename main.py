
from ast import Or
from cProfile import run
import time
import json
from display import Display
from datetime import datetime
from typing import List
from typings import TideDatum
   
def getData() -> List[TideDatum]:
    print("Reading file...")
    with open(sourceFile, encoding='utf-8-sig') as tideFile:
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
sourceFile = 'data/tide-perranporth-2022-2023.json'
display = Display()
runForever()
# display.writeText('Alas no data')
# try:
#     while True:
#         print('will check to update in 10 mins...')
#         time.sleep(600)
# except KeyboardInterrupt:
#     display.off()