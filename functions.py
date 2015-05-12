import win32api, win32con, ctypes, autoit
from PIL import ImageOps, Image, ImageGrab
from numpy import *
import os
import time
import cv2
import random
import winsound

leftCornerx = 7
leftCornery = 38
x1 = leftCornerx
y1 = leftCornery
x2 = 1554
y2 = 360
fullY2 = 1000
title = "[CLASS:l2UnrealWWindowsViewportWindow]"

def getScreen(x1, y1, x2, y2):
    box = (x1, y1, x2, y2)
    screen = ImageGrab.grab(box)
    img =  array(screen.getdata(),dtype=uint8).reshape((screen.size[1],screen.size[0],3))
    # img = cv2.imread('snap__1426174983.png')
    # cv2.imshow('image',img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return img

def getTargetCntrs(img):
    # img[leftCornery:106, leftCornerx:506]=cv::Scalar(0, 0, 0)
    img[0:106, 0:506]=(0, 0, 0)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # for i in xrange(245,255):
    #     ret,th1 = cv2.threshold(gray,i,255,cv2.THRESH_TOZERO_INV)
    #     for j in xrange(230,255):
    #         ret,th3 = cv2.threshold(th1,j,255,cv2.THRESH_BINARY)
    # #     # cv2.imwrite('th1_' + str(i) + str(int(time.time())) + '.png',th1)
    # #     ret,th3 = cv2.threshold(th1,i,255,cv2.THRESH_BINARY)
    #         cv2.imwrite('tg\\th3_i' + str(i) + '_j' + str(j) + '_' + str(int(time.time())) + '.png',th3)
    # bla()
    ret,th1 = cv2.threshold(gray,254,255,cv2.THRESH_TOZERO_INV)
    ret,th3 = cv2.threshold(th1,252,255,cv2.THRESH_BINARY)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (80, 5))
    closed = cv2.morphologyEx(th3, cv2.MORPH_CLOSE, kernel)
    # cv2.imshow('closed0',closed)
    kernel2 = ones((1,2),uint8)
    # print 'kernel ' + str(kernel2)
    closed = cv2.erode(closed, kernel2,iterations = 2)
    # cv2.imshow('closed1',closed)
    closed = cv2.dilate(closed, None, iterations = 3)
    # cv2.imshow('closed2',closed)
    (cnts, hierarchy) = cv2.findContours(closed,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    # cv2.drawContours(img, cnts, -1, (0,255,0), 3)
    # cv2.imshow('image',img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # bla()
    return cnts;

def findTarget():
    img = getScreen(leftCornerx,leftCornery,x2,y2)    
    cnts = getTargetCntrs(img)
    approxes = []
    hulls = []
    for cnt in cnts:
        approxes.append(cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True))
        hulls.append(cv2.convexHull(cnt))
        left = list(cnt[cnt[:,:,0].argmin()][0])        
        right = list(cnt[cnt[:,:,0].argmax()][0])
        print 'left x' + str(left[0])+ 'y '+ str(left[1])
        print 'right x' + str(right[0])+ 'y '+ str(right[1])
        if right[0] - left[0] < 20:
            print 'Small diff ' + str(right[0] - left[0])
            continue
        center = round((right[0]+left[0])/2)
        center = int(center)
        moveMouse(center,left[1]+90)
        sleep(0.2,0.4)
        res = findHP(img);
        if res > 0:
            autoit.control_send(title, '', '{F1}', 0)
            sleep(0.1,0.4)
            return

        if (findFromTargeted(left, right)):
            autoit.mouse_click('left', center, left[1]+90)
            sleep(0.1,0.3)
            autoit.mouse_click('left', center, left[1]+90)
            return True
        # moveMouse(center,left[1]+70)
        # res = findHP(img);
        # if res > 0:
        #     autoit.control_send(title, '', '{F2}', 0)
        #     return
        # if (findFromTargeted(left, right)):
        #     autoit.mouse_click('left', center+10, left[1]+70)
        #     return True
    mouseRotate()

