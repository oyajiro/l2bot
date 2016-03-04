import pyautogui, win32api, win32con, ctypes, autoit
from PIL import ImageOps, Image, ImageGrab
from numpy import *
import os
import time
import cv2
import random
from Bot import  *

def main():
    bot = Bot()
    autoit.win_wait(bot.title, 5)
    counter = 0
    poitonUse = 0
    cycle = True
    fullCounter = 0
    while cycle:
        hpstatus = bot.checkOwnHp()
        print 'hp ' + str(hpstatus)
        if hpstatus == 0:
            bot.sleep(2,3)
            if hpstatus == 0:
                print 'Dead'
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
        else:
            fullCounter = 0
            lure = 0
        if fullCounter > 6:
            autoit.control_send(bot.title, '', '{ESC}', 0)
            bot.sleep(0.3,0.6)
            autoit.control_send(bot.title, '', '{F3}', 0)
            # bot.mouseRotate()
            fullCounter = 0
            
        if res > 0:
            autoit.control_send(bot.title, '', '{F1}', 0)
            counter = 0

            if res == 1 or res == 3:
                bot.sleep(0.3,0.6)
            if res > 1 and res < 3:
                bot.sleep(1,3)
        else:
            fullCounter = 0
            if counter < 2:
                autoit.control_send(bot.title, '', '{F3}', 0)
                bot.sleep(0.1,0.2)
                autoit.control_send(bot.title, '', '{F1}', 0)

            if counter > 1:
                # bot.findTarget()
                print 'counrter > 1'
                autoit.control_send(bot.title, '', '{F7}', 0)
                bot.sleep(0.3,0.5)
                if bot.findHP() > 0 :
                    print 'lure'
                    autoit.control_send(bot.title, '', '{F5}', 0)
                    bot.sleep(5,7)
                counter = 0
            counter += 1
        print 'cnt ' + str(counter)
    pass

if __name__ == '__main__':
    main()
