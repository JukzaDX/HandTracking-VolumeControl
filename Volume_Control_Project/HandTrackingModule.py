import cv2
import math
import mediapipe as np

class handDetector():
    def __init__(self,mode=False,maxHands=1,mode1Comp1exity=1,detectionCon=0.5,trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.mode1Complex = mode1Comp1exity
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = np.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.mode1Complex, self.detectionCon, self.trackCon)

        self.npDraw=np.solutions.drawing_utils
        self.tipIds=[4,8,12,16,20]

    def findHands(self,img,draw=True):

        imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results=self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLMS in self.results.multi_hand_landmarks:
                if draw:
                    self.npDraw.draw_landmarks(img,handLMS,self.mpHands.HAND_CONNECTIONS)

        return img
#
    def findPosition(self,img,handNo=0,draw=True):
        xList=[]
        yList=[]
        bbox=[]
        self.Imlist=[]

        if self.results.multi_hand_landmarks:
            myhand=self.results.multi_hand_landmarks[handNo]
            for id,Im in enumerate(myhand.landmark):
                h,w,c=img.shape
                cx,cy=int(Im.x*w),int(Im.y*h)
                xList.append(cx)
                yList.append(cy)
                self.Imlist.append([id,cx,cy])

                if draw:
                    cv2.circle(img,[cx,cy],7,(255,0,255),cv2.FILLED)
            Xmin,Xmax=min(xList),max(xList)
            Ymin,Ymax=min(yList),max(yList)
            bbox=Xmin,Ymin,Xmax,Ymax

            if draw:
                cv2.rectangle(img[bbox[0],bbox[1]],[bbox[2],bbox[1]],(0,255,0),2)
        return self.Imlist, bbox

    def fingersup(self):
        finger=[]

        if self.Imlist != []:
            if self.Imlist[self.tipIds[0]] [1] <self.Imlist[self.tipIds[0]-1][1]:
                finger.append(0)
            else:
                finger.append(1)

            for id in range(1,5):
                if self.Imlist[self.tipIds[id]][2] < self.Imlist[self.tipIds[id]-2][2]:
                    finger.append(1)
                else:
                    finger.append(0)
            return finger

    def distance(self,img,Top_1,Top_2,draw=True):
        x1,y1 = self.Imlist[0][Top_1][1:]
        x2,y2 = self.Imlist[0][Top_2][1:]

        cx,cy = (x1+x2)//2 , (y1+y2)//2

        length = math.hypot(x1-x2,y1-y2)

        if draw:
            cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.circle(img,(cx,cy),7,(0,0,255),cv2.FILLED)

        return length, img, [x1,y1,x2,y2,cx,cy]
