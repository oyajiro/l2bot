import pyautogui, win32api, win32con, ctypes, autoit
from PIL import ImageOps, Image, ImageGrab
from numpy import *
from functions import *
import os
import time
import cv2
import random
from functions import  *

leftCornerx = 7
leftCornery = 38
x2 = 1554
# y2 = 1000
y2 = 405
fullY2 = 1000
title = "[CLASS:l2UnrealWWindowsViewportWindow]"

def main():
    autoit.win_wait(title, 5)
    counter = 0
    poitonUse = 0
    cycle = True
    while cycle:
        hpstatus = checkOwnHp()
        print 'hp ' + str(hpstatus)
        if hpstatus == -1:
            print 'CPDamage'
            cv2.imwrite('CPDamage' + str(int(time.time())) + '.png',getScreen(leftCornerx,leftCornery,x2,fullY2))
            cycle = False
            # autoit.win_kill(title)
        if hpstatus == 0:
            print 'Dead'
            cv2.imwrite('Dead' + str(int(time.time())) + '.png',getScreen(leftCornerx,leftCornery,x2,fullY2))
            cycle = False
        if hpstatus == 1:
            if poitonUse == 0:
                autoit.control_send(title, '', '{F10}', 0)
            poitonUse += 1
            if poitonUse > 5:
                poitonUse = 0
        else:
            poitonUse = 0
        img = getScreen(leftCornerx,leftCornery,x2,y2)
        res = findHP(img);
        print 'tgs ' + str(res)

        if res > 0:
            autoit.control_send(title, '', '{F1}', 0)
            counter = 0

            if res == 1:
                sleep(0.3,0.6)
            if res > 1:
                sleep(2,4)
        else:
            if counter < 2:
                autoit.control_send(title, '', '{F3}', 0)
                sleep(0.1,0.2)
                autoit.control_send(title, '', '{F1}', 0)

            if counter > 1:
                findTarget()
                # autoit.control_send(title, '', '{F11}', 0)
                counter = 0
            counter += 1
        print 'cnt ' + str(counter)
    pass

if __name__ == '__main__':
    main()
