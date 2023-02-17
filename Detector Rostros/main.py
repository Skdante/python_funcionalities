import cv2

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(0)
'''cap = cv2.VideoCapture('video2.avi')'''

while True:
    _, img = cap.read();
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
    cv2.imshow('img', img)
    k = cv2.waitKey(30)
    if k == 27: 
        break;
cap.release()
        
'''1.-  pip install opencv-python'''
'''https://github.com/opencv/opencv/tree/master/data/haarcascades'''
'''https://github.com/andrewssobral/vehicle_detection_haarcascades'''
'''https://www.youtube.com/watch?v=kUMjVo25kX0&list=WL&index=11'''