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
    x2 = 1400
    y2 = 870
    title = "[TITLE:Lineage II]"

    def getScreen(sefl, x1, y1, x2, y2):
        box = (x1, y1, x2, y2)
        screen = ImageGrab.grab(box)
        img =  array(screen.getdata(),dtype=uint8).reshape((screen.size[1],screen.size[0],3))
        # img = cv2.imread('test2.png')
        # img = img[y1:y2, x1:x2]
        return img

    def findTarget(self):
        img = self.getScreen(self.leftCornerx,self.leftCornery,self.x2,self.y2)
        cv2.rectangle(img, (582, 407), (1100, 750), [0, 0, 0], -1)
        cv2.rectangle(img, (0, 0), (520, 77), [0, 0, 0], -1)
        # cv2.imshow("images", img)
        # cv2.waitKey(0)
        # bla()
        colorMin = [255, 131, 86]
        colorMax = [255, 167, 108]
        mask = cv2.inRange(img, array(colorMin, dtype='uint8'), array(colorMax, dtype='uint8'))
        mask = cv2.filter2D(mask,-1, ones((5,5), float32))
        (cnts, hierarchy) = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        colorMin = [166, 228, 154]
        colorMax = [169, 232, 156]
        mask = cv2.inRange(img, array(colorMin, dtype='uint8'), array(colorMax, dtype='uint8'))
        mask = cv2.filter2D(mask,-1, ones((15,15), float32))
        (cnts, hierarchy) = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        cnts = sorted(cnts, key=lambda cnt: self.contourHeight(cnt), reverse=True);        
        # cv2.drawContours(img, cnts, -1, (255,0,0), 3)
        # cv2.imshow("images", img)
        # cv2.waitKey(0)
        # bla()
        for cnt in cnts:
            x,y,w,h = cv2.boundingRect(cnt)
            left = list(cnt[cnt[:,:,0].argmin()][0])        
            right = list(cnt[cnt[:,:,0].argmax()][0])
            print 'left x' + str(left[0])+ 'y '+ str(left[1])
            print 'right x' + str(right[0])+ 'y '+ str(right[1])
            if right[0] - left[0] < 20:
                print 'Small diff ' + str(right[0] - left[0])
                continue
            x,y,w,h = cv2.boundingRect(cnt)
            test = self.getScreen(x,y+h,x+w,y+200)
            cv2.imwrite('tgt/' + str(int(time.time())) + '_not_chmp.png',test)

            center = round((right[0]+left[0]+3)/2)
            center = int(center)
            self.moveMouse(center,left[1]+90)
            self.sleep(0.3,0.5)
            autoit.control_send(self.title, '', '{F3}', 0)
            res = self.findHP();
            if res > 0:
                autoit.control_send(self.title, '', '{F1}', 0)
                self.sleep(0.1,0.4)
                return

            if (self.findFromTargeted(left, right)):
                autoit.mouse_click('left', center, left[1]+90)
                self.sleep(0.1,0.3)
                autoit.mouse_click('left', center, left[1]+90)
                return True
        self.mouseRotate()

    def findFromTargeted(self, left, right):
        template = cv2.imread('target_template.png', 0)
        roi = self.getScreen(left[0]-70+self.leftCornerx, left[1]+self.leftCornery-10, right[0]+70+self.leftCornerx, right[1]+30+self.leftCornery)
        # cv2.imshow("images", roi)
        # cv2.waitKey(0)
        # bla()
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
                    cv2.imwrite('tgt/' + str(int(time.time())) + '_roitgt.png',roi)
                    return False
        return False


    def matchBuff(self, buffname):
        template = cv2.imread('buffs/' + buffname, 0)
        roi = self.getScreen(self.leftCornerx, self.leftCornery - 5, 600, 140)
        roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        res = cv2.matchTemplate(roi, template, cv2.TM_CCORR_NORMED)
        if (res.any()):
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            print buffname + '%.2f'%max_val
            if (max_val > 0.98):
                return True
        print 'not_buff '+ buffname
        return False

    def clickBuff(self, clickname):
        template = cv2.imread('buffs/' + clickname, 0)
        th, tw = template.shape[:2]
        roi = self.getScreen(352, 875, 865, 1063)
        # cv2.imshow("roi", roi)
        # cv2.waitKey(0)
        # bla()
        roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        res = cv2.matchTemplate(roi, template, cv2.TM_CCORR_NORMED)
        if (res.any()):
            min_val, max_val, min_loc, (x1,y1) = cv2.minMaxLoc(res)
            # roi2 = roi[y1:y1+th, x1:x1+tw]
            # print 352+x1
            # print 875+y1
            # cv2.imshow("2", roi)
            # cv2.waitKey(0)
            # bla()
            if (max_val > 0.98):
                autoit.mouse_click('left', 352+x1+int(round(tw/2)), 875+y1+int(round(th/2)))
                return True
        print 'not_click '+ clickname
        return False

    def grabHP(self):
        hp = self.getScreen(self.leftCornerx + 500,self.leftCornery + 15,self.leftCornerx + 700,self.leftCornery + 28)

        return hp


    def findHP(self):
        statuses = {'none': -1, 'dead' : 0,  'lhalf' : 1, 'mhalf' : 2, 'full' : 3}
        hpcolorMin = [111, 23, 18]
        hpcolorMax = [111, 23, 21]
        deadcolor = [46, 25, 23]
        deadcolorMin = array([41, 21, 21])
        deadcolorMax = array([53, 32, 30])
        hp = self.grabHP()

        mask = cv2.inRange(hp, array(hpcolorMin, dtype='uint8'), array(hpcolorMax, dtype='uint8'))
        mask = cv2.filter2D(mask,-1, ones((2,17), float32))

        (cnts, hierarchy) = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        # cv2.drawContours(hp, cnts, -1, (255,0,0), 3)
        # cv2.imshow("images", hp)
        # cv2.waitKey(0)
        # bla()
        if (len(cnts) == 0):
            # for y in range(0, 8):
            #     print hp[y, 28];
            # bla()
            mask = cv2.inRange(hp, deadcolorMin, deadcolorMax)
            mask = cv2.filter2D(mask,-1, ones((2,20), float32))
            (cnts2, hierarchy) = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            # cv2.drawContours(hp, cnts, -1, (255,0,0), 3)
            # cv2.imshow("images", hp)
            # cv2.waitKey(0)
            # bla()
            print 'LEN', len(cnts)
            if (len(cnts2) > 0):
                print 'DEAD'
                return statuses['dead']
            else:
                return statuses['none']

        leftx = list(cnts[0][cnts[0][:,:,0].argmin()][0])[0]
        rightx = list(cnts[0][cnts[0][:,:,0].argmax()][0])[0]
        diff = rightx - leftx
        print 'diff ', diff
        if diff > 147:
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

    def randClick(self, a, b, button):
        autoit.mouse_click(button, int(random.uniform(a+2, a-2)), int(random.uniform(b+2, b-2)))

    def mouseRotate(self):
        autoit.mouse_move(655, 521)
        self.sleep(0.2, 0.6)
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

    def checkOwnHp(self):
        statuses = {'verylow' : -1, 'dead' : 0,  'lhalf' : 1, 'mhalf' : 2, 'full': 3}
        hpcolor = [130, 87, 80]
        hpdeadcolor = [68,54,48]
        hpCord = (34 - self.leftCornerx, 104 - self.leftCornery, 190 - self.leftCornerx, 109 - self.leftCornery)
        hp = ImageGrab.grab(hpCord)
        imgHP =  array(hp.getdata(),dtype=uint8).reshape((hp.size[1],hp.size[0],3))
        # hparr = array(hpcolor, dtype='uint8')
        # mask = cv2.inRange(hp, hparr, hparr)
        # mask = cv2.filter2D(mask,-1, ones((2,17), float32))
        px = imgHP[2, 28];
        if (px == hpdeadcolor).all():
            return statuses['verylow']
        hparr = array(hpcolor, dtype='uint8')
        mask = cv2.inRange(imgHP, hparr, hparr)
        mask = cv2.filter2D(mask,-1, ones((2,17), float32))
        (cnts, hierarchy) = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        # cv2.drawContours(imgHP, cnts, -1, (255,0,0), 3)
        # cv2.imshow("images", imgHP)
        # cv2.waitKey(0)
        # bla()
        if (len(cnts) == 0):
            winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
            return statuses['dead']

        left = list(cnts[0][cnts[0][:,:,0].argmin()][0])
        right = list(cnts[0][cnts[0][:,:,0].argmax()][0])
        diff = right[0] - left[0]
        if diff >= 110:
            return statuses['mhalf']
        if diff < 110:
            return statuses['lhalf']

    def checkOwnMp(self):
        statuses = {'none': 0, 'less': 1,  'lhalf': 2, 'mhalf': 3}
        mpcolor = [76,98,136]
        mpCord = (20, 80, 185, 85)
        mp = ImageGrab.grab(mpCord)
        imgmp =  array(mp.getdata(),dtype=uint8).reshape((mp.size[1],mp.size[0],3))
        mparr = array(mpcolor, dtype='uint8')
        mask = cv2.inRange(imgmp, mparr, mparr)
        mask = cv2.filter2D(mask,-1, ones((2,17), float32))
        (cnts, hierarchy) = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        # cv2.drawContours(imgmp, cnts, -1, (255,0,0), 3)
        # cv2.imshow("images", imgmp)
        # cv2.waitKey(0)
        # bla()
        if (len(cnts) == 0):
            return statuses['none']

        left = list(cnts[0][cnts[0][:,:,0].argmin()][0])
        right = list(cnts[0][cnts[0][:,:,0].argmax()][0])
        diff = right[0] - left[0]
        print 'MP_DIFF ', diff
        if diff >= 100:
            return statuses['mhalf']
        if diff > 15 and diff < 100:
            return statuses['lhalf']
        if diff < 15:
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

    def contourHeight(self, cnt):
        x,y,w,h = cv2.boundingRect(cnt)
        img = self.getScreen(x,y+h,x+w,y+200)
        colorMin = [255, 131, 86]
        colorMax = [255, 167, 108]
        mask = cv2.inRange(img, array(colorMin, dtype='uint8'), array(colorMax, dtype='uint8'))
        mask = cv2.filter2D(mask,-1, ones((5,5), float32))
        (cnts, hierarchy) = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        if (not cnts):
            return y
        else:
            print "champ!!!"
            cv2.imwrite('tgt/' + str(int(time.time())) + '_chmp.png',img)
            return y*100

    def checkPetHp(self):
        statuses = {'verylow' : -1, 'dead' : 0,  'lhalf' : 1, 'mhalf' : 2, 'full': 3}
        hpcolor = [127, 70, 68]
        hpCord = (355, 748, 535, 800)
        hp = ImageGrab.grab(hpCord)
        imgHP =  array(hp.getdata(),dtype=uint8).reshape((hp.size[1],hp.size[0],3))
        if (px == hpdeadcolor).all():
            winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
            return statuses['dead']
        hparr = array(hpcolor, dtype='uint8')
        mask = cv2.inRange(imgHP, hparr, hparr)
        mask = cv2.filter2D(mask,-1, ones((2,17), float32))
        (cnts, hierarchy) = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        # cv2.drawContours(imgHP, cnts, -1, (255,0,0), 3)
        # cv2.imshow("images", imgHP)
        # cv2.waitKey(0)
        # bla()
        if (len(cnts) == 0):
            return statuses['dead'];

        left = list(cnts[0][cnts[0][:,:,0].argmin()][0])
        right = list(cnts[0][cnts[0][:,:,0].argmax()][0])
        diff = right[0] - left[0]
        if diff >= 80:
            return statuses['mhalf']
        if diff < 80:
            return statuses['lhalf']

    def checkSystemChatColor(self, colorMin, colorMax):
        systemChatCoord = (27, 751, 350, 870)
        grab = ImageGrab.grab(systemChatCoord)
        img =  array(grab.getdata(),dtype=uint8).reshape((grab.size[1],grab.size[0],3))
        mask = cv2.inRange(img, array(colorMin, dtype='uint8'), array(colorMax, dtype='uint8'))
        mask = cv2.filter2D(mask,-1, ones((2,30), float32))
        (cnts, hierarchy) = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        # cv2.drawContours(img, cnts, -1, (255,0,0), 3)
        # cv2.imshow("images", img)
        # cv2.waitKey(0)
        # bla()
        if (len(cnts) > 0):
            return 1

        return 0

    def findTemplate(self, templateName, dir):
        template = cv2.imread(dir + templateName, 0)
        roi = self.getScreen(self.leftCornerx,self.leftCornery,self.x2,self.y2)
        roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        res = cv2.matchTemplate(roi, template, cv2.TM_CCORR_NORMED)
        if (res.any()):
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            print templateName + '%.2f'%max_val
            if (max_val > 0.98):
                return (min_val, max_val, min_loc, max_loc)
        print 'not_match '+ templateName
        return False

    def clickTemplate(self, templateName, dir, mouse_btn):
        find = self.findTemplate(templateName, dir)
        if (find):
            min_val, max_val, min_loc, (x1,y1) = find
            print (find)
            # roi2 = roi[y1:y1+th, x1:x1+tw]
            # print 352+x1
            # print 875+y1
            # cv2.imshow("2", roi)
            # cv2.waitKey(0)
            # bla()
            autoit.mouse_click(mouse_btn, self.leftCornerx+x1+3, self.leftCornery+y1+3)
            return True
        print 'not_click '+ templateName
        return False