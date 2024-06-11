import cv2
import time
import numpy as np
import module as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

wcam,hcam=1000,700
cap=cv2.VideoCapture(0)
ptime=0
cap.set(3,wcam)
cap.set(4,hcam)
detector=htm.HandDetector(min_detection_confidence=.8,min_tracking_confidence=.8)


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volrange=volume.GetVolumeRange()


volume.SetMasterVolumeLevel(0, None)
minvol=volrange[0]
maxvol=volrange[1]




volper=0
volbar=400
vol=0
#
while True:
    succes,frame=cap.read()
    frame1=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    frame1= detector.findhands(frame1)
    cv2.rectangle(frame, (20, 200), (50, 400), 3)

    lmlist=detector.findpos(frame1)
    if len(lmlist)!=0:
        # print(lmlist[4],lmlist[8])
        x1,y1=lmlist[4][1],lmlist[4][2]
        x2, y2 = lmlist[8][1], lmlist[8][2]
        cv2.circle(frame,(x1,y1),3,(0,0,0),cv2.FILLED)
        cv2.circle(frame, (x2, y2), 3, (0, 0, 0), cv2.FILLED)
        cv2.line(frame,(x1,y1),(x2,y2),(0,0,0),3)
        length=math.hypot(x2-x1,y2-y1)
        cx,cy=((x1+x2)//2,(y1+y2)//2)


        # print(length)
        vol=np.interp(length,[20,80],[minvol,maxvol])
        volbar = np.interp(length, [20, 80], [400, 200])
        volper = np.interp(length, [20, 80], [0,100])
        volume.SetMasterVolumeLevel(vol, None)

        # print(vol)
        if length<30:
            cv2.circle(frame, (cx,cy), 3, (0, 255, 0), cv2.FILLED)
        if length > 80:
            cv2.circle(frame, (cx, cy), 3, (0, 0,255), cv2.FILLED)
    cv2.rectangle(frame, (20, int(volbar)), (50, 400),(255,0,0), cv2.FILLED)
    cv2.putText(frame,f"{int(volper)}%",(25,430),cv2.FONT_HERSHEY_PLAIN,2,(255,0,0),2)
    ctime = time.time()
    fps = 1 / (ctime - ptime)
    ptime = ctime
    cv2.putText(frame, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
    cv2.imshow("Hand Tracking", frame)
    if cv2.waitKey(1) == ord("k"):
        break