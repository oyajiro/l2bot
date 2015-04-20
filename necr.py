import pyautogui, win32api, win32con, ctypes, autoit
from PIL import ImageOps, Image, ImageGrab
from numpy import *
from functions import *
import os
import time
import cv2
import random

leftCornerx = 7
leftCornery = 38
x1 = leftCornerx
y1 = leftCornery
x2 = 1390
# y2 = 1000
y2 = 360
fullY2 = 1000
title = "[CLASS:l2UnrealWWindowsViewportWindow]"

def main():
    autoit.win_wait(title, 5)
    counter = 0
    cycle = True
    while cycle:
        hpstatus = checkOwnHp()
        mpstatus = checkOwnMp()
        print 'hps ' + str(hpstatus)
        print 'mps ' + str(mpstatus)
        if mpstatus == 1:
            autoit.control_send(title, '', '{F11}', 0)

        if hpstatus == -1:
            print 'CPDamage'
            cv2.imwrite('CPDamage' + str(int(time.time())) + '.png',getScreen(leftCornerx,leftCornery,x2,fullY2))
            # autoit.win_kill(title)
            cycle = False
        if hpstatus == 0:
            print 'Dead'
            cv2.imwrite('Dead' + str(int(time.time())) + '.png',getScreen(leftCornerx,leftCornery,x2,fullY2))
            cycle = False
        if hpstatus == 1:
            autoit.control_send(title, '', '{F5}', 0)

        img = getScreen(leftCornerx,leftCornery,x2,y2)
        res = findHP(img);
        print 'tgs ' + str(res)

        if res > 0:
            autoit.control_send(title, '', '{F1}', 0)
            counter = 0
        else:
            if counter == 0:
                autoit.control_send(title, '', '{F3}', 0)
                sleep(0.1,0.3)
                autoit.control_send(title, '', '{F1}', 0)

            counter += 1
            if counter >= 1:
                findTarget()
                # autoit.control_send(title, '', '{F11}', 0)
                counter = 0
        print 'cnt ' + str(counter)
    pass

if __name__ == '__main__':
    main()
