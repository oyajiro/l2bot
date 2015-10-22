from Bot import  *
import sys

def main():
    bot = Bot()
    autoit.win_wait(bot.title, 5)
    cycle = True
    while cycle:
        mp = bot.checkOwnMp();
        print mp
        if mp < 2:
            autoit.control_send(bot.title, '', '{F11}', 0)
        bot.sleep(10,30)
    pass

main()