def findFromTargeted(left, right):
    template = cv2.imread('template_target2.png', 0)
    # print template.shape
    roi = getScreen(left[0]-70+leftCornerx, left[1]-15+leftCornery, right[0]+70+leftCornerx, right[1]+12+leftCornery)
    # roi2 = getScreen(left[0]+leftCornerx, left[1]+leftCornery, right[0]+leftCornerx, right[1]+leftCornery)
    # cv2.imwrite('roi' + str(int(time.time())) + '.png',roi)
    # cv2.imwrite('roi2' + str(int(time.time())) + '.png',roi2)
    roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    # roi = img[left[1]-8:right[1]+8, left[0]-25:right[0]];
    # for x in xrange(70,255):
    #     for j in xrange(20,200):
    #         ret,th1 = cv2.threshold(roi,x,255,cv2.THRESH_TOZERO_INV)
    #         ret,th2 = cv2.threshold(th1,j,255,cv2.THRESH_BINARY)
    #         if not hasattr(th2, 'shape'):
    #             pass
    #         else:
    #             ret,tp1 = cv2.threshold(template,x,255,cv2.THRESH_TOZERO_INV)
    #             ret,tp2 = cv2.threshold(tp1,j,255,cv2.THRESH_BINARY)
    #             wth, hth = th2.shape
    #             wtp, htp = tp2.shape
    #             if wth > wtp and hth > htp:
    #                 res = cv2.matchTemplate(th2, tp2, cv2.TM_CCORR_NORMED)
    #                 if (res.any()):
    #                     min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    #                     if (max_val > 0.95):
    #                         print 'x:' + str(x) + ' j:' + str(j)
    #                         print 'max_val %.2f'%max_val
    # bla()
    ret,th1 = cv2.threshold(roi,224,255,cv2.THRESH_TOZERO_INV)
    ret,th2 = cv2.threshold(th1,135,255,cv2.THRESH_BINARY)
    ret,tp1 = cv2.threshold(template,224,255,cv2.THRESH_TOZERO_INV)
    ret,tp2 = cv2.threshold(tp1,135,255,cv2.THRESH_BINARY)
    if not hasattr(th2, 'shape'):
        return False
    wth, hth = th2.shape
    wtp, htp = tp2.shape
    if wth > wtp and hth > htp:
        res = cv2.matchTemplate(th2, tp2, cv2.TM_CCORR_NORMED)
        if (res.any()):
            # cv2.imwrite('th2' + str(int(time.time())) + '.png',th2)
            # cv2.imwrite('tp2' + str(int(time.time())) + '.png',tp2)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            print 'mxv %.2f'%max_val
            if (max_val > 0.7):
                return True
            else:
                return False
    return False


def matchBuff(buffname, x, y):
    template = cv2.imread(buffname, 0)
    roi = getScreen(x, y, x+32, y+32)
    roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    # cv2.imshow('image',roi)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # bla()
    res = cv2.matchTemplate(roi, template, cv2.TM_CCORR_NORMED)
    if (res.any()):
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        print 'buffname %.2f'%max_val
        if (max_val > 0.98):
            return True
    print 'not any'
    return False

def grabHP():
    hp = getScreen(leftCornerx + 514,leftCornery + 16,leftCornerx + 668,leftCornery + 25)

    # img = cv2.imread('snap__1426174990.png')
    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # roi = gray[16:25, 958:1111];
    return hp


