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
    bot.sleep(5,10)
    autoit.control_send(bot.title, '', 'oyajirospoil', 30)
    bot.sleep(7,10)
    autoit.control_send(bot.title, '', '8w141qtf', 30)
    bot.sleep(7,10)
    autoit.control_send(bot.title, '', '{NUMPADENTER}', 30)
    bot.sleep(7,10)
    autoit.control_send(bot.title, '', '{NUMPADENTER}', 30)
    pass

if __name__ == '__main__':
    main()
