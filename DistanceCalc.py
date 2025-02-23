import pandas as pd
import numpy as np
import cv2
class DistanceCalculator:
    def checkDist(self, leftEye, rightEye) -> None:                  
        leftEyeCenter = leftEye.mean(axis=0)				                #compute the center of mass for each eye
        rightEyeCenter = rightEye.mean(axis=0)                              #compute the center of mass for each eye
        eyeDistance = np.linalg.norm(leftEyeCenter - rightEyeCenter)        #compute the distance between the eye centers
        
        distance_cm = self.a*eyeDistance**2+self.b*eyeDistance+self.c-15                      #calculate the distance in cm
        if distance_cm < 51:                                                                                                        #for safe use, distance to screen should be grater than 51 cm
            self.badFrames += 1                                                                                                     #increment the bad frames counter
            if self.badFrames == 20:                                                                                                #check if the bad frames counter is greater than 20
                self.notifier.notify("Too Close To Screen", f'{int(distance_cm)} cm - Not Safe', "normal")		                    #display tray notification
        elif distance_cm > 63:                                                                                                      #check if the distance is greater than 63 cm
            self.badFrames += 1                                                                                                     #increment the bad frames counter
            if self.badFrames == 20:
                self.notifier.notify("Too Far From Screen", f'{int(distance_cm)} cm - Not Safe', "normal")		                    #display tray notification            
        else:
            self.badFrames = 0                                                                                                      #reset the bad frames counter
    
    def __init__(self, notifier) -> None:
        self.notifier = notifier                                #initialize the notifier class
        distance_df = pd.read_csv('Resources/distance_xy.csv')  #read the csv data
        self.distance_pixel = distance_df['distance_pixel']     #read the distance data
        self.distance_cm = distance_df['distance_cm']           #read the distance data
        self.badFrames = 0                                      #initialize the bad frames counter
        coff = np.polyfit(self.distance_pixel, self.distance_cm, 2)         #get coefficients of the polynomial
        self.a, self.b, self.c = coff                                       #unpack the coefficients