def findHP(img):
    statuses = {'none': -1, 'dead' : 0,  'lhalf' : 1, 'mhalf' : 2, 'full' : 3}
    # hpcolor = [231, 73, 132]
    hpcolor = [123, 8, 0]
    deadcolor = [49, 24, 16]
    hp = grabHP()
    # for y in xrange(0,10):
    #     px = hp[y, 150];
    #     print px
    #     px = hp[y, 140];
    #     print '140' + str(px) +' y' + str(y)

    # gray = cv2.cvtColor(hp, cv2.COLOR_BGR2GRAY)
    # for x in xrange(200,255):
    #     ret,pl = cv2.threshold(gray,x,255,cv2.THRESH_BINARY)
    #     cv2.imwrite('test\\th2_' + str(x) + '_' + str(int(time.time())) + '.png',pl)
    #     pass
    # bla()
    # ret,pl = cv2.threshold(gray,218,255,cv2.THRESH_TOZERO_INV)
    # ret,pl = cv2.threshold(pl,217,255,cv2.THRESH_BINARY)
    # (cntspl, hierarchy) = cv2.findContours(pl,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    # if (len(cntspl) > 0):
    #     print 'player'
    #     autoit.control_send(title, '', '{ESC}', 0)
    #     mouseRotate()
    #     pass

    # ret,th1 = cv2.threshold(gray,120,255,cv2.THRESH_TOZERO_INV)
    # ret,th1 = cv2.threshold(th1,100,255,cv2.THRESH_TOZERO)
    # cv2.imwrite('th1' + str(int(time.time())) + '.png',th1)
    hparr = array(hpcolor, dtype='uint8')
    mask = cv2.inRange(hp, hparr, hparr)

    (cnts, hierarchy) = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    if (len(cnts) == 0):
        deadarr = array(deadcolor, dtype='uint8')
        mask = cv2.inRange(hp, deadarr, deadarr)
        (cnts, hierarchy) = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        if (len(cnts) > 0):
            return statuses['dead']
        else:
            return statuses['none']

    leftx = list(cnts[0][cnts[0][:,:,0].argmin()][0])[0]
    rightx = list(cnts[0][cnts[0][:,:,0].argmax()][0])[0]
    diff = rightx - leftx
    if diff > 140:
        return statuses['full']
    if diff >= 75:
        return statuses['mhalf']
    if diff < 75 and diff > 0:
        return statuses['lhalf']
    return statuses['dead']

def moveMouse(x,y):
    autoit.mouse_move(x,y,3)

def sleep(a,b):
    time.sleep(random.uniform(a, b))
    return True

def mouseRotate():
    autoit.mouse_move(655, 521)
    sleep(0.2, 0.6)
    autoit.mouse_down('right')
    autoit.mouse_move(670, 521)
    autoit.mouse_up('right')

def checkOwnCp():
    statuses = {'dead' : 0,  'lhalf' : 1, 'mhalf' : 2, 'full': 3}
    cpCord = (24, 57, 175, 69)
    cpcolor = [140,117,90]
    cp = ImageGrab.grab(cpCord)
    imgCP =  array(cp.getdata(),dtype=uint8).reshape((cp.size[1],cp.size[0],3))
    # for x in xrange(145,150):
    #     for y in xrange(0,5):
    #         px = imgCP[y, x];
    #         print str(px) + ' - ' + str(x) + ' ' + str(y)
    # fghjfghfg
    # gray = cv2.cvtColor(imgCP, cv2.COLOR_BGR2GRAY)
    # ret,th1 = cv2.threshold(gray,120,255,cv2.THRESH_TOZERO_INV)
    # ret,th1 = cv2.threshold(th1,100,255,cv2.THRESH_TOZERO)
    cparr = array(cpcolor, dtype='uint8')
    mask = cv2.inRange(imgCP, cparr, cparr)
    # cv2.imshow('image',mask)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # sdfsd

    (cnts, hierarchy) = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    if (len(cnts) == 0):
        winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
        return statuses['dead']
    left = list(cnts[0][cnts[0][:,:,0].argmin()][0])
    right = list(cnts[0][cnts[0][:,:,0].argmax()][0])
    diff = right[0] - left[0]
    if diff > 145:
        return statuses['full']
    if diff >= 90 and diff < 145:
        return statuses['mhalf']
    if diff < 90:
        return statuses['lhalf']

