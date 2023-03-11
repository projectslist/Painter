import cv2
import numpy as np
import time
import os
import pyautogui
from cvzone.HandTrackingModule import HandDetector
from cvzone.HandTrackingModule import HandDetector as htm

folderPath = "Headers"

myList = os.listdir(folderPath)

overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)



header = overlayList[4]


cap =cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)
detector = HandDetector(detectionCon=0.85)
drawColor = (106, 255, 0)
xp,yp = 0,0
imgcanvas = np.zeros((720,1280,3),np.uint8)
while True:
    success, img = cap.read()

    #For left to left and right to right
    img = cv2.flip(img,1)
    lmList, bboxInfo = detector.findHands(img)
    hand = detector.findHands(img, draw=False)
    fing = cv2.imread("Put image path with 0 fingures up")
    if hand:

        # Taking the landmarks of hand
        lmlist = hand[0]
        if lmlist:
            x1,y1 = lmList[0]['lmList'][8][:2]
            x2,y2 = lmList[0]['lmList'][12][:2]

            # Find how many fingers are up
            fingerup = detector.fingersUp(lmlist)

            if fingerup[1] and fingerup[2]:
                if y1 < 100:
                    if 110 < x1 < 310:
                        header = overlayList[4]
                        shape = 'freestyle'
                        drawColor = (106, 255, 0)
                    elif 320 < x1 < 520:
                        header = overlayList[2]
                        shape = 'freestyle'
                        drawColor = (0, 0, 255)
                    elif 720 < x1 < 920:
                        header = overlayList[3]
                        shape = 'freestyle'
                        drawColor = (225, 155, 0)
                    elif 1120 < x1 < 1280:
                        header = overlayList[1]
                        shape = 'freestyle'
                        drawColor = (0, 0, 0)

                print('selection mode')


            if fingerup[1] and fingerup[2 ]  == False:

              if xp==0 and yp==0:
                  xp,yp = x1,y1
              if drawColor == (0,0,0):
                  cv2.line(img,(xp,yp),(x1,y1),drawColor,50)
                  cv2.line(imgcanvas, (xp, yp), (x1, y1), drawColor, 50)
              else:

                cv2.line(img,(xp,yp),(x1,y1),drawColor,10)
                cv2.line(imgcanvas, (xp, yp), (x1, y1), drawColor, 10)
            xp, yp = x1, y1

    img[0:210, 0:1280] = header

    img_gray = cv2.cvtColor(imgcanvas,cv2.COLOR_BGR2GRAY)
    _,imginv = cv2.threshold(img_gray,50,255,cv2.THRESH_BINARY_INV)
    imginv = cv2.cvtColor(imginv,cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img,imginv)
    img = cv2.bitwise_or(img,imgcanvas)


    cv2.imshow('Virtual Painter', img)

    cv2.waitKey(1)
