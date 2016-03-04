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
    print bot.title
    autoit.win_wait(bot.title, 5)
    counter = 0
    poitonUse = 0
    cycle = True
    summAttackCount = 0
    while cycle:
        hpstatus = bot.checkOwnHp()
        print 'hp ' + str(hpstatus)
        if hpstatus == 0:
            print 'Dead'
            cv2.imwrite('Dead' + str(int(time.time())) + '.png',getScreen(leftCornerx,leftCornery,x2,fullY2))
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

        if res > 0:
            autoit.control_send(bot.title, '', '{F1}', 0)
            bot.sleep(0.1,0.6)
            autoit.control_send(bot.title, '', '{F2}', 0)
            counter = 0

            if res == 1:
                bot.sleep(0.3,0.6)
            if res > 1:
                if summAttackCount < 3:
                    autoit.control_send(bot.title, '', '{F2}', 0)
                bot.sleep(1,3)
                summAttackCount += 1
            # autoit.control_send(bot.title, '', '{F5}', 0)
        else:
            autoit.control_send(bot.title, '', '{F5}', 0)
            if counter < 3:
                autoit.control_send(bot.title, '', '{F3}', 0)
                bot.sleep(0.1,0.2)
                autoit.control_send(bot.title, '', '{F1}', 0)

            if counter > 1:
                # bot.findTarget()
                autoit.control_send(bot.title, '', '{F7}', 0)
            if counter > 2:
                autoit.control_send(bot.title, '', '{F8}', 0)
                counter = 0
            counter += 1
        print 'cnt ' + str(counter)
    pass

if __name__ == '__main__':
    main()
