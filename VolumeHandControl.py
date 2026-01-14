import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL

########################################
wCam, hCam = 640, 480
########################################

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

pTime = 0
detector = htm.HandDetector()

# Audio setup
device = AudioUtilities.GetSpeakers()
volume = device.EndpointVolume
minVol, maxVol, _ = volume.GetVolumeRange()

# States
showSkeleton = False
volumeMode = False
numberMode = False

numberCooldown = 0
gestureCooldown = 0
volumeCooldown = 0

########################################
def countFingers(lm):
    fingers = 0

    # Index
    if lm[8][2] < lm[6][2]:
        fingers += 1
    # Middle
    if lm[12][2] < lm[10][2]:
        fingers += 1
    # Ring
    if lm[16][2] < lm[14][2]:
        fingers += 1
    # Pinky
    if lm[20][2] < lm[18][2]:
        fingers += 1

    # Thumb — distance based (NO left/right confusion)
    thumb_dist = math.hypot(
        lm[4][1] - lm[2][1],
        lm[4][2] - lm[2][2]
    )

    # Count thumb ONLY if other fingers are open
    if fingers == 4 and thumb_dist > 40:
        fingers = 5

    return fingers

########################################

while True:
    success, img = cap.read()
    img = detector.findHands(img, draw=showSkeleton)

    allHands = []
    if detector.results.multi_hand_landmarks:
        for i in range(len(detector.results.multi_hand_landmarks)):
            lm = detector.findPosition(img, handNo=i, draw=False)
            allHands.append((detector.handTypes[i], lm))

    # ---------- NUMBER MODE TOGGLE (thumb + pinky) ----------
    if numberCooldown == 0:
        for _, lm in allHands:
            tx, ty = lm[4][1], lm[4][2]
            px, py = lm[20][1], lm[20][2]

            if math.hypot(px - tx, py - ty) < 25:
                numberMode = not numberMode
                numberCooldown = 20
                break

    if numberCooldown > 0:
        numberCooldown -= 1

    # ---------- NUMBER MODE (two-hand counting) ----------
    if numberMode:
        for handType, lm in allHands:
            count = countFingers(lm)

            # Position: above middle finger (tip = 12, MCP = 9)
            x = lm[12][1]
            y = lm[12][2] - 40  # above finger

            # Number mapping
            if handType == "Right":
                displayNum = count            # 1–5
            else:
                displayNum = count + 5        # 6–10

            cv2.putText(img,str(displayNum),(x - 10, y),cv2.FONT_HERSHEY_SIMPLEX,1.0,(255, 0, 0),2)



        if numberMode:
            leftCount = 0
            rightCount = 0

            for handType, lm in allHands:
                if handType == "Left":
                    leftCount = countFingers(lm )
                elif handType == "Right":
                    rightCount = countFingers(lm)

            number = leftCount + rightCount



            # 🔴 ADD THIS BLOCK BELOW (DO NOT INDENT MORE)
            cTime = time.time()
            fps = int(1 / (cTime - pTime)) if cTime != pTime else 0
            pTime = cTime

            cv2.putText(
                img,
                f'FPS: {fps}',
                (10, 70),
                cv2.FONT_HERSHEY_PLAIN,
                3,
                (255, 0, 0),
                3
            )

            cv2.imshow("Image", img)
            cv2.waitKey(1)
            continue



    # ---------- VOLUME MODE ----------
    if not numberMode and len(allHands) > 0:
        _, lm = allHands[0]

        x1, y1 = lm[4][1], lm[4][2]   # Thumb
        x2, y2 = lm[8][1], lm[8][2]   # Index

        length = math.hypot(x2 - x1, y2 - y1)

        if volumeMode:
            vol = np.interp(length, [30, 100], [minVol, maxVol])
            volPercent = int(np.interp(length, [30, 100], [0, 100]))
            volume.SetMasterVolumeLevel(vol, None)

            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
            cv2.line(img, (x1, y1), (x2, y2), (200, 200, 200), 3)
            cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)

            cv2.putText(
                img,
                f"Volume {volPercent}%",
                (cx - 30, cy - 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

        # Toggle volume mode (thumb + ring)
        rx, ry = lm[16][1], lm[16][2]
        if volumeCooldown == 0 and math.hypot(rx - x1, ry - y1) < 25:
            volumeMode = not volumeMode
            volumeCooldown = 20
        
        mx, my = lm[12][1], lm[12][2]
        if gestureCooldown == 0 and math.hypot(mx - x1, my - y1) < 25:
            showSkeleton = not showSkeleton
            gestureCooldown = 20

    if volumeCooldown > 0:
        volumeCooldown -= 1
    
    if gestureCooldown > 0:
        gestureCooldown -= 1


    # ---------- FPS ----------
    cTime = time.time()
    fps = int(1 / (cTime - pTime)) if cTime != pTime else 0
    pTime = cTime

    cv2.putText(img, f'FPS: {fps}', (10, 70),
                cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)

cap.release()
cv2.destroyAllWindows()
