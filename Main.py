from ScreenBrightness import BrightnessControl
from DistanceCalc import DistanceCalculator
from EyeMovements import EyeMovement
from schedule import repeat, every
from imutils import face_utils
from EyeRedness import Redness
from Posture import Postures
from notifier import notif
from Config import config
from Yawn import yawning
from time import time
from GUI import GUI
import numpy as np
import threading
import schedule
import imutils
import dlib
import cv2

delayTime = 20                                                                          #set the delay time for the break reminder

#@repeat(every(2).seconds)										#repeat the function every 2 seconds to test
@repeat(every(delayTime).minutes)										#repeat the function every 25 minutes
def takeBreak() -> None:
    notifier.notify("Take A Break", "You have been working for 20 minutes. Take a break to rest your eyes.", "critical")   #remind the user to take a break
    delayTime = 25                                                                                                         #set the delay time for the break reminder to 25 minutes to include the break time 

detector = dlib.get_frontal_face_detector() 											#initialize dlib's face detector
predictor = dlib.shape_predictor("Resources/shape_predictor_68_face_landmarks.dat")		#initialize dlib's facial landmark predictor
#predictor = dlib.shape_predictor("Resources/predictor.dat")		                    #initialize dlib's facial landmark predictor
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]							#grab the indexes of the facial landmarks for the left eye
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]							#grab the indexes of the facial landmarks for the right eye
(mStart, mEnd) = face_utils.FACIAL_LANDMARKS_IDXS["mouth"]								#grab the indexes of the facial landmarks for the mouth
badFrames = 0																			#initialize the bad frames counter

notifier = notif()                                              #initialize the notifier class
distanceCalc = DistanceCalculator(notifier)				        #initialize the distance calculator class
brightnessControl = BrightnessControl(notifier)					#initialize the brightness control class
eyeRedness = Redness(notifier)									#initialize the redness class

GUI(detector, predictor, notifier)			                    #configure the application to the user's face
eyeMovement = EyeMovement(notifier)								#initialize the eye movement class
posture = Postures(notifier, True)								#initialize the posture class
yawns = yawning(notifier)										#initialize the yawn class
cap = cv2.VideoCapture(0)									    #initialize the camera 
while True:
    if not cap.isOpened():															                #check if the video stream was opened correctly
        notifier.notify("Cannot open camera", "Ensure your camera is connected.", "critical")		#display tray notification
        exit()																			            #exit the program
        
    ret, frame = cap.read()																    #read the frame from the camera and check if it was read correctly
    if ret:                                                                                 #check if the frame was read correctly
        frame = cv2.resize(frame, (450, 337))					                            #resize the frame
        schedule.run_pending()																#run the scheduler
        
        brightness = threading.Thread(brightnessControl.update(frame))						#create the brightness control thread
        pose = threading.Thread(posture.checkPosture(frame))		                        #create the posture check thread
        brightness.start()											#start the brightness control thread
        pose.start()												#start the posture check thread
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)				#convert the frame to grayscale
        faces = detector(gray, 0)									#detect faces in the grayscale frame
        
        if not faces:												#check if a face was detected
            badFrames += 1											#increment the bad frames counter
            if badFrames > 70:								        #check if bad frames counter for greater than 5 seconds
                notifier.notify("No Face Detected", "Ensure your face is in the frame.", "critical")		#display tray notification
                badFrames = 0										#reset the bad frames counter
        else:
            for face in faces:
                shape = predictor(gray, face)							#determine the facial landmarks for the face region, then convert the facial landmark (x, y)-coordinates to a NumPy array
                shape = face_utils.shape_to_np(shape)                   #convert the facial landmark (x, y)-coordinates to a NumPy array
                
                leftEye = shape[lStart:lEnd]							#extract the left eye coordinates
                rightEye = shape[rStart:rEnd]                           #extract the right eye coordinates
                mouth = shape[mStart:mEnd]                              #extract the mouth coordinates
                
                yawned = threading.Thread(yawns.checkYawn(mouth, frame))		                        #create the yawn checker thread
                yawned.start()											                                #start the yawn checker thread
                dist = threading.Thread(distanceCalc.checkDist(leftEye,rightEye))						#create the distance calculator thread
                dist.start()											                                #start the distance calculator thread
                redness = threading.Thread(eyeRedness.checkRedness(frame, leftEye, rightEye))			#create the redness checker thread
                redness.start()											                                #start the redness checker thread
                
                eyeMovement.checkMovement(leftEye,rightEye)				            #check if the eyes are blinking or squinting
                leftEyeHull, rightEyeHull = eyeMovement.getHull()                   #get the hulls for the eyes to draw on the frame
                cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)			#draw the hull around the left eye
                cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)			#draw the hull around the right eye
                
                total = eyeMovement.getTotal()                                      #get the total number of blinks
                ear = eyeMovement.getEAR()                                          #get the eye aspect ratio
                cv2.putText(frame, "Blinks: {}".format(total), (10, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)				#draw the total number of blinks on the frame
                cv2.putText(frame, "EAR: {:.2f}".format(ear), (300, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)				#draw the calculated eye aspect ratio on the frame
                
            cv2.imshow("Eye Care", frame)						#show the frame
            brightness.join()									#join the brightness control thread
            dist.join()											#join the distance calculator thread
            pose.join()											#join the posture check thread
            yawned.join()										#join the yawn checker thread
            redness.join()										#join the redness checker thread
            
    if cv2.waitKey(30) & 0xFF ==ord('q'):				#hold q to quit
        break                                           #break the loop

cv2.destroyAllWindows()								#close all windows
cap.release()										#release the camera
exit()												#exit the program