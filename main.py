
from ast import Or
from cProfile import run
import time
import json
from display import Display
from datetime import datetime
from typing import List, Literal
from typings import TideDatum
from gpiozero import Button
   
def getData() -> List[TideDatum]:
    print("Reading file...")
    with open(sourceFile, encoding='utf-8-sig') as tideFile:
        tideData = json.load(tideFile)
        # print(tideData)
        return tideData

def getDataForDate(dateAsYYMMDD: str):
    tideData = getData()
    def first(iterable, default=None):
        for item in iterable:
            return item
        return default

    dataForDate = first(x for x in tideData if x.get("date") == dateAsYYMMDD)
    return dataForDate

def updateDisplay():
    global display
    global lastDateUsed
    global current_view
    print('Checking if display needs updating...')
    print('Current view is', current_view)
    today = datetime.today()
    dateAsYYYYMMDD = today.strftime('%Y-%m-%d')
    dateData = getDataForDate(dateAsYYYYMMDD)
    if dateData:
        print ("Data found for ", dateAsYYYYMMDD)
        dateAsDDMonYYYY = today.strftime('%d %b %Y')
        if current_view == 'tide_times':
            display.writeTideTime(dateData, dateAsDDMonYYYY)
        elif current_view == 'sunrise_sunset':
            display.writeSunRiseSunset(dateData, dateAsDDMonYYYY)
    else:
        display.writeText('Alas no data')

def runForever():
    global display
    print('commencing runForever method...')
    updateDisplay()
    try:
        while True:
            print('will check to update in 10 mins...')
            time.sleep(600)
            updateDisplay()
    except KeyboardInterrupt:
        display.off()

def toggleView():
    global toggle_view_button
    global current_view
    print('Toggle view button pressed')
    if current_view == 'tide_times':
        current_view = 'sunrise_sunset'
    elif current_view == 'sunrise_sunset':
        current_view = 'tide_times'
    updateDisplay()
    

print('initialising')
toggle_view_button = Button(17)
toggle_view_button.when_pressed = toggleView
# 'tide_times' | 'sunrise_sunset'
current_view: Literal['tide_times', 'sunrise_sunset'] = 'tide_times'
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