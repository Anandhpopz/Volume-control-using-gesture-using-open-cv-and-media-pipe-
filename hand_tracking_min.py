import cv2
import mediapipe as mp
import time

ptime = 0
cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpdraw = mp.solutions.drawing_utils
while True:
    sucess, frame = cap.read()
    imgrgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(imgrgb)
    print(result.multi_hand_landmarks)
    if result.multi_hand_landmarks:
        for hand in result.multi_hand_landmarks:
            for id, lm in enumerate(hand.landmark):
                h, w, c = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                if id == 0:
                    cv2.circle(frame, (cx, cy), 10, (255, 255, 255), cv2.FILLED)

            mpdraw.draw_landmarks(frame, hand, mpHands.HAND_CONNECTIONS)
    ctime = time.time()
    fps = 1 / (ctime - ptime)
    ptime = ctime
    cv2.putText(frame, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
    cv2.imshow("Hand Tracking", frame)
    if cv2.waitKey(1) == ord("k"):
        break
