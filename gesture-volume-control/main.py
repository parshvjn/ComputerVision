import math
from subprocess import call
import cv2,time,numpy as np, HandTrackingModule as htm

#########################
wCam, hCam = 1280, 720
#########################

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

detector = htm.handDetector(detectionCon=0.7)# default detection confidence is 0.5 so we change to 0.7 so it doesn't flicker too much. it has to be more confident about detecting a hand.


minVol = 0
maxVol = 100

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw = False)
    # print(lmList)
    if len(lmList) != 0:
        # print(lmList)
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1+x2)//2, (y1+y2)//2

        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        length = math.hypot(x2 - x1, y2- y1)
        # print(length)

        #Hand Range: 50 - 300
        #Volume Range: 0 - 100
        vol = np.interp(length, [50, 170], [minVol, maxVol])
        # print(length)
        volString = "osascript -e 'set volume output volume {}'".format(vol)
        call(volString, shell=True)

        if length<50:
            cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)


    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    text = "FPS: " + str(int(fps))
    cv2.putText(img, text, (40,50), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0), 3)

    cv2.imshow("Img", img)

    cv2.waitKey(1)