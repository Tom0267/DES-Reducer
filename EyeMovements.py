from EyeArea import Eyes
import pandas as pd
import numpy as np
import cv2
class EyeMovement:
    def checkMovement(self,leftEye,rightEye) -> None:
        self.leftEAR = self.eyeArea.eyeAspectRatio(leftEye)				#left eye aspect ratio
        self.rightEAR = self.eyeArea.eyeAspectRatio(rightEye)			#right eye aspect ratio
        self.ear = (self.leftEAR + self.rightEAR) / 2.0				    #average the eye aspect ratio together for both eyes

        self.leftEyeHull = cv2.convexHull(leftEye)			    #calculate the convex hull for the left eye
        self.rightEyeHull = cv2.convexHull(rightEye)			#calculate the convex hull for the right eye

        if self.ear <= self.blinkThresh:										#check is eye aspect ratio is below the blink threshold
            self.blinkCounter += 1										        #increment the blink Counter
            if self.blinkCounter >= self.blinkConsecFrames and self.blinkCounter < 3:			#if the eyes were closed for a sufficient number of frames increment the total number of blinks
                self.total += 1
                self.blink2 = np.datetime64('now')					    #record the time of the blink
                if self.blink2 - self.blink1 >  8:						#check if the time between blinks is greater than 8 seconds
                    self.notifier.notify("Don't Forget To Blink", "For healthy eyes, you should be blinking every 5 seconds.", "low")
                elif self.blink2 - self.blink1 < 2 and self.notificationTime - self.blink2 >= self.notificationDelay:			#check if the time between blinks is less than 2 seconds and the time since the last notification is greater than 20 seconds
                    self.notifier.notify("Rapid Blinking", "Take a break from the screen to ensure your eyes stay healythy.", "low")
                    self.notificationTime = np.datetime64('now')		#record the time of the notification for rapid blinking to prevent spamming
        else :
            self.blinkCounter = 0								                #reset the eye frame blink Counter
            self.blink1 = self.blink2                                           #record the time of the last blink
            
        if self.ear <= self.squintThresh and self.ear > self.blinkThresh:		#check is eye aspect ratio is below the squint threshold and above the blink threshold
            self.squintCounter += 1										        #increment the squint Counter
            if self.squintCounter == self.squintConsecFrames:   #if the eyes were closed for a sufficient number of frames
                self.notifier.notify("Squinting Detected", "Ensure you have proper lighting and are not too close to the screen.", "low")		#display tray notification
        else :
            self.squintCounter = 0								#reset the eye frame squint Counter
            
    def getHull(self) -> tuple:
        return self.leftEyeHull, self.rightEyeHull              #return the hulls

    def getEAR(self) -> float:
        return self.ear                                         #return the eye aspect ratio
    
    def getTotal(self) -> int:
        return self.total                                       #return the total number of blinks

    def __init__(self, notifier) -> None:
        self.notifier = notifier                                #initialize the notifier class
        self.eyeArea = Eyes()					                #initialize the eye area class
        self.blink1 = np.datetime64('now')                      #initializes blink1
        self.blink2 = np.datetime64('now')                      #initializes blink2
        self.ear = 0.00                                         #initializes eye aspect ratio
        self.leftEyeHull = 0                                    #initializes eye hull
        self.rightEyeHull = 0                                   #initializes eye hull
        try:
            self.dataframe = pd.DataFrame(columns=['Labels', 'Values'])     #initializes the dataframe
            self.dataframe = pd.read_csv('Resources/configData.csv')        #read the configuration file
            self.blinkThresh = self.dataframe['Values'].loc[self.dataframe.index[self.dataframe['Labels'] == 'CEAR']].tolist()		  #gets value from csv file
            self.blinkThresh = self.blinkThresh[0] #+ 0.03           #threshold for eye aspect ratio to count as a blink
            self.squintThresh = self.dataframe['Values'].loc[self.dataframe.index[self.dataframe['Labels'] == 'EAR']].tolist()		  #gets value from csv file
            self.squintThresh = self.squintThresh[0] #+ 0.02         #threshold for eye aspect ratio to count as a squint
        except Exception as e:
            self.notifier.notify("Error", "Error in reading configuration file", "critical")		#display tray notification
            exit()
        self.blinkConsecFrames = 2					            #number of consecutive frames the eye must be below the threshold for to count as a blink
        self.squintConsecFrames = 5			                    #number of consecutive frames the eye must be below the threshold for to count as a squinting
        self.blinkCounter = 0									#frame blink Counter
        self.squintCounter = 0									#frame squint Counter 
        self.total = 0									        #total number of blinks counter
        self.notificationTime = np.datetime64('now')            #time of the last notification for rapid blinking to prevent spamming 
        self.notificationDelay = 20                             #set the notification delay to 20 seconds for rapid blinking notifications