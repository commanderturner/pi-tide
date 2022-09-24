
import time
import json
from display import Display
from datetime import datetime

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


   
def getData():
    print("Reading file...")
    with open('data/tide-newquay-2022-2023.json', encoding='utf-8-sig') as tideFile:
        tideData = json.load(tideFile)
        print(tideData)
        return tideData

def getDataForDate(dateAsYYMMDD):
    tideData = getData()
    def first(iterable, default=None):
        for item in iterable:
            return item
        return default

    todayData = first(x for x in tideData if x["date"] == dateAsYYMMDD)
    return todayData

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
display = Display()
todayAsYYMMDD = datetime.today().strftime('%Y-%m-%d')
todayData = getDataForDate(todayAsYYMMDD)
if todayData["high_1_time"]:
    print ("high tide 1: ", todayData["high_1_time"])
   
    display.writeTideTime(todayData, todayAsYYMMDD)
else:
    display.writeText('Alas no data')

time.sleep(100)
display.off()