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
 
def getScreen(x1, y1, x2, y2):
    box = (x1, y1, x2, y2)
    screen = ImageGrab.grab(box)
    img =  array(screen.getdata(),dtype=uint8).reshape((screen.size[1],screen.size[0],3))
    # img = cv2.imread('snap__1426174983.png')
    # cv2.imshow('image',img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return img

def findTarget(img):    
    template_tg = cv2.imread('template_target2.png', 0)
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
        time.sleep(0.3)
        if (findFromTargeted(template_tg, left, right)):
            autoit.mouse_click('left', center-10, left[1]+70)
            return True
        pyautogui.moveTo(center,left[1]+70)
        moveMouse(center,left[1]+70)
        time.sleep(0.3)
        if (findFromTargeted(template_tg, left, right)):
            autoit.mouse_click('left', center+10, left[1]+70)
            return True
    # autoit.mouse_click('middle')

def findFromTargeted(template, left, right):
    # print template.shape
    roi = getScreen(left[0]-25+leftCornerx, left[1]-8+leftCornery, right[0]+leftCornerx, right[1]+8+leftCornery)
    # cv2.imwrite('roi' + str(int(time.time())) + '.png',roi)
    roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    # roi = img[left[1]-8:right[1]+8, left[0]-25:right[0]];
    ret,th1 = cv2.threshold(roi,200,255,cv2.THRESH_TOZERO_INV)
    ret,th2 = cv2.threshold(th1,100,255,cv2.THRESH_BINARY)
    ret,tp1 = cv2.threshold(template,200,255,cv2.THRESH_TOZERO_INV)
    ret,tp2 = cv2.threshold(tp1,100,255,cv2.THRESH_BINARY)
    wth, hth = th2.shape
    wtp, htp = tp2.shape
    if wth > wtp and hth > htp:
        res = cv2.matchTemplate(th2, tp2, cv2.TM_CCORR_NORMED)
        if (res.any()):
            # cv2.imwrite('th2' + str(int(time.time())) + '.png',th2)
            # cv2.imwrite('tp2' + str(int(time.time())) + '.png',tp2)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            print 'max_val %.2f'%max_val
            if (max_val > 0.9):
                return True
            else:
                return False
    return False
def grabHP():
    hp = getScreen(leftCornerx + 958,leftCornery + 16,leftCornerx + 1111,leftCornery + 25)

    # img = cv2.imread('snap__1426174990.png')
    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # roi = gray[16:25, 958:1111];
    return hp


def findHP(img):
    statuses = {'none': -1, 'dead' : 0,  'lhalf' : 1, 'mhalf' : 2, 'full' : 3}
    # hpcolor = [231, 73, 132]
    hpcolor = [107, 101, 107]
    hp = grabHP()
    gray = cv2.cvtColor(hp, cv2.COLOR_BGR2GRAY)
    ret,th1 = cv2.threshold(gray,120,255,cv2.THRESH_TOZERO_INV)
    ret,th1 = cv2.threshold(th1,100,255,cv2.THRESH_TOZERO)
    # cv2.imwrite('th1' + str(int(time.time())) + '.png',th1)

    (cnts, hierarchy) = cv2.findContours(th1,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    if (len(cnts) == 0):
        return statuses['dead']
    left = list(cnts[0][cnts[0][:,:,0].argmin()][0])
    px = hp[left[1], left[0]];
    # print px
    if (hpcolor != px).any():
        return statuses['none']

    leftx = list(cnts[0][cnts[0][:,:,0].argmin()][0])[0]
    rightx = list(cnts[0][cnts[0][:,:,0].argmax()][0])[0]
    diff = rightx - leftx
    if diff > 140:
        return statuses['full']
    if diff >= 75:
        return statuses['mhalf']
    if diff < 75:
        return statuses['lhalf']
    return statuses['dead']

def moveMouse(x,y):
    autoit.mouse_move(x,y)
def rotate:
    autoit.mouse_move(968, 474)
    time.sleep(1)
    autoit.mouse_down('right')
    autoit.mouse_move(970, 474)
    autoit.mouse_up('right')

def main():
    title = "[CLASS:l2UnrealWWindowsViewportWindow]"
    autoit.win_wait(title, 5)
    counter = 0
    splcnt = 0
    time.sleep(2)
    

    # while True:
    #     img = getScreen(leftCornerx,leftCornery,x2,y2)
    #     res = findHP(img);
    #     print res
    #     if res > 0:
    #         if res > 2 and splcnt < 2:
    #             autoit.control_send(title, '', '{F2}', 0)
    #             time.sleep(2)
    #             splcnt += 1
    #         else:
    #             autoit.control_send(title, '', '{F1}', 0)
    #             time.sleep(2)
    #         counter = 0
    #     else:
    #         if res == 0 and counter == 0:
    #             autoit.control_send(title, '', '{F4}', 0)
    #         splcnt = 0

    #         if counter == 1:
    #             autoit.control_send(title, '', '{F3}', 0)

    #         if counter > 2:
    #             findTarget(img)
    #             counter = 0
    #         counter += 1
    #     print 'counter ' + str(counter)
    pass

if __name__ == '__main__':
    main()
