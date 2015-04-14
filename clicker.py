import pyautogui, win32api, win32con, ctypes, autoit
from PIL import ImageOps, Image, ImageGrab
from numpy import *
import os
import time
import cv2
import random
from functions import  *

def main():
    autoit.win_wait(title, 5)
    counter = 0
    cycle = True
    sleep(3,3)
    while cycle:
        autoit.mouse_click('right', 768, 804)
        sleep(0.1,0.2)
        counter += 1
        if counter > 861:
            cycle = False
        print counter
        if counter % 100 == 0:
            sleep(3,5)

    pass

main()