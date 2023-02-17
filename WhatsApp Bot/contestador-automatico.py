import pyautogui as pt 
from time import sleep

while True:
    posXY = pt.position()
    print(posXY, pt.pixel(posXY[0], posXY[1]))
    sleep(1)
    if posXY[0] == 0:
        break

''' pip install opencv-python '''
''' pip install "PyMsgBox==1.0.7" '''
''' pip install "PyScreeze==0.1.26 '''
''' pip install pyautogui '''