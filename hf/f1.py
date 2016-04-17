import pyautogui, win32api, win32con, ctypes, autoit
from PIL import ImageOps, Image, ImageGrab
from numpy import *
import os
import time
import sys
import cv2
import random
from Bot import  *

def main():
    bot = Bot()
    wincount = sys.argv[1]
    autoit.win_wait(bot.title, 5)
    counter = 0
    cycle = True
    while cycle:
        print 'send'
        for count in range(1, int(wincount)+1):
            title = "[TITLE:Lineage II; INSTANCE:" + str(count) + "]"
            autoit.control_send(title, '', '{F1}', 0)
            bot.sleep(0.1,0.3)
            autoit.control_send(title, '', '{F1}', 0)
            bot.sleep(0.7,1.3)
            print 'title ', title
        bot.sleep(0.3,0.8)

main()