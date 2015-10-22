from Bot import  *
import sys

def main():
    bot = Bot()
    autoit.win_wait(bot.title, 5)
    item = 'vorpal_llg.png'
    stone = 'fire_stone.png'
    button = 'confirm.png'
    cycle = True
    while cycle:
        bot.clickTemplate(stone, 'items/', 'right')
        bot.sleep(0.3, 0.5)
        bot.clickTemplate(item, 'items/', 'left')
        bot.sleep(0.3, 0.5)
        bot.clickTemplate(button, 'buttons/', 'left')
        bot.sleep(3,5)
    pass

main()