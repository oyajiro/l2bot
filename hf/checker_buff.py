from Bot import  *
import sys

def main():
    bot = Bot()
    autoit.win_wait(bot.title, 5)
    cycle = True
    # print 'Argument:', str(sys.argv[1])
    while cycle:
        if not bot.matchBuff(str(sys.argv[1]) + '.png'):
            # bot.clickBuff(str(sys.argv[1]) + '_click.png')
            autoit.control_send(bot.title, '', '{F4}', 0)
        bot.sleep(20,40)
    pass

main()