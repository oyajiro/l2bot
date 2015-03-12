import pyautogui, win32api, win32con, ctypes, autoit
from PIL import ImageOps, Image, ImageGrab
from numpy import *
import os
import time
import cv2

leftCornerx = 7
leftCornery = 38
x1 = leftCornerx
y1 = leftCornery
x2 = 1390
y2 = 1000

# 967 55
# 1120 62
 
def getScreen():
    #screen = screenGrab(leftCornerx,leftCornery,x2,y2)
    #img = array(screen)
    #img = cv2.cv.fromarray(screen)
    img = cv2.imread('snap__1426174983.png')
    return img

def findTarget(img):    
    template_tg = cv2.imread('template_target2.png')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret,th1 = cv2.threshold(gray,253,255,cv2.THRESH_TOZERO_INV)
    ret,th3 = cv2.threshold(th1,251,255,cv2.THRESH_BINARY)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 15))
    closed = cv2.morphologyEx(th3, cv2.MORPH_CLOSE, kernel)
    closed = cv2.erode(closed, None, iterations = 3)
    closed = cv2.dilate(closed, None, iterations = 2)
    (cnts, hierarchy) = cv2.findContours(closed,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    approxes = []
    hulls = []
    for cnt in cnts:
        approxes.append(cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True))
        hulls.append(cv2.convexHull(cnt))
        left = list(cnt[cnt[:,:,0].argmin()][0])        
        right = list(cnt[cnt[:,:,0].argmax()][0])
        print 'left x' + str(left[0])+ 'y '+ str(left[1])
        print 'right x' + str(right[0])+ 'y '+ str(right[1])
        center = round((right[0]+left[0])/2)
        center = int(center)
        moveMouse(center-10,left[1]+70)
        time.sleep(1)
        if (findFromTargeted(gray, template_tg, left, right)):
            return (center-10,left[1]+70)
        pyautogui.moveTo(center,left[1]+70)
        moveMouse(center,left[1]+70)
        time.sleep(1)
        if (findFromTargeted(gray, template_tg, left, right)):
            return (center,left[1]+70)
        moveMouse(center+10,left[1]+70)
        time.sleep(1)
        if (findFromTargeted(gray, template_tg, left, right)):
            return (center+10,left[1]+70)

def findFromTargeted(img, template, left, right):
    w, h = template.shape[::-1]
    roi = img[left[1]-8:right[1]+8, left[0]-25:right[0]];
    ret,th1 = cv2.threshold(roi,200,255,cv2.THRESH_TOZERO_INV)
    ret,th2 = cv2.threshold(th1,100,255,cv2.THRESH_BINARY)
    ret,tp1 = cv2.threshold(template,200,255,cv2.THRESH_TOZERO_INV)
    ret,tp2 = cv2.threshold(tp1,100,255,cv2.THRESH_BINARY)
    res = cv2.matchTemplate(th2, tp2, cv2.TM_CCORR_NORMED)
    if (res.any()):
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        if (max_val > 0.9):
            return True
        else:
            return False
def grabHP():
    # hp = screenGrab(leftCornerx + 958,leftCornery + 16,leftCornerx + 1111,leftCornery + 25)
    # gray = cv2.cvtColor(hp, cv2.COLOR_BGR2GRAY)

    img = cv2.imread('snap__1426174990.png')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    roi = gray[16:25, 958:1111];
    return roi


def findHP(img):
    gray = grabHP()
    # roi = gray[leftCornery + 16:leftCornery + 25, leftCornerx + 958:leftCornerx + 1111];
    ret,th1 = cv2.threshold(gray,100,255,cv2.THRESH_BINARY)
    (cnts, hierarchy) = cv2.findContours(th1,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    # print len(cnts)
    # cv2.drawContours(roi, cnts, -1, (0,255,0), 3)
    leftmost = tuple(cnts[cnts[:,:,0].argmin()][0])
    rightmost = tuple(cnts[cnts[:,:,0].argmax()][0])
    print leftmost
    print rightmost
    return False

def moveMouse(x,y):
    autoit.mouse_move(x,y)

def main():
    img = getScreen()
    title = "[CLASS:l2UnrealWWindowsViewportWindow]"
    if (findHP(img)):
        print '1'
        # autoit.control_send(title, "", '{F1}', 1)
    pass

if __name__ == '__main__':
    main()
