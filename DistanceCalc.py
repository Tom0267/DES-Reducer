import pandas as pd
import numpy as np
import cv2
class DistanceCalculator:
    def checkDist(self, leftEye, rightEye):
        coff = np.polyfit(self.distance_pixel, self.distance_cm, 2)         # get corrlation coffs
        a, b, c = coff                                                      #unpack the coffs
                  
        leftEyeCenter = leftEye.mean(axis=0)				    #compute the center of mass for each eye
        rightEyeCenter = rightEye.mean(axis=0)                #compute the center of mass for each eye
        eyeDistance = np.linalg.norm(leftEyeCenter - rightEyeCenter)        #compute the euclidean distance between the eye centers
        
        distance_cm = a*eyeDistance**2+b*eyeDistance+c-10                      #calculate the distance in cm
        if distance_cm < 55:                                                                                                        #for safe use, distance to screen should be grater than 51 cm
            self.notifier.show_toast("Too Close To Screen", f'{int(distance_cm)} cm - Not Safe', duration=5, threaded=True)		#display tray notification
        elif distance_cm > 70:                                                                                                      #check if the distance is greater than 65 cm
            self.notifier.show_toast("Too Far From Screen", f'{int(distance_cm)} cm - Not Safe', duration=5, threaded=True)		#display tray notification            
    
    def __init__(self, notifier):
        distance_df = pd.read_csv('distance_xy.csv')            #read the csv data
        self.distance_pixel = distance_df['distance_pixel']     #read the distance data
        self.distance_cm = distance_df['distance_cm']           #read the distance data
        self.notifier = notifier                                #initialize the notifier