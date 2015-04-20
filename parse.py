import lxml.html as html
from pandas import DataFrame
import winsound
import time
import random

cycle = True
counter = 0
cabriocl = 'male'
hallatecl = 'male'
kernoncl = 'male'
golkondacl = 'male'
barakielcl = 'male'
while cycle:
    page = html.parse('http://www.l2aura.ru/index.php?f=stat&act=raid&sid=1').getroot()
    trs = page.cssselect('#l2top tr')
    # trs = table.cssselect('tr')
    for row in trs:
        spans = row.cssselect('td.name span')
        if spans:
            span = spans.pop()
            cl = span.get('class')
            currtime = str(time.strftime('%d %b %Y %H:%M:%S'))
            # if (span.text == 'Shilen\'s Messenger Cabrio'):
            #     if cl == cabriocl:
            #         print cabriocl + ' Cabrio ' + currtime
            #         winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
            #         winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
            #         winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
            #         f = open('bosses', 'a')
            #         f.write(cabriocl + ' Cabrio ' + currtime + '\n')
            #         f.close()
            #         if cabriocl == 'male':
            #             cabriocl = 'female'
            #         else:
            #             cabriocl = 'male'
            # if (span.text == 'Death Lord Hallate'):
            #     if cl == hallatecl:
            #         print hallatecl + ' Hallate ' + currtime
            #         winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
            #         winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
            #         winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
            #         f = open('bosses', 'a')
            #         f.write(hallatecl + ' Hallate ' + currtime + '\n')
            #         f.close()
            #         if hallatecl == 'male':
            #             hallatecl = 'female'
            #         else:
            #             hallatecl = 'male'
            # if (span.text == 'Kernon'):
            #     if cl == kernoncl:
            #         print kernoncl + ' Kernon ' + currtime
            #         winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
            #         winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
            #         winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
            #         f = open('bosses', 'a')
            #         f.write(kernoncl + ' Kernon ' + currtime + '\n')
            #         f.close()
            #         if kernoncl == 'male':
            #             kernoncl = 'female'
            #         else:
            #             kernoncl = 'male'
            # if (span.text == 'Longhorn Golkonda'):
            #     if cl == golkondacl:
            #         print golkondacl + ' Golkonda ' + currtime
            #         winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
            #         winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
            #         winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
            #         f = open('bosses', 'a')
            #         f.write(golkondacl + ' Golkonda ' + currtime + '\n')
            #         f.close()
            #         if golkondacl == 'male':
            #             golkondacl = 'female'
            #         else:
            #             golkondacl = 'male'
            if (span.text == 'Flame of Splendor Barakiel'):
                if cl == barakielcl:
                    print barakielcl + ' Barakiel ' + currtime
                    winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
                    winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
                    winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
                    f = open('bosses', 'a')
                    f.write(barakielcl + ' Barakiel ' + currtime + '\n')
                    f.close()
                    if barakielcl == 'male':
                        barakielcl = 'female'
                    else:
                        barakielcl = 'male'
    counter +=1
    if (counter % 10 == 0):
        print str(time.strftime('%H:%M:%S'))
        counter = 0
    time.sleep(random.uniform(50, 90))

    