import cv2
import mediapipe as mp
import time

class HandDetector():
    def __init__(self, max_num_hands=2,mode=False,detectionCon=0.5,trackCon=0.5):
        self.mode=mode
        self.max_num_hands=max_num_hands
        self.detectionCon=detectionCon
        self.trackCon=trackCon
        mp_drawing = mp.solutions.drawing_utils
        mp_drawing_styles = mp.solutions.drawing_styles
        mp_hands = mp.solutions.hands

        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.max_num_hands,
            min_detection_confidence=self.detectionCon,
            min_tracking_confidence=self.trackCon
        )
    
    def findHands(self, image, draw=True):
            

        image = cv2.flip(image, 1)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        self.results = self.hands.process(rgb)
        self.handTypes = []
        if self.results.multi_handedness:
            for hand in self.results.multi_handedness:
                self.handTypes.append(hand.classification[0].label)

        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                if draw: 
                    self.mp_drawing.draw_landmarks(
                        image,
                        hand_landmarks,
                        self.mp_hands.HAND_CONNECTIONS,
                        self.mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=5),
                        self.mp_drawing.DrawingSpec(color=(0, 200, 0), thickness=2))
        return image
                
    def findPosition(self, image, handNo=0,draw=True):
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id , lm in enumerate(myHand.landmark):
                h,w,c=image.shape
                cx,cy=int(lm.x*w),int(lm.y*h)
                lmList.append([id,cx,cy])
                if draw:
                    cv2.circle(image,(cx,cy),5,(255,0,255),cv2.FILLED)
        return lmList


# def main():
#     cap = cv2.VideoCapture(0)
#     detector = HandDetector()
#     prevTime=0
#     currTime=0
#     while True:
#         data,image = cap.read()
#         image = detector.findHands(image,draw=showSkeleton)
#         lmList = detector.findPosition(image)
#         if len(lmList)!=0:
#             print(lmList[8])
        
        
#         currTime=time.time()
#         fps=1/(currTime-prevTime)
#         prevTime=currTime
#         cv2.putText(image,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
#         cv2.imshow('MediaPipe Hands', cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
#         cv2.waitKey(1)

    


# if __name__ == "__main__":
#     main()