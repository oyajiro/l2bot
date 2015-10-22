from Bot import  *
import sys

def main():
    bot = Bot()
    autoit.win_wait(bot.title, 5)
    cycle = True
    colorMin = [160, 160, 5]
    colorMax = [237, 237, 30]
    cnt = 0
    found = 0
    temp = 0
    while cycle:
        if found == 0 and temp == 1: 
            autoit.control_send(bot.title, '', '{F4}', 0)
            bot.sleep(1,4)
            found = temp

            # systemChatCoord = (27, 751, 350, 870)
            # grab = ImageGrab.grab(systemChatCoord)
            # img =  array(grab.getdata(),dtype=uint8).reshape((grab.size[1],grab.size[0],3))
            # mask = cv2.inRange(img, array(colorMin, dtype='uint8'), array(colorMax, dtype='uint8'))
            # mask = cv2.filter2D(mask,-1, ones((2,30), float32))
            # (cnts, hierarchy) = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            # cv2.drawContours(img, cnts, -1, (255,0,0), 3)
            # cv2.imshow("images", img)
            # cv2.waitKey(0)
            # bla()

        if temp == 0:
            found = temp

        if cnt > 10 or found == 1:
            print found 
            cnt = 0
        cnt += 1
        bot.sleep(0.1,0.2)
        temp = bot.checkSystemChatColor(colorMin, colorMax)
    pass

main()