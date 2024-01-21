from imutils.video import FileVideoStream, VideoStream
from ScreenBrightness import BrightnessControl
from DistanceCalc import DistanceCalculator
from EyeMovements import EyeMovement
from win10toast import ToastNotifier
from BreakReminder import breakTime
from imutils import face_utils
from Config import config
from time import time
from GUI import GUI
import numpy as np
import threading
import imutils
import time
import dlib
import cv2
 
brightnessControl = BrightnessControl()					#initialize the brightness control class
notifier = ToastNotifier()								#initialize the notifier
breakCheck = breakTime(notifier)						#initialize the break check class
distanceCalc = DistanceCalculator(notifier)				#initialize the distance calculator class

detector = dlib.get_frontal_face_detector() 											#initialize dlib's face detector
predictor = dlib.shape_predictor("Resources/shape_predictor_68_face_landmarks.dat")		#initialize dlib's facial landmark predictorqqqqqq
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]							#grab the indexes of the facial landmarks for the left eye
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]							#grab the indexes of the facial landmarks for the right eye

config = GUI(detector, predictor, notifier)													#configure the application to the user's face
vs = VideoStream(src=0).start()															#start the video stream thread
eyeMovement = EyeMovement(notifier)						#initialize the eye movement class
while True:
    if not vs.stream.isOpened():																#check if the video stream was opened correctly
        self.notifier.show_toast("Cannot open camera", "Ensure your camera is connected.", duration=5, threaded=True)		#display tray notification
        exit()
        
    frame = vs.read()																	#read the frame from the threaded video stream
    brightness = threading.Thread(brightnessControl.update(frame))						#start the brightness control thread
    breakTime = threading.Thread(breakCheck.checkBreak())								#start the break check thread
    brightness.start()											#start the brightness control thread
    breakTime.start()											#start the break check thread
    
    frame = imutils.resize(frame, width=450)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    faces = detector(gray, 0)									#detect faces in the grayscale frame
    if not faces:												#check if a face was detected
        notifier.show_toast("No Face Detected", "Ensure your face is in the frame.", duration=5, threaded=True)		#display tray notification
    else:
        for face in faces:
            shape = predictor(gray, face)							#determine the facial landmarks for the face region, then convert the facial landmark (x, y)-coordinates to a NumPy array
            shape = face_utils.shape_to_np(shape)
            
            leftEye = shape[lStart:lEnd]							#extract the left and right eye coordinates, then use the coordinates to calculate the eye aspect ratio for both eyes
            rightEye = shape[rStart:rEnd]
            
            dist = threading.Thread(distanceCalc.checkDist(leftEye,rightEye))						#start the brightness control thread
            dist.start()											#start the brightness control thread
            
            eyeMovement.checkMovement(leftEye,rightEye)				#check if the eyes are blinking or squinting
            leftEyeHull, rightEyeHull = eyeMovement.getHull()
            cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)			#draw the hull around the left eye
            cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)			#draw the hull around the right eye
            
            total = eyeMovement.getTotal()
            ear = eyeMovement.getEAR()
            cv2.putText(frame, "Blinks: {}".format(total), (10, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)				#draw the total number of blinks on the frame
            cv2.putText(frame, "EAR: {:.2f}".format(ear), (300, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)				#draw the calculated eye aspect ratio on the frame
            
        cv2.imshow("Eye Care", frame)						#show the frame
        
        brightness.join()									#join the brightness control thread
        breakTime.join()									#join the break check thread
        dist.join()											#join the distance calculator thread
        
        if cv2.waitKey(30) & 0xFF ==ord('q'):				#press q to quit
            break

cv2.destroyAllWindows()								#close all windows
vs.stop()		