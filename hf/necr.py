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
        mpstatus = bot.checkOwnMp()
        print 'hp ' + str(hpstatus)
        if hpstatus == 0:
            print 'Dead'
            cv2.imwrite('Dead' + str(int(time.time())) + '.png',bot.getScreen(leftCornerx,leftCornery,x2,fullY2))
            cycle = False
        if hpstatus == 1:
            autoit.control_send(bot.title, '', '{F5}', 0)
        print 'mp ' + str(mpstatus)
        if mpstatus < 2:
            autoit.control_send(bot.title, '', '{F11}', 0)
        res = bot.findHP();
        print 'tgs ' + str(res)
        if res == 3:
            fullCounter += 1
            print 'fc ' + str(fullCounter)
        else:
            fullCounter = 0
        if fullCounter > 9:
            autoit.control_send(bot.title, '', '{ESC}', 0)
            bot.sleep(0.3,0.6)
            # autoit.control_send(bot.title, '', '{F3}', 0)
            # bot.mouseRotate()
            fullCounter = 0
            
        if res > 0:
            autoit.control_send(bot.title, '', '{F1}', 0)
            counter = 0
            bot.sleep(0.1,0.2)
            autoit.control_send(bot.title, '', '{F2}', 0)
        else:
            fullCounter = 0
            autoit.control_send(bot.title, '', '{F9}', 0)
            if counter < 2:
                autoit.control_send(bot.title, '', '{F3}', 0)
                bot.sleep(0.1,0.2)
                autoit.control_send(bot.title, '', '{F1}', 0)

            if counter > 1:
                # bot.findTarget()
                autoit.control_send(bot.title, '', '{F7}', 0)
                counter = 0
            counter += 1
        print 'cnt ' + str(counter)
    pass

if __name__ == '__main__':
    main()
