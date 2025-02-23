import numpy as np
import cv2
class Redness:
    
    def getRedness(self, roi) -> float:
        roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)                               #convert the roi to the HSV (hue, saturation, and lightness value) color space  
        redMask1 = cv2.inRange(roi, (0, 70, 50), (10, 255, 255))                   #create a mask for the red pixels in the roi 
        redMask2 = cv2.inRange(roi, (170, 70, 50), (180, 255, 255))                #create a mask for the red pixels in the roi 
        redMask = cv2.add(redMask1, redMask2)                                       #combine the two masks to get the final mask
        avgRed = np.mean(roi[redMask > 0])                                         #get the average red intensity of the roi 
        return avgRed
    
    def checkRedness(self, frame, leftEye, rightEye) -> None:
        copy = frame.copy()                                     #create a copy of the frame
        (x, y, w, h) = cv2.boundingRect(leftEye)                #get the coordinates of the left eye rectangle
        roi1 = frame[y:y + h, x:x + w]                          #get the region of the left eye
        (x, y, w, h) = cv2.boundingRect(rightEye)               #get the coordinates of the left eye rectangle
        roi2 = frame[y:y + h, x:x + w]                          #get the region of the right eye 
        leftRedness = self.getRedness(roi1)                     #get the redness of the left eye
        rightRedness = self.getRedness(roi2)                    #get the redness of the right eye
        cv2.putText(copy, "Left Eye Redness: {:.2f}".format(leftRedness), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)              #draw the redness of the left eye on the frame
        cv2.putText(copy, "Right Eye Redness: {:.2f}".format(rightRedness), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)            #draw the redness of the right eye on the frame
        cv2.imshow("Redness Checker", copy)                                                                                                     #show the frame
        if (leftRedness > 90 or rightRedness > 90) and (np.datetime64('now') - self.notificationTime >= self.notificationDelay):     #check if the redness of the eyes is greater than 50 and the time since the last notification is greater than 20 seconds
            self.notifier.notify("Red Eyes", "if your eyes are getting red, Take a break to rest your eyes and ensure they are hydrated", "critical")         #notify the user that their eyes are red
            self.notificationTime = np.datetime64('now')
            
    def __init__(self, notifier) -> None:
        self.notifier = notifier                                #initialize the notifier class 
        self.notificationTime = np.datetime64('now')            #initialize the notification time to the current time 
        self.notificationDelay = 20                             #set the notification delay to 20 seconds for rapid blinking notifications 