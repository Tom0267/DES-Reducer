from imutils.video import FileVideoStream, VideoStream
from ScreenBrightness import BrightnessControl
from DistanceCalc import DistanceCalculator
from EyeMovements import EyeMovement
from schedule import repeat, every
from imutils import face_utils
from Posture import Postures
from notifier import notif
from Config import config
from time import time
from GUI import GUI
import numpy as np
import threading
import schedule
import imutils
import timeq
import dlib
import cv2

#@repeat(every(2).seconds)										#repeat the function every 2 seconds to test
@repeat(every(25).minutes)										#repeat the function every 25 minutes
def takeBreak() -> None:
    notifier.notify("Take A Break", "You have been working for 20 minutes. Take a break to rest your eyes.", "critical")   #remind the user to take a break

detector = dlib.get_frontal_face_detector() 											#initialize dlib's face detector
predictor = dlib.shape_predictor("Resources/shape_predictor_68_face_landmarks.dat")		#initialize dlib's facial landmark predictor
#predictor = dlib.shape_predictor("Resources/predictor.dat")		                    #initialize dlib's facial landmark predictor
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]							#grab the indexes of the facial landmarks for the left eye
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]							#grab the indexes of the facial landmarks for the right eye

notifier = notif()                                              #initialize the notifier class
distanceCalc = DistanceCalculator(notifier)				        #initialize the distance calculator class
brightnessControl = BrightnessControl(notifier)					#initialize the brightness control class
posture = Postures(notifier)									#initialize the posture class
eyeMovement = EyeMovement(notifier)								#initialize the eye movement class

config = GUI(detector, predictor, notifier)												            #configure the application to the user's face
vs = VideoStream(src=0).start()															            #start the video stream thread
while True:
    if not vs.stream.isOpened():															        #check if the video stream was opened correctly
        notifier.notify("Cannot open camera", "Ensure your camera is connected.", "critical")		#display tray notification
        exit()																			            #exit the program	
        
      
    frame = vs.read()																	#read the frame from the threaded video stream
    frame = imutils.resize(frame, height=337, width=450)					            #resize the frame
    schedule.run_pending()																#run the scheduler
    
    brightness = threading.Thread(brightnessControl.update(frame))						#create the brightness control thread
    pose = threading.Thread(posture.checkPosture(frame))		                        #create the posture check thread
    brightness.start()											#start the brightness control thread
    pose.start()												#start the posture check thread
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)				#convert the frame to grayscale
    faces = detector(gray, 0)									#detect faces in the grayscale frame
    
    if not faces:												#check if a face was detected
        notifier.notify("No Face Detected", "Ensure your face is in the frame.", "critical")		#display tray notification
    else:
        for face in faces:
            shape = predictor(gray, face)							#determine the facial landmarks for the face region, then convert the facial landmark (x, y)-coordinates to a NumPy array
            shape = face_utils.shape_to_np(shape)
            
            leftEye = shape[lStart:lEnd]							#extract the left and right eye coordinates, then use the coordinates to calculate the eye aspect ratio for both eyes
            rightEye = shape[rStart:rEnd]
            
            dist = threading.Thread(distanceCalc.checkDist(leftEye,rightEye))						#create the distance calculator thread
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
        dist.join()											#join the distance calculator thread
        pose.join()											#join the posture check thread
        
        if cv2.waitKey(30) & 0xFF ==ord('q'):				#hold q to quit
            break

cv2.destroyAllWindows()								#close all windows
vs.stop()		                                    #stop the video stream
exit()												#exit the program