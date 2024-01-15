from imutils.video import FileVideoStream
from imutils.video import VideoStream
from EyeMovements import EyeMovement
from imutils import face_utils
from time import time
import numpy as np
import threading
import imutils
import time
import dlib
import cv2
import csv

class config:
    def __init__(self, detector, predictor, notifier):
        self.detector = detector
        self.predictor = predictor
        self.notifier = notifier
        self.file = open('Resources/configData.csv', 'w')
        self.writer = csv.writer(self.file)
        print("initialized")
    
    def calculateDistance(self, leftEye, rightEye):
        leftEyeCenter = leftEye.mean(axis=0).astype("int")				#compute the center of mass for each eye
        rightEyeCenter = rightEye.mean(axis=0).astype("int")
        distance = np.linalg.norm(leftEyeCenter - rightEyeCenter)			#compute the euclidean distance between the center of the eyes
        return distance

    def checkCamera(self, vs):
        if not vs.stream.isOpened():																#check if the video stream was opened correctly
            self.notifier.show_toast("Cannot open camera", "Ensure your camera is connected.", duration=5, threaded=True)		#display tray notification
            exit()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    def configure(self):
        vs = VideoStream(src=0).start()
        self.checkCamera(vs)
        (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]							#grab the indexes of the facial landmarks for the left eye
        (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]							#grab the indexes of the facial landmarks for the right eye
        while True:
            self.checkCamera(vs)
            frame = vs.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.detector(gray, 0)									#detect faces in the grayscale frame
            if not faces:												#check if a face was detected
                self.notifier.show_toast("No Face Detected", "Ensure your face is in the frame.", duration=5, threaded=True)		#display tray notification
            else:
                for face in faces:
                    shape = self.predictor(gray, face)							#determine the facial landmarks for the face region, then convert the facial landmark (x, y)-coordinates to a NumPy array
                    shape = face_utils.shape_to_np(shape)
                    leftEye = shape[lStart:lEnd]							#extract the left and right eye coordinates, then use the coordinates to calculate the eye aspect ratio for both eyes
                    rightEye = shape[rStart:rEnd]
                    distance = self.calculateDistance(leftEye,rightEye)     #calculate the distance between the eyes
                    if cv2.waitKey(2) & 0xFF == ord('k'):
                        self.writer.writerow([distance])
                        print('distance written')
                        
                        
            cv2.putText(frame, "Press 'k' to record face values", (10, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.imshow("Configuring", frame)
            
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        vs.stop()
        cv2.destroyAllWindows()