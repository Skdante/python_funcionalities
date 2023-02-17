import pyautogui as pg, webbrowser as web, time as tm

web.open('https://web.whatsapp.com/send?phone=+529983146667')
tm.sleep(5);

pg.write("Hola, que tal BB!")
pg.press("enter")

web.close()

'''f = open('texto.txt','r')

for word in f:
    pg.typewrite(word)
    pg.press("enter")
'''

''' pip install "PyMsgBox==1.0.7" '''
''' pip install "PyScreeze==0.1.26 '''
''' pip install pyautogui '''