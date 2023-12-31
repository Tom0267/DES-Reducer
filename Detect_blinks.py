from scipy.spatial import distance as dist
from imutils.video import FileVideoStream
from imutils.video import VideoStream
from imutils import face_utils
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

EYE_AR_THRESH = 0.25						#threshold for eye aspect ratio to count as a blink
EYE_AR_CONSEC_FRAMES = 2					#number of consecutive frames the eye must be below the threshold for to count as a blink
COUNTER = 0									#frame counter
TOTAL = 0									#total number of blinks

detector = dlib.get_frontal_face_detector() 											#initialize dlib's face detector
predictor = dlib.shape_predictor("Resources/shape_predictor_68_face_landmarks.dat")		#initialize dlib's facial landmark predictor
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]							#grab the indexes of the facial landmarks for the left eye
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]							#grab the indexes of the facial landmarks for the right eye

vs = VideoStream(src=0).start()															#start the video stream thread

while True:
	frame = vs.read()
	frame = imutils.resize(frame, width=450)
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

		if ear < EYE_AR_THRESH:							#check is eye aspect ratio is below the blink threshold
			COUNTER += 1								#increment the blink counter
		else:
			if COUNTER >= EYE_AR_CONSEC_FRAMES:			#if the eyes were closed for a sufficient number of then increment the total number of blinks
				TOTAL += 1
			COUNTER = 0						#reset the eye frame counter


		#draw the total number of blinks on the frame along with the computed eye aspect ratio for the frame
		cv2.putText(frame, "Blinks: {}".format(TOTAL), (10, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
		cv2.putText(frame, "EAR: {:.2f}".format(ear), (300, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

		cv2.imshow("Window", frame)						#show the frame
		if cv2.waitKey(30) & 0xFF ==ord('q'):			#press q to quit
			break

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()