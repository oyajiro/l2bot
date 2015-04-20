import pyautogui, win32api, win32con, ctypes, autoit
from PIL import ImageOps, Image, ImageGrab
from numpy import *
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

# 967 55
# 1120 62

def main():
    autoit.win_wait(title, 5)
    cycle = True
    while cycle:
        cpstatus = checkOwnCp()
        hpstatus = checkOwnHp()
        print 'cp ' + str(cpstatus)
        print 'hp ' + str(hpstatus)
        if cpstatus == 0:
            if hpstatus == 0:
                print 'Dead'
                cv2.imwrite('Dead' + str(int(time.time())) + '.png',getScreen(leftCornerx,leftCornery,x2,fullY2))
                cycle = False
        if cpstatus < 2:
            if hpstatus > 0:
                autoit.control_send(title, '', '{F8}', 0)
                sleep(0.8,1.5)
    pass

if __name__ == '__main__':
    main()