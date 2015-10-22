from Bot import  *
import sys

def main():
    bot = Bot()
    autoit.win_wait(bot.title, 5)
    counter = 0
    poitonUse = 0
    cycle = True
    bot.sleep(3,5)
    bigsleep = round(random.uniform(10, 50))
    print 'Argument:', str(sys.argv[1])
    while cycle:
        bot.randClick(1444, 724, 'right')
        bot.sleep(1,1.5)
        counter += 1
        if counter >= int(sys.argv[1]):
            cycle = False
        print str(counter) + " bgs(" + str(bigsleep) + ")"
        if counter % bigsleep == 0:
            bot.sleep(1,2)
            bigsleep = round(random.uniform(10, 50))

    pass

main()