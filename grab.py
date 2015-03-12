from PIL import ImageGrab
import os
import time
leftCornerx = 7
leftCornery = 38
x1 = leftCornerx
y1 = leftCornery
x2 = 1390
y2 = 1000
 
def screenGrab(x1, y1, x2, y2):
    box = (x1,y1,x2,y2)
    im = ImageGrab.grab(box)
    im.save(os.getcwd() + '\\snap__' + str(int(time.time())) + '.png', 'PNG')
 
def main():
    screenGrab(leftCornerx,leftCornery,x2,y2)
 
if __name__ == '__main__':
    main()