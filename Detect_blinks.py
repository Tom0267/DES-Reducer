from scipy.spatial import distance as dist
from imutils.video import FileVideoStream
from imutils.video import VideoStream
from win10toast import ToastNotifier
from imutils import face_utils
from time import time
import numpy as np
import imutils
import time
import dlib
import cv2

# compute the euclidean distances between the two sets of vertical eye landmarks (x, y) coordinates
def eye_aspect_ratio(eye):
	A = dist.euclidean(eye[1], eye[5])
	B = dist.euclidean(eye[2], eye[4])
	C = dist.euclidean(eye[0], eye[3])  					#compute the euclidean distance between the horizontal eye landmark (x, y)-coordinates
	ear = (A + B) / (2.0 * C)  		 						#compute the eye aspect ratio
	return ear

notifier = ToastNotifier()					#initialize the notifier

blinkThresh = 0.26						#threshold for eye aspect ratio to count as a blink
squintThresh = 0.3						#threshold for eye aspect ratio to count as a squint
EYE_BLINK_CONSEC_FRAMES = 2					#number of consecutive frames the eye must be below the threshold for to count as a blink
EYE_SQUINT_CONSEC_FRAMES = 10				#number of consecutive frames the eye must be below the threshold for to count as a squinting
blinkCounter = 0									#frame blink Counter
squintCounter = 0									#frame squint Counter
TOTAL = 0									#total number of blinks


detector = dlib.get_frontal_face_detector() 											#initialize dlib's face detector
predictor = dlib.shape_predictor("Resources/shape_predictor_68_face_landmarks.dat")		#initialize dlib's facial landmark predictor
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]							#grab the indexes of the facial landmarks for the left eye
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]							#grab the indexes of the facial landmarks for the right eye

vs = VideoStream(src=0).start()															#start the video stream thread
blink1 = np.datetime64('now')
blink2 = np.datetime64('now')
while True:
	frame = vs.read()
	#frame = imutils.resize(frame, width=450)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	
	faces = detector(gray, 0)							#detect faces in the grayscale frame
	for face in faces:
		shape = predictor(gray, face)					#determine the facial landmarks for the face region, then convert the facial landmark (x, y)-coordinates to a NumPy array
		shape = face_utils.shape_to_np(shape)
		
		leftEye = shape[lStart:lEnd]					#extract the left and right eye coordinates, then use the coordinates to compute the eye aspect ratio for both eyes
		rightEye = shape[rStart:rEnd]
		leftEAR = eye_aspect_ratio(leftEye)				#left eye aspect ratio
		rightEAR = eye_aspect_ratio(rightEye)			#right eye aspect ratio
		
		ear = (leftEAR + rightEAR) / 2.0				#average the eye aspect ratio together for both eyes
		
		leftEyeHull = cv2.convexHull(leftEye)			#compute the convex hull for the left eye
		rightEyeHull = cv2.convexHull(rightEye)			#compute the convex hull for the right eye
		cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)			#draw the hull around the left eye
		cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)			#draw the hull around the right eye

		if ear <= blinkThresh:								#check is eye aspect ratio is below the blink threshold
			blinkCounter += 1										#increment the blink Counter
			if blinkCounter >= EYE_BLINK_CONSEC_FRAMES and not blinkCounter > 3:			#if the eyes were closed for a sufficient number of frames increment the total number of blinks
				TOTAL += 1
				blink2 = np.datetime64('now')
				if blink2 - blink1 >5:
					notifier.show_toast("BLINK BITCH!!", "For healthy eyes, you should be blinking every 5 seconds.", duration=20, threaded=True)
		else :
			blinkCounter = 0								#reset the eye frame blink Counter
			blink1 = blink2
		if ear <= squintThresh:								#check is eye aspect ratio is below the squint threshold
			squintCounter += 1										#increment the squint Counter
			if squintCounter >= EYE_SQUINT_CONSEC_FRAMES:				#if the eyes were closed for a sufficient number of frames increment the total number of squints
				notifier.show_toast("Squinting Detected", "Ensure you have proper lighting and are not too close to the screen.", duration=20, threaded=True)		#display tray notification
		else :
			squintCounter = 0								#reset the eye frame squint Counter
		#draw the total number of blinks on the frame along with the computed eye aspect ratio for the frame
		cv2.putText(frame, "Blinks: {}".format(TOTAL), (10, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
		cv2.putText(frame, "EAR: {:.2f}".format(ear), (300, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

		cv2.imshow("Eye Care", frame)						#show the frame
		if cv2.waitKey(30) & 0xFF ==ord('q'):				#press q to quit
			break

#cleanup
cv2.destroyAllWindows()								#close all windows
vs.stop()											#stop the video stream