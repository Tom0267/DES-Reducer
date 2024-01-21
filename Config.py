from imutils.video import FileVideoStream, VideoStream
from EyeMovements import EyeMovement
from imutils import face_utils
from EyeArea import Eyes
import pandas as pd
import numpy as np
import threading
import imutils
import dlib
import cv2
import csv

class config:
    def __init__(self, detector, predictor, notifier, vs):
        self.blinked = False
        self.relaxed = False
        self.vs = vs
        self.detector = detector
        self.predictor = predictor                                              
        self.notifier = notifier
        self.eyeArea = Eyes()                   
        self.EEdistances = []                  
        self.LEMDistances = []
        self.REMDistances = []           
        self.ear = []
        self.clearFile()
        self.searchString = []
        self.dataframe = pd.DataFrame(columns = ['Labels','Values'])        #creates dataframe

    def checkDataFrame(self, func):
        if func == 'Relax':
            self.searchString = ['EE', 'LEM', 'REM', 'EAR']                             #defines search values for relax function
        else:
            self.searchString = ['CEAR']                                                #defines search values for blinking function
        for label in self.searchString:                                                 #searches for values in dataframe
            self.dataframe.drop(self.dataframe.index[self.dataframe['Labels'] == label], inplace = True)   #drops values from dataframe
        
    def saveDataFrame(self):
        self.clearFile()                                                                    #clears contents of csv
        temp = self.dataframe.copy()                                                        #creates copy of dataframe
        self.dataframe.to_csv('Resources/configData.csv', index = False, header = True)     #save the dataframe to the csv file
        self.dataframe = temp.copy()                                                        #reverts dataframe to original state
        
    def clearFile(self):           
        self.f = open('Resources/configData.csv', 'w')		                #open the csv file
        self.writer = csv.writer(self.f)                                     #create the csv writer
        self.f.truncate(0)                               #clears contents of csv
        self.f.close
    
    def calculateDistance(self, leftEye, rightEye, mouth):
        leftEyeCenter = leftEye.mean(axis=0).astype("int")				    #compute the center of mass for each eye
        rightEyeCenter = rightEye.mean(axis=0).astype("int")                #compute the center of mass for each eye
        mouthCenter = mouth.mean(axis=0).astype("int")                      #compute the center of mass for the mouth
        self.EEdistances.append(np.linalg.norm(leftEyeCenter - rightEyeCenter))			#compute the euclidean distance between the center of the eyes
        self.LEMDistances.append(np.linalg.norm(leftEyeCenter - mouthCenter))			#compute the euclidean distance between the center of the left eye and the mouth
        self.REMDistances.append(np.linalg.norm(rightEyeCenter - mouthCenter))			#compute the euclidean distance between the center of the right eye and the mouth
        
    def averages(self, func):
        if func == 'Relax':
            self.EEDistance = np.mean(self.EEdistances)							#compute the average distance between the eyes
            self.LEMDistance = np.mean(self.LEMDistances)						#compute the average distance between the left eye and the mouth
            self.REMDistance = np.mean(self.REMDistances)						#compute the average distance between the right eye and the mouth
            self.EAR = np.mean(self.ear)										#compute the average eye aspect ratio
        elif func == 'Blinks':
            self.CEAR = np.mean(self.ear)                                        #compute the average closed eye aspect ratio
        elif func == 'Distance':
            self.EEDistance = np.mean(self.EEdistances)							#compute the average distance between the eyes
            self.LEMDistance = np.mean(self.LEMDistances)						#compute the average distance between the left eye and the mouth
            self.REMDistance = np.mean(self.REMDistances)						#compute the average distance between the right eye and the mouth

    def calculateEAR(self, leftEye, rightEye):
        leftEAR = self.eyeArea.eye_aspect_ratio(leftEye)				#left eye aspect ratio
        rightEAR = self.eyeArea.eye_aspect_ratio(rightEye)			    #right eye aspect ratio
        self.ear.append((leftEAR + rightEAR) / 2.0)				        #append the average the eye aspect ratio together for both eyes
    
    def checkCamera(self, vs):
        if not vs.stream.isOpened():																#check if the video stream was opened correctly
            self.notifier.show_toast("Cannot open camera", "Ensure your camera is connected.", duration=5, threaded=True)		#display tray notification
            exit()
            
    def configureRelax(self):
        self.checkCamera(self.vs)
        (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]							#grab the indexes of the facial landmarks for the left eye
        (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]							#grab the indexes of the facial landmarks for the right eye
        (mStart, mEnd) = face_utils.FACIAL_LANDMARKS_IDXS["mouth"]							#grab the indexes of the facial landmarks for the mouth
        self.counter = 0
        self.loop = True
        while self.loop == True:
            frame = self.vs.read()
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
                    mouth = shape[mStart:mEnd]
                    self.calculateDistance(leftEye,rightEye,mouth)     #calculate the distance between the eyes
                    self.calculateEAR(leftEye,rightEye)               #calculate the eye aspect ratio
                    self.counter += 1
                    if self.counter >= 5:
                        self.averages('Relax')
                        self.checkDataFrame('Relax')
                        self.dataframe = pd.concat([self.dataframe, pd.DataFrame({'Labels': ['EE'], 'Values': [self.EEDistance]})])  #write the average distance between the eyes to the dataframe
                        self.dataframe = pd.concat([self.dataframe, pd.DataFrame({'Labels': ['LEM'], 'Values': [self.LEMDistance]})]) #write the average distance between the left eye and the mouth to the dataframe
                        self.dataframe = pd.concat([self.dataframe, pd.DataFrame({'Labels': ['REM'], 'Values': [self.REMDistance]})]) #write the average distance between the right eye and the mouth to the dataframe
                        self.dataframe = pd.concat([self.dataframe, pd.DataFrame({'Labels': ['EAR'], 'Values': [self.EAR]})]) #write the average eye aspect ratio to the dataframe
                        self.notifier.show_toast("Relaxed Configuration Complete","", duration=5, threaded=True)		#display tray notification
                        self.relaxed = True
                        self.loop = False 
        if self.blinked == True and self.relaxed == True:
            self.saveDataFrame()
                        
    def configureBlinks(self):
        self.checkCamera(self.vs)
        (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]							#grab the indexes of the facial landmarks for the left eye
        (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]							#grab the indexes of the facial landmarks for the right eye
        self.counter = 0
        self.loop = True
        while self.loop == True:
            frame = self.vs.read()
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
                    self.calculateEAR(leftEye,rightEye)               #calculate the eye aspect ratio
                    self.counter += 1
                    if self.counter >= 5:
                        self.averages('Blinks')
                        self.checkDataFrame('Blinks')
                        self.dataframe = pd.concat([self.dataframe, pd.DataFrame({'Labels': ['CEAR'], 'Values': [self.CEAR]})]) #write the average eye aspect ratio to the csv file
                        self.notifier.show_toast("Blink Configuration Complete","", duration=5, threaded=True)		#display tray notification
                        self.blinked = True
                        self.loop = False 
        if self.blinked == True and self.relaxed == True:
            self.saveDataFrame()
            
    def configureDistance(self):
        self.checkCamera(self.vs)
        (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]							#grab the indexes of the facial landmarks for the left eye
        (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]							#grab the indexes of the facial landmarks for the right eye
        self.loop = True
        self.counter = 0
        while self.loop == True:
            frame = self.vs.read()
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
                    mouth = shape[mStart:mEnd]
                    self.calculateDistance(leftEye,rightEye,mouth)     #calculate the distance between the eyes
                    if counter >= 5:
                        self.averages('Distance')
                        self.notifier.show_toast("Distance Configuration Complete","", duration=5, threaded=True)        #display tray notification
                    