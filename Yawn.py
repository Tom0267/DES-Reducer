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

class yawning:
    def mouthAspectRatio(self, mouth) -> float:
        A = np.linalg.norm(mouth[13] - mouth[19])				#distance between the corners of the mouth
        B = np.linalg.norm(mouth[14] - mouth[18])				#distance between the corners of the mouth
        C = np.linalg.norm(mouth[15] - mouth[17])				#distance between the corners of the mouth
        D = np.linalg.norm(mouth[12] - mouth[16])				#distance between the corners of the mouth
        aspectRatio = (A + B + C) / (3.0 * D)					#mouth aspect ratio
        return aspectRatio										#return the mouth aspect ratio
    
    def checkYawn(self, mouth, frame) -> None:
        self.mouthRatio = self.mouthAspectRatio(mouth)		    #mouth aspect ratio
        mouthHull = cv2.convexHull(mouth)						#calculate the convex hull for the mouth
        if self.mouthRatio > 0.5:								#check if the mouth aspect ratio is greater than 0.7
            self.yawnCounter += 1								#increment the yawn counter
            if self.yawnCounter >= 8 and self.yawnCounter < 10:	#if the mouth was open for a sufficient number of frames
                self.notifier.notify("Yawning Detected", "If your'e getting tired, consider taking a break", "critical")	#display tray notification
        else :
            self.yawnCounter = 0								#reset the yawn counter
            
        cv2.drawContours(frame, [mouthHull], -1, (0, 255, 0), 1)			#draw the hull around the left eye
        cv2.putText(frame, "Yawn: {:.2f}".format(self.mouthRatio), (300, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)	#display the mouth aspect ratio on the frame
        cv2.imshow("Yawn Checker", frame)										#display the frame
        
    def __init__(self, notifier) -> None:
        self.notifier = notifier                                #initialize the notifier class
        self.yawnCounter = 0                                    #initialize the yawn counter
        