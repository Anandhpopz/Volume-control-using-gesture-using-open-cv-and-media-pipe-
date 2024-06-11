import cv2
import mediapipe as mp
import time

class HandDetector():


    def __init__(self,static_image_mode=False,
               max_num_hands=2,
               model_complexity=1,
               min_detection_confidence=0.5,
               min_tracking_confidence=0.5):
        self.static_image_mode=static_image_mode
        self.max_num_hands =max_num_hands
        self.model_complexity =   model_complexity
        self.min_detection_confidence =min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence
        self.mpHands=mp.solutions.hands
        self.hands=self.mpHands.Hands(self.static_image_mode,self.max_num_hands,self.model_complexity,
                                      self.min_detection_confidence,self.min_tracking_confidence)
        self.mpdraw=mp.solutions.drawing_utils

    def findhands(self,frame,draw=True):

        imgrgb=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        self.result=self.hands.process(imgrgb)
        # print(result.multi_hand_landmarks)
        if self.result.multi_hand_landmarks:
          for hand in self.result.multi_hand_landmarks:
              if draw:
                self.mpdraw.draw_landmarks(frame,hand,self.mpHands.HAND_CONNECTIONS)
        return frame
    def findpos(self,frame,handno=0,draw=True,landmark_draw=0):
        lmlist = []

        if self.result.multi_hand_landmarks:
            myhand = self.result.multi_hand_landmarks[handno]
            for id, lm in enumerate(myhand.landmark):
                h, w, c = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmlist.append([id, cx, cy])
                if draw:
                    if id == landmark_draw:
                        cv2.circle(frame, (cx, cy), 10, (255, 255, 255), cv2.FILLED)

        return lmlist

# n=int(input("enter the land mark:"))
def main():
    cap = cv2.VideoCapture(0)
    ptime = 0
    detector=HandDetector()

    while True:
        sucess, frame = cap.read()
        img=detector.findhands(frame,draw=True)


        lmlist=detector.findpos(img,landmark_draw=0)

        if len(lmlist)!=0:
            print(lmlist[0])

        ctime = time.time()
        fps = 1 / (ctime - ptime)
        ptime = ctime
        cv2.putText(frame, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        cv2.imshow("Hand Tracking", frame)
        if cv2.waitKey(1) == ord("k"):
            break
if __name__=="__main__":
    main()