import mediapipe as mp
import math
import cv2

class Postures:
  def findAngle(self, x1, y1, x2, y2):
    theta = math.acos((y2 -y1)*(-y1) / (math.sqrt((x2 - x1)**2 + (y2 - y1)**2) * y1))                 #calculate the angle between the two points
    degree = int(180/math.pi)*theta                                                                   #convert the angle to degrees
    return degree
  
  def checkOnScreen(self, landmark):
    x, y = int(landmark.x * self.width), int(landmark.y * self.height)
    return 0 <= x < self.width and 0 <= y < self.height
  
  def checkElbows(self):
    left_elbow = self.imagePoints.landmark[self.keyPoints.LEFT_ELBOW]
    right_elbow = self.imagePoints.landmark[self.keyPoints.RIGHT_ELBOW]
    print(left_elbow and self.checkOnScreen(left_elbow) and right_elbow and self.checkOnScreen(right_elbow))
    if left_elbow and self.checkOnScreen(left_elbow) and right_elbow and self.checkOnScreen(right_elbow):
      self.notifier.show_toast("Stretching Detected", "If you're tired or uncomfortable, consider taking break.", duration=5, threaded=True)		#display tray notification
  
  def landmarkCoordinates(self):
    self.leftShldr_x = int(self.imagePoints.landmark[self.keyPoints.LEFT_SHOULDER].x * self.width)      #get the x coordinates for the left shoulder
    self.leftShldr_y = int(self.imagePoints.landmark[self.keyPoints.LEFT_SHOULDER].y * self.height)     #get the y coordinates for the left shoulder
    
    self.rightShldr_x = int(self.imagePoints.landmark[self.keyPoints.RIGHT_SHOULDER].x * self.width)     #get the x coordinates for the right shoulder
    self.rightShldr_y = int(self.imagePoints.landmark[self.keyPoints.RIGHT_SHOULDER].y * self.height)    #get the y coordinates for the right shoulder
    
    self.leftEar_x = int(self.imagePoints.landmark[self.keyPoints.LEFT_EAR].x * self.width)         #get the x coordinates for the left ear
    self.leftEar_y = int(self.imagePoints.landmark[self.keyPoints.LEFT_EAR].y * self.height)        #get the y coordinates for the left ear
    
    self.rightEar_x = int(self.imagePoints.landmark[self.keyPoints.RIGHT_EAR].x * self.width)        #get the x coordinates for the right ear
    self.rightEar_y = int(self.imagePoints.landmark[self.keyPoints.RIGHT_EAR].y * self.height)       #get the y coordinates for the right ear
    
    self.nose_x = int(self.imagePoints.landmark[self.keyPoints.NOSE].x * self.width)              #get the x coordinates for the nose
    self.nose_y = int(self.imagePoints.landmark[self.keyPoints.NOSE].y * self.height)             #get the y coordinates for the nose
    
    self.leftElbow_x = int(self.imagePoints.landmark[self.keyPoints.LEFT_ELBOW].x * self.width)     #get the x coordinates for the left elbow
    self.leftElbow_y = int(self.imagePoints.landmark[self.keyPoints.LEFT_ELBOW].y * self.height)    #get the y coordinates for the left elbow
    
    self.rightElbow_x = int(self.imagePoints.landmark[self.keyPoints.RIGHT_ELBOW].x * self.width)    #get the x coordinates for the right elbow
    self.rightElbow_y = int(self.imagePoints.landmark[self.keyPoints.RIGHT_ELBOW].y * self.height)   #get the y coordinates for the right elbow
  
  def checkPosture(self, frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)                                                #convert the frame from BGR to RGB    
    self.results = self.pose.process(frame)                                                       #get the landmarks from the frame
    self.imagePoints = self.results.pose_landmarks                                                #get the landmarks from the frame    
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)                                                #convert the frame from RGB to BGR
    if self.results.pose_landmarks:
      self.landmarkCoordinates()                                                                         #get the coordinates for the landmarks 
    
      neckAngle = self.findAngle(self.leftShldr_x, self.leftShldr_y, self.leftEar_x, self.leftEar_y)          #calculate the angle between the left shoulder and left ear
      torsoAngle = self.findAngle(self.nose_x, self.nose_y, self.leftShldr_x, self.leftShldr_y)               #calculate the angle between the nose and left shoulder

      cv2.circle(frame, (self.leftShldr_x, self.leftShldr_y), 5, (255, 0, 0), -1)                           #draw the circles for the left shoulder
      cv2.circle(frame, (self.rightShldr_x, self.rightShldr_y), 5, (255, 0, 0), -1)                         #draw the circles for the right shoulder
      cv2.circle(frame, (self.leftEar_x, self.leftEar_y), 5, (255, 0, 0), -1)                               #draw the circles for the left ear
      cv2.circle(frame, (self.rightEar_x, self.rightEar_y), 5, (255, 0, 0), -1)                             #draw the circles for the right ear
      cv2.circle(frame, (self.nose_x, self.nose_y), 5, (255, 0, 0), -1)                                     #draw the circles for the nose
      cv2.circle(frame, (self.leftElbow_x, self.leftElbow_y), 5, (255, 0, 0), -1)                           #draw the circles for the left elbow
      cv2.circle(frame, (self.rightElbow_x, self.rightElbow_y), 5, (255, 0, 0), -1)                         #draw the circles for the right elbow  
      
      self.checkElbows()                                                                                   #check if the user is stretching
      
      if neckAngle > 26 and neckAngle < 29 and torsoAngle > 136 and torsoAngle < 139:               #check if the user has good posture (angles determined experimentally)
        status = 'Good Posture'                                                                     #set the status to good posture   
        lineColor = (0, 255, 0)                                                                     #set the line color to green if the user has good posture  
      else:
        status = 'Bad Posture'                                                               #set the status to bad posture 
        lineColor = (0, 0, 255)                                                              #set the line color to red if the user has bad posture
        self.badFrames += 1                                                                  #increment the bad posture frames counter
        if self.badFrames >= 15:
          self.notifier.show_toast("Bad Posture Detected", "Ensure you are sitting up straight.", duration=5, threaded=True)		#display tray notification
          self.badFrames = 0                                                                                   #reset the bad posture frames counter    
        
      cv2.putText(frame, status, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, lineColor, 2)                                     #display the status of the user's posture
      cv2.line(frame, (self.leftShldr_x, self.leftShldr_y), (self.leftEar_x, self.leftEar_y), lineColor, 4)                 #draw the lines between the landmarks
      cv2.line(frame, (self.leftShldr_x, self.leftShldr_y), (self.rightShldr_x, self.rightShldr_y), lineColor, 4)           #draw the lines between the landmarks
      cv2.line(frame, (self.leftShldr_x, self.leftShldr_y), (self.nose_x, self.nose_y), lineColor, 4)                       #draw the lines between the landmarks
      cv2.line(frame, (self.nose_x, self.nose_y), (self.rightShldr_x, self.rightShldr_y), lineColor, 4)                     #draw the lines between the landmarks
      cv2.line(frame, (self.rightShldr_x, self.rightShldr_y), (self.rightEar_x, self.rightEar_y), lineColor, 4)             #draw the lines between the landmarks    
    
      cv2.putText(frame, 'Neck : ' + str(int(neckAngle)) + '  Torso : ' + str(int(torsoAngle)), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)        #display neck and torse angles
    cv2.imshow('Posture', frame)          #show the frame
 
  def __init__(self, notifier):
    self.notifier = notifier                                                                            #initialize the notifier
    self.pose = mp.solutions.pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)       #initialize the pose class with the confidence values
    self.keyPoints = mp.solutions.pose.PoseLandmark                                                     #initialize the pose landmarks 
    self.badFrames = 0                                                                                  #initialize the bad posture frames counter
    self.height = 337                                                                                   #initialize the height of the frame
    self.width = 450                                                                                    #initialize the width of the frame