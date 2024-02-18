import numpy as np
import cv2

class Redness:
    
    def getRedness(self, roi):
        b, g, r = cv2.split(roi)                            #split the roi into its BGR components
        redness = (r - ((g + b) / 2))                       #calculate the redness of the roi
        redness = np.mean(redness)                          #get the average redness of the roi
        return redness                                      #return the redness of the roi
    
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
        if (leftRedness > 50 or rightRedness > 50) and (self.notificationTime - np.datetime64('now') >= self.notificationDelay):     #check if the redness of the eyes is greater than 50 and the time since the last notification is greater than 20 seconds
            self.notifier.notify("Red Eyes", "if your eyes are getting red, Take a break to rest your eyes and ensure they are hydrated", "critical")         #notify the user that their eyes are red
            self.notificationTime = np.datetime64('now')
            
    def __init__(self, notifier):
        self.notifier = notifier                                #initialize the notifier class 
        self.notificationTime = np.datetime64('now')            #initialize the notification time to the current time 
        self.notificationDelay = 20                             #set the notification delay to 20 seconds for rapid blinking notifications 