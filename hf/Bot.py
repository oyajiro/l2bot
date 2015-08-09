import win32api, win32con, ctypes, autoit
from PIL import ImageOps, Image, ImageGrab
from numpy import *
import os
import time
import cv2
import random
import winsound
class Bot:

    leftCornerx = 7
    leftCornery = 38
    x2 = 1661
    y2 = 360
    title = "[CLASS:l2UnrealWWindowsViewportWindow]"

    def getScreen(sefl, x1, y1, x2, y2):
        box = (x1, y1, x2, y2)
        screen = ImageGrab.grab(box)
        img =  array(screen.getdata(),dtype=uint8).reshape((screen.size[1],screen.size[0],3))
        img = cv2.imread('test2.png')
        img = img[y1:y2, x1:x2]
        return img

    def findTarget(self):
        img = self.getScreen(self.leftCornerx,self.leftCornery,self.x2,self.y2)
        targetColor = [154, 228, 166]
        arr = array(targetColor, dtype='uint8')
        mask = cv2.inRange(img, arr, arr)
        mask = cv2.filter2D(mask,-1, ones((15,15), float32))
        (cnts, hierarchy) = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
                
        # cv2.drawContours(img, cnts, -1, (255,0,0), 3)
        # cv2.imshow("images", img)
        # cv2.waitKey(0)
        # bla()
        for cnt in cnts:
            left = list(cnt[cnt[:,:,0].argmin()][0])        
            right = list(cnt[cnt[:,:,0].argmax()][0])
            print 'left x' + str(left[0])+ 'y '+ str(left[1])
            print 'right x' + str(right[0])+ 'y '+ str(right[1])
            if right[0] - left[0] < 20:
                print 'Small diff ' + str(right[0] - left[0])
                continue
            center = round((right[0]+left[0])/2)
            center = int(center)
            self.moveMouse(center,left[1]+90)
            self.sleep(0.2,0.4)
            res = self.findHP(img);
            if res > 0:
                autoit.control_send(self.title, '', '{F1}', 0)
                self.sleep(0.1,0.4)
                return

            if (findFromTargeted(left, right)):
                autoit.mouse_click('left', center, left[1]+90)
                self.sleep(0.1,0.3)
                autoit.mouse_click('left', center, left[1]+90)
                return True
        mouseRotate()

    def findFromTargeted(left, right):
        template = cv2.imread('template_target2.png', 0)
        roi = getScreen(left[0]-70+self.leftCornerx, left[1]-15+self.leftCornery, right[0]+70+self.leftCornerx, right[1]+12+self.leftCornery)
        roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
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
        res = cv2.matchTemplate(roi, template, cv2.TM_CCORR_NORMED)
        if (res.any()):
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            print 'buffname %.2f'%max_val
            if (max_val > 0.98):
                return True
        print 'not any'
        return False

    def grabHP(self):
        hp = self.getScreen(self.leftCornerx + 520,self.leftCornery + 16,self.leftCornerx + 675,self.leftCornery + 25)

        return hp


    def findHP(self, img):
        statuses = {'none': -1, 'dead' : 0,  'lhalf' : 1, 'mhalf' : 2, 'full' : 3}
        hpcolorMin = [18, 23, 111]
        hpcolorMax = [21, 23, 111]
        deadcolor = [58, 57, 68]
        hp = self.grabHP()

        mask = cv2.inRange(hp, array(hpcolorMin, dtype='uint8'), array(hpcolorMax, dtype='uint8'))
        mask = cv2.filter2D(mask,-1, ones((2,17), float32))

        (cnts, hierarchy) = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        # cv2.drawContours(hp, cnts, -1, (255,0,0), 3)
        # cv2.imshow("images", hp)
        # cv2.waitKey(0)
        # bla()
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

    def moveMouse(self, x, y):
        autoit.mouse_move(x,y,3)

    def sleep(self, a, b):
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
        cparr = array(cpcolor, dtype='uint8')
        mask = cv2.inRange(imgCP, cparr, cparr)

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
        hpcolor = [80, 87, 130]
        hpdeadcolor = [57,44,41]
        hpCord = (24, 71, 175, 84)
        hp = ImageGrab.grab(hpCord)
        imgHP =  array(hp.getdata(),dtype=uint8).reshape((hp.size[1],hp.size[0],3))
        # hparr = array(hpcolor, dtype='uint8')
        # mask = cv2.inRange(hp, hparr, hparr)
        # mask = cv2.filter2D(mask,-1, ones((2,17), float32))
        px = imgHP[4, 28];
        if (px == hpdeadcolor).all():
            return statuses['verylow']
        px = imgHP[4, 5];
        if (px == hpdeadcolor).all():
            winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
            return statuses['dead']
        hparr = array(hpcolor, dtype='uint8')
        mask = cv2.inRange(imgHP, hparr, hparr)
        (cnts, hierarchy) = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

        if (len(cnts) == 0):
            return statuses['lhalf'];

        left = list(cnts[0][cnts[0][:,:,0].argmin()][0])
        right = list(cnts[0][cnts[0][:,:,0].argmax()][0])
        diff = right[0] - left[0]
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
        mparr = array(mpcolor, dtype='uint8')
        mask = cv2.inRange(imgmp, mparr, mparr)
        (cnts, hierarchy) = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

        if (len(cnts) == 0):
            return statuses['none']

        left = list(cnts[0][cnts[0][:,:,0].argmin()][0])
        right = list(cnts[0][cnts[0][:,:,0].argmax()][0])
        diff = right[0] - left[0]
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