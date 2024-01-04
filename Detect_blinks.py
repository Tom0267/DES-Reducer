from ScreenBrightness import BrightnessControl
from scipy.spatial import distance as dist
from imutils.video import FileVideoStream
from imutils.video import VideoStream
from win10toast import ToastNotifier
from imutils import face_utils
from time import time
import numpy as np
import threading
import imutils
import time
import dlib
import cv2

#calculate the euclidean distances between the two sets of vertical eye landmarks (x, y) coordinates
def eye_aspect_ratio(eye):
	A = dist.euclidean(eye[1], eye[5])
	B = dist.euclidean(eye[2], eye[4])
	C = dist.euclidean(eye[0], eye[3])  					#calculate the euclidean distance between the horizontal eye landmark (x, y)-coordinates
	ear = (A + B) / (2.0 * C)  		 						#calculate the eye aspect ratio
	return ear

brightnessControl = BrightnessControl()		#initialize the brightness control class
notifier = ToastNotifier()					#initialize the notifier
blinkThresh = 0.25						#threshold for eye aspect ratio to count as a blink
squintThresh = 0.29						#threshold for eye aspect ratio to count as a squint
blinkConsecFrames = 2					#number of consecutive frames the eye must be below the threshold for to count as a blink
squintConsecFrames = 10				#number of consecutive frames the eye must be below the threshold for to count as a squinting
blinkCounter = 0									#frame blink Counter
squintCounter = 0									#frame squint Counter
total = 0									#total number of blinks

detector = dlib.get_frontal_face_detector() 											#initialize dlib's face detector
predictor = dlib.shape_predictor("Resources/shape_predictor_68_face_landmarks.dat")		#initialize dlib's facial landmark predictor
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]							#grab the indexes of the facial landmarks for the left eye
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]							#grab the indexes of the facial landmarks for the right eye

vs = VideoStream(src=0).start()															#start the video stream thread
blink1 = np.datetime64('now')
blink2 = np.datetime64('now')
while True:
	frame = vs.read()
	brightness = threading.Thread(brightnessControl.update(frame))					#start the brightness control thread
	brightness.start()									#start the brightness control thread
	#frame = imutils.resize(frame, width=450)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	
	faces = detector(gray, 0)							#detect faces in the grayscale frame
	for face in faces:
		shape = predictor(gray, face)					#determine the facial landmarks for the face region, then convert the facial landmark (x, y)-coordinates to a NumPy array
		shape = face_utils.shape_to_np(shape)
		
		leftEye = shape[lStart:lEnd]					#extract the left and right eye coordinates, then use the coordinates to calculate the eye aspect ratio for both eyes
		rightEye = shape[rStart:rEnd]
		leftEAR = eye_aspect_ratio(leftEye)				#left eye aspect ratio
		rightEAR = eye_aspect_ratio(rightEye)			#right eye aspect ratio
		
		ear = (leftEAR + rightEAR) / 2.0				#average the eye aspect ratio together for both eyes
		
		leftEyeHull = cv2.convexHull(leftEye)			#calculate the convex hull for the left eye
		rightEyeHull = cv2.convexHull(rightEye)			#calculate the convex hull for the right eye
		cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)			#draw the hull around the left eye
		cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)			#draw the hull around the right eye

		if ear <= blinkThresh:										#check is eye aspect ratio is below the blink threshold
			blinkCounter += 1										#increment the blink Counter
			if blinkCounter >= blinkConsecFrames and not blinkCounter > 3:			#if the eyes were closed for a sufficient number of frames increment the total number of blinks
				total += 1
				blink2 = np.datetime64('now')					#record the time of the blink
				if blink2 - blink1 >  8:						#check if the time between blinks is greater than 8 seconds
					notifier.show_toast("Don't Forget To Blink", "For healthy eyes, you should be blinking every 5 seconds.", duration=5, threaded=True)
				elif blink2 - blink1 < 2:						#check if the time between blinks is less than 2
					notifier.show_toast("Rapid Blinking", "Take a break from the screen to ensure your eyes stay healythy.", duration=5, threaded=True)
		else :
			blinkCounter = 0								#reset the eye frame blink Counter
			blink1 = blink2

		if ear <= squintThresh:										#check is eye aspect ratio is below the squint threshold
			squintCounter += 1										#increment the squint Counter
			if squintCounter >= squintConsecFrames:					#if the eyes were closed for a sufficient number of frames increment the total number of squints
				notifier.show_toast("Squinting Detected", "Ensure you have proper lighting and are not too close to the screen.", duration=5, threaded=True)		#display tray notification
		else :
			squintCounter = 0								#reset the eye frame squint Counter

		cv2.putText(frame, "Blinks: {}".format(total), (10, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)				#draw the total number of blinks on the frame
		cv2.putText(frame, "EAR: {:.2f}".format(ear), (300, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)				#draw the calculated eye aspect ratio on the frame
		cv2.imshow("Eye Care", frame)						#show the frame
	brightness.join()									#join the brightness control thread

	if cv2.waitKey(30) & 0xFF ==ord('q'):				#press q to quit
		break

cv2.destroyAllWindows()								#close all windows
vs.stop()											#stop the video stream