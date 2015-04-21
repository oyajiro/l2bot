import pyautogui
import win32api
import win32con
import ctypes
import autoit
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
x1 = leftCornerx
y1 = leftCornery
x2 = 1554
# y2 = 1000
y2 = 360
fullY2 = 1000
title = "[CLASS:l2UnrealWWindowsViewportWindow]"

def main():
    autoit.win_wait(title, 5)
    counter = 0
    splcnt = 0
    poitonUse = 0
    cycle = True
    while cycle:
        hpstatus = checkOwnHp()
        cpstatus = checkOwnCp()
        print 'hps ' + str(hpstatus)
        print 'cps ' + str(cpstatus)
        if cpstatus < 3:
            print 'CPDamage'
            cv2.imwrite('CPDamage' + str(int(time.time())) + '.png',getScreen(leftCornerx,leftCornery,x2,fullY2))
            autoit.win_kill(title)
        if hpstatus == 0:
            print 'Dead'
            cv2.imwrite('Dead' + str(int(time.time())) + '.png',getScreen(leftCornerx,leftCornery,x2,fullY2))
            cycle = False
            continue
            # autoit.win_kill(title)
        if hpstatus == 1:
            if poitonUse == 0:
                autoit.control_send(title, '', '{F10}', 0)
            poitonUse += 1
            if poitonUse > 5:
                poitonUse = 0
        else:
            poitonUse = 0

        if hpstatus == -1:
            autoit.control_send(title, '', '{F9}', 0)
            sleep(6,10)
            restoreMenyHp()
            autoit.control_send(title, '', '{F9}', 0)

        img = getScreen(leftCornerx,leftCornery,x2,y2)
        res = findHP(img);
        print 'tgs ' + str(res)

        if res > 0:
            if res > 2 and splcnt < 4:
                autoit.control_send(title, '', '{F2}', 0)
                sleep(1,3)
                splcnt += 1
            else:
                autoit.control_send(title, '', '{F1}', 0)
                if (res > 1):
                    sleep(2,4)
                else:
                    sleep(0.5, 1)
            counter = 0
        else:
            splcnt = 0
            if res == 0:
                autoit.control_send(title, '', '{F4}', 0)
                sleep(0.2,0.7)

            if counter < 2:
                autoit.control_send(title, '', '{F3}', 0)
                if res == 0 and counter == 0:
                    sleep(0.1,0.3)
                    autoit.control_send(title, '', '{F2}', 0)

            if counter > 1:
                findTarget()
                # autoit.control_send(title, '', '{F11}', 0)
                counter = 0
            counter += 1
        print 'cnt ' + str(counter)
    pass

if __name__ == '__main__':
    main()
