from Bot import  *
import sys

def main():
    bot = Bot()
    autoit.win_wait(bot.title, 5)
    enchx = 1010
    ecnhy = 684
    cycle = True
    bot.sleep(3,5)
    print 'Count:', str(sys.argv[1])
    print 'X:', str(sys.argv[2])
    print 'Y:', str(sys.argv[3])
    count = sys.argv[1]
    x = sys.argv[2]
    y = sys.argv[3]
    while i <= count:
        bot.randClick(x, y, 'right')


    pass

main()