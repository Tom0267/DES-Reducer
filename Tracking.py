import cv2
import numpy as np


#video
#cap = cv2.VideoCapture("tomAndSuzi.mp4")

#webcam
cap = cv2.VideoCapture(0)       #sets video cap to default camera
cap.set(3,640)      #set width
cap.set(4,480)      #set height
cap.set(10,100)     #set brightness


#object detection from stable camera
object_detector = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=20)

eyeCascade = cv2.CascadeClassifier("Resources/haarcascade_eye.xml")
faceCascade = cv2.CascadeClassifier("Resources/haarcascade_frontalface_default.xml")

while True:
    ret, Webcam = cap.read()

    mask = object_detector.apply(Webcam)
    grey = cv2.cvtColor(Webcam,cv2.COLOR_BGR2GRAY)
    cv2.imshow("Grey", grey)
    #_, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)
    #extract region of interest
    #roi = Webcam[340: 600,500: 700]



    #object detection
    #contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #for cnt in contours:
    #    #calculate area and remove small objects
    #    area = cv2.contourArea(cnt)
    #    if area > 100:
    #        cv2.drawContours(Webcam, [cnt], -1, (0,255,0), 2)
    
    #detect eyes and faces using the cascade
    eyes = eyeCascade.detectMultiScale(grey,1.1,4)
    faces = faceCascade.detectMultiScale(grey,1.1,4)
    
    #draw rectangles around eyes and faces
    for(x,y,w,h) in eyes:
        cv2.rectangle(Webcam, (x,y), (x+w,y+h),(255,0,0),3)
    
    for(x,y,w,h) in faces:
        cv2.rectangle(Webcam, (x,y), (x+w,y+h),(255,0,0),3)


    #key = cv2.waitKey(30)
    if cv2.waitKey(30) & 0xFF ==ord('q'):
        break

    cv2.imshow("Webcam", Webcam)

cap.release()
cv2.destroyAllWindows()

