from ScreenBrightness import BrightnessControl
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

brightnessControl = BrightnessControl()		#initialize the brightness control class
eyeMovement = EyeMovement()						#initialize the eye movement class

detector = dlib.get_frontal_face_detector() 											#initialize dlib's face detector
predictor = dlib.shape_predictor("Resources/shape_predictor_68_face_landmarks.dat")		#initialize dlib's facial landmark predictor
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]							#grab the indexes of the facial landmarks for the left eye
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]							#grab the indexes of the facial landmarks for the right eye

vs = VideoStream(src=0).start()															#start the video stream thread
while True:
	frame = vs.read()
	brightness = threading.Thread(brightnessControl.update(frame))					#start the brightness control thread
	brightness.start()											#start the brightness control thread
	#frame = imutils.resize(frame, width=450)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	
	faces = detector(gray, 0)									#detect faces in the grayscale frame
	for face in faces:
		shape = predictor(gray, face)							#determine the facial landmarks for the face region, then convert the facial landmark (x, y)-coordinates to a NumPy array
		shape = face_utils.shape_to_np(shape)
		
		leftEye = shape[lStart:lEnd]							#extract the left and right eye coordinates, then use the coordinates to calculate the eye aspect ratio for both eyes
		rightEye = shape[rStart:rEnd]
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

	if cv2.waitKey(30) & 0xFF ==ord('q'):				#press q to quit
		break

cv2.destroyAllWindows()								#close all windows
vs.stop()		