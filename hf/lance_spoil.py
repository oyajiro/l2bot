import pyautogui, win32api, win32con, ctypes, autoit
from PIL import ImageOps, Image, ImageGrab
from datetime import datetime
from numpy import *
import os
import time
import cv2
import random
from Bot import  *

def main():
    bot = Bot()
    print bot.title
    autoit.win_wait(bot.title, 5)
    counter = 0
    poitonUse = 0
    cycle = True
    spoilCount = 0
    fullCounter = 0
    deadCounter = 0
    while cycle:
        hpstatus = bot.checkOwnHp()
        print 'hp ' + str(hpstatus)
        checkOwnMp()
        if hpstatus == 0:
            autoit.control_send(bot.title, '', '{F9}', 0)
            bot.sleep(0.3,0.6)
            print 'I\'m Dead', str(datetime.now())
            str(datetime.now())
            cv2.imwrite('Dead' + str(int(time.time())) + '.png',bot.getScreen(leftCornerx,leftCornery,x2,fullY2))
            cycle = False
        if hpstatus == 1:
            if poitonUse == 0:
                autoit.control_send(bot.title, '', '{F10}', 0)
            poitonUse += 1
            if poitonUse > 5:
                poitonUse = 0
        else:
            poitonUse = 0
        res = bot.findHP();
        print 'tgs ' + str(res)
        if res == 3:
            fullCounter += 1
            print 'fc ' + str(fullCounter)
            autoit.control_send(bot.title, '', '{F1}', 0)
        else:
            fullCounter = 0
        if fullCounter > 6:
            autoit.control_send(bot.title, '', '{ESC}', 0)
            bot.sleep(0.1,0.3)
            autoit.control_send(bot.title, '', '{F3}', 0)
            bot.sleep(0.1,0.3)
            # bot.mouseRotate()
            fullCounter = 0
            spoilCount = 0
        if res > 0:
            autoit.control_send(bot.title, '', '{F1}', 0)
            counter = 0
            deadCounter = 0

            if res == 1:
                autoit.control_send(bot.title, '', '{F3}', 0)
                bot.sleep(0.1,0.4)
                autoit.control_send(bot.title, '', '{F1}', 0)
                bot.sleep(0.5,0.8)
                autoit.control_send(bot.title, '', '{F4}', 0)
                bot.sleep(0.1,0.4)
                autoit.control_send(bot.title, '', '{F1}', 0)


            autoit.control_send(bot.title, '', '{F5}', 0)
            bot.sleep(0.3,0.6)
            if spoilCount < 4:
                autoit.control_send(bot.title, '', '{F2}', 0)
                bot.sleep(0.3,0.6)
                autoit.control_send(bot.title, '', '{F2}', 0)
                # if spoilCount % 2 == 0:
                #     autoit.control_send(bot.title, '', '{F2}', 0)
                # else:
                #     autoit.control_send(bot.title, '', '{F6}', 0)
                bot.sleep(0.3,0.6)
                autoit.control_send(bot.title, '', '{F1}', 0)
                bot.sleep(0.1,0.3)
                autoit.control_send(bot.title, '', '{F1}', 0)
                spoilCount += 1
        else:
            deadCounter += 1
            spoilCount = 0
            bot.sleep(0.1,0.2)
            if res == 0 and counter < 2:
                autoit.control_send(bot.title, '', '{F4}', 0)
                bot.sleep(0.2,0.4)
                autoit.control_send(bot.title, '', '{F4}', 0)                   
                bot.sleep(0.1,0.3)
                autoit.control_send(bot.title, '', '{F3}', 0)            
                print 'F4'
                deadCounter = 0
            if counter < 3:
                autoit.control_send(bot.title, '', '{F3}', 0)
                bot.sleep(0.1,0.3)
                autoit.control_send(bot.title, '', '{F3}', 0)
                bot.sleep(0.1,0.3)
                autoit.control_send(bot.title, '', '{F1}', 0)
                print 'F3'
                bot.sleep(0.1,0.3)
                autoit.control_send(bot.title, '', '{F1}', 0)

            if counter > 2:
                # bot.findTarget()
                autoit.control_send(bot.title, '', '{F7}', 0)
                bot.sleep(0.1,0.3)
                autoit.control_send(bot.title, '', '{F7}', 0)
                print 'F7'
                counter = 0
            counter += 1
        print 'cnt ' + str(counter)
    pass

def checkOwnMp():
    bot = Bot()
    if bot.checkOwnMp() <= 1:
        print 'MP_USE'
        autoit.control_send(bot.title, '', '{F12}', 0)

if __name__ == '__main__':
    main()
