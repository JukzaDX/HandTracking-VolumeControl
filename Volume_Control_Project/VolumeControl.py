import cv2
import time
import HandTrackingModule as htm
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
import math
import numpy as np

wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)

cap.set(3,wCam)
cap.set(4,hCam)
pTime = 0

detector = htm.handDetector(detectionCon=0.7)
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_,CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

volrange = volume.GetVolumeRange()
minvol = volrange[0]
maxvol = volrange[1]
vol = 0
volbar = 400
volper = 0

while True:
    success, img = cap.read()

    img = detector.findHands(img)
    ImList = detector.findPosition(img, draw=False)

    if ImList !=([],[]):
        x1, y1 = ImList[0][4][1], ImList[0][4][2]
        x2, y2 = ImList[0][12][1], ImList[0][12][2]
        cx,cy = (x1+x2) // 2, (y1+y2) // 2

        cv2.circle(img, (x1,y1), 15, (157,0,63), cv2.FILLED)
        cv2.circle(img, (x2,y2), 15, (157,0,63), cv2.FILLED)

        cv2.line(img, (x1,y1), (x2,y2), (157,0,63), 3)
        cv2.circle(img, (cx,cy), 15, (157,0,63), cv2.FILLED)

        length = math.hypot(x2-x1, y2-y1)

        vol = np.interp(length,[50,300], [minvol,maxvol])
        volbar = np.interp(length,[50,300],[400,150])
        volPer = np.interp(length,[50,300],[0,100])

        volume.SetMasterVolumeLevel(vol, None)
        print("length: "+ str(length)+",vol: "+ str(vol))

        if length < 50:
            cv2.circle(img, (cx,cy), 15, (0,255,0), cv2.FILLED)

    cTime = time.time()
    fps = 1 / (cTime-pTime)
    pTime = cTime

    cv2.rectangle(img,(50,150),(85,400),(255,0,0),3)
    cv2.rectangle(img,(50,int(volbar)),(85,400),(255,0,0),cv2.FILLED)

    cv2.putText(img,"FPS: "+str(int(fps)),(40,50),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),3)

    cv2.imshow("Gesture Volume Control", img)

    k=cv2.waitKey(1)
    if k%256 == 27:
        print("Escape hit, closing...")
        break


cap.release()
cv2.destroyAllWindows()
