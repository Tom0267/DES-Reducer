from imutils.video import FileVideoStream, VideoStream
from imutils import face_utils
from EyeArea import Eyes
import pandas as pd
import numpy as np
import threading
import imutils
import dlib
import cv2
import csv
class EyeMovement:
    def checkMovement(self,leftEye,rightEye):
        self.leftEAR = self.eyeArea.eyeAspectRatio(leftEye)				#left eye aspect ratio
        self.rightEAR = self.eyeArea.eyeAspectRatio(rightEye)			#right eye aspect ratio
        self.ear = (self.leftEAR + self.rightEAR) / 2.0				    #average the eye aspect ratio together for both eyes

        self.leftEyeHull = cv2.convexHull(leftEye)			    #calculate the convex hull for the left eye
        self.rightEyeHull = cv2.convexHull(rightEye)			#calculate the convex hull for the right eye

        if self.ear <= self.blinkThresh:										#check is eye aspect ratio is below the blink threshold
            self.blinkCounter += 1										        #increment the blink Counter
            if self.blinkCounter >= self.blinkConsecFrames and not self.blinkCounter > 3:			#if the eyes were closed for a sufficient number of frames increment the total number of blinks
                self.total += 1
                self.blink2 = np.datetime64('now')					    #record the time of the blink
                if self.blink2 - self.blink1 >  8:						#check if the time between blinks is greater than 8 seconds
                    self.notifier.show_toast("Don't Forget To Blink", "For healthy eyes, you should be blinking every 5 seconds.", duration=5, threaded=True)
                elif self.blink2 - self.blink1 < 2:						#check if the time between blinks is less than 2
                    self.notifier.show_toast("Rapid Blinking", "Take a break from the screen to ensure your eyes stay healythy.", duration=5, threaded=True)
        else :
            self.blinkCounter = 0								                #reset the eye frame blink Counter
            self.blink1 = self.blink2
            
        if self.ear <= self.squintThresh:										#check is eye aspect ratio is below the squint threshold
            self.squintCounter += 1										        #increment the squint Counter
            if self.squintCounter >= self.squintConsecFrames:					#if the eyes were closed for a sufficient number of frames increment the total number of squints
                self.notifier.show_toast("Squinting Detected", "Ensure you have proper lighting and are not too close to the screen.", duration=5, threaded=True)		#display tray notification
        else :
            self.squintCounter = 0								#reset the eye frame squint Counter
            
    def getHull(self):
        return self.leftEyeHull, self.rightEyeHull              #return the hulls

    def getEAR(self):
        return self.ear                                         #return the eye aspect ratio
    
    def getTotal(self):
        return self.total                                       #return the total number of blinks

    def __init__(self, notifier):
        self.notifier = notifier					            #initialize the notifier
        self.eyeArea = Eyes()					                #initialize the eye area class
        self.blink1 = np.datetime64('now')                      #initializes blink1
        self.blink2 = np.datetime64('now')                      #initializes blink2
        self.dataframe = pd.DataFrame(columns=['Labels', 'Values'])     #initializes the dataframe
        self.dataframe = pd.read_csv('Resources/configData.csv')        #read the configuration file
        self.leftEye = 0                                        #initializes left eye
        self.rightEye = 0                                       #initializes right eye
        self.ear = 0.00                                         #initializes eye aspect ratio
        self.leftEyeHull = 0                                    #initializes eye hull
        self.rightEyeHull = 0                                   #initializes eye hull
        self.blinkThresh = self.dataframe['Values'].loc[self.dataframe.index[self.dataframe['Labels'] == 'CEAR']].tolist()		  #gets value from csv file
        self.blinkThresh = self.blinkThresh[0] + 0.06           #threshold for eye aspect ratio to count as a blink
        self.squintThresh = self.dataframe['Values'].loc[self.dataframe.index[self.dataframe['Labels'] == 'EAR']].tolist()		  #gets value from csv file
        self.squintThresh = self.squintThresh[0] + 0.02         #threshold for eye aspect ratio to count as a squint
        self.blinkConsecFrames = 2					            #number of consecutive frames the eye must be below the threshold for to count as a blink
        self.squintConsecFrames = 5				                #number of consecutive frames the eye must be below the threshold for to count as a squinting
        self.blinkCounter = 0									#frame blink Counter
        self.squintCounter = 0									#frame squint Counter
        self.total = 0									        #total number of blinks