def checkOwnHp():
    statuses = {'verylow' : -1, 'dead' : 0,  'lhalf' : 1, 'mhalf' : 2, 'full': 3}
    hpcolor = [140,97,90]
    hpdeadcolor = [57,44,41]
    hpCord = (24, 71, 175, 84)
    hp = ImageGrab.grab(hpCord)
    imgHP =  array(hp.getdata(),dtype=uint8).reshape((hp.size[1],hp.size[0],3))
    px = imgHP[4, 28];
    if (px == hpdeadcolor).all():
        return statuses['verylow']
    px = imgHP[4, 5];
    if (px == hpdeadcolor).all():
        winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
        return statuses['dead']
    # for x in xrange(80,150):
    #     for y in xrange(2,5):
    #         px = imgHP[y, x];
    #         print str(px) + ' - ' + str(x) + ' ' + str(y)
    # fghjfghfg
    hparr = array(hpcolor, dtype='uint8')
    mask = cv2.inRange(imgHP, hparr, hparr)
    # cv2.imshow('image',mask)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # sdfsd
    # cv2.imshow('image',th1)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    (cnts, hierarchy) = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    if (len(cnts) == 0):
        return statuses['lhalf'];

    left = list(cnts[0][cnts[0][:,:,0].argmin()][0])
    right = list(cnts[0][cnts[0][:,:,0].argmax()][0])
    diff = right[0] - left[0]
    # print 'hpdiff ' + str(diff)
    if diff >= 90:
        return statuses['mhalf']
    if diff < 90:
        return statuses['lhalf']

def checkOwnMp():
    statuses = {'none': 0, 'less': 1,  'lhalf': 2, 'mhalf': 3}
    mpcolor = [82,109,148]
    mpCord = (24, 83, 175, 97)
    mp = ImageGrab.grab(mpCord)
    imgmp =  array(mp.getdata(),dtype=uint8).reshape((mp.size[1],mp.size[0],3))
    # for y in xrange(0,10):
    #     px = imgmp[y, 3];
    #     print px
    mparr = array(mpcolor, dtype='uint8')
    mask = cv2.inRange(imgmp, mparr, mparr)
    # cv2.imshow('image',mask)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # dsfgdf
    (cnts, hierarchy) = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    if (len(cnts) == 0):
        return statuses['none']

    left = list(cnts[0][cnts[0][:,:,0].argmin()][0])
    right = list(cnts[0][cnts[0][:,:,0].argmax()][0])
    diff = right[0] - left[0]
    # print 'mpdiff ' + str(diff)
    if diff >= 100:
        return statuses['mhalf']
    if diff > 60 and diff < 100:
        return statuses['lhalf']
    if diff < 60:
        return statuses['less']

def restoreMenyHp():
    template = cv2.imread('template_button.png', 0)
    cycle = True
    while cycle:
        autoit.mouse_click('left', 1365, 983)
        sleep(0.3,0.7)
        autoit.mouse_click('left', 1250, 704)
        sleep(0.6,0.7)
        button = getScreen(540, 170, 675, 220)
        button = cv2.cvtColor(button, cv2.COLOR_BGR2GRAY)
        res = cv2.matchTemplate(button, template, cv2.TM_CCORR_NORMED)
        if (res.any()):
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            print 'menuval %.2f'%max_val
            if (max_val > 0.9):
                autoit.mouse_click('left', 606, 189)
                sleep(0.3,0.7)
                autoit.mouse_click('left', 729, 322)
                sleep(0.4,0.9)
                autoit.mouse_click('left', 1043, 92)
                sleep(0.4,0.9)
                autoit.mouse_click('left', 1378, 670)
                cycle = False
        else:
            autoit.mouse_click('left', 1043, 92)
            sleep(0.4,0.9)
            autoit.mouse_click('left', 1378, 670)            
