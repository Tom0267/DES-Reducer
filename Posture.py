import mediapipe as mp
import math
import cv2

class Postures:
  def findDistance(self, x1, y1, x2, y2):
    dist = math.sqrt((x2-x1)**2+(y2-y1)**2)                                                        #calculate the distance between the two points   
    return dist
  
  def findAngle(self, x1, y1, x2, y2):
    theta = math.acos((y2 -y1)*(-y1) / (math.sqrt((x2 - x1)**2 + (y2 - y1)**2) * y1))                 #calculate the angle between the two points
    degree = int(180/math.pi)*theta                                                                   #convert the angle to degrees
    return degree
  
  def landmarkCoordinates(self):
    self.l_shldr_x = int(self.imagePoints.landmark[self.keyPoints.LEFT_SHOULDER].x * self.width)      #get the x coordinates for the left shoulder
    self.l_shldr_y = int(self.imagePoints.landmark[self.keyPoints.LEFT_SHOULDER].y * self.height)     #get the y coordinates for the left shoulder
    
    self.r_shldr_x = int(self.imagePoints.landmark[self.keyPoints.RIGHT_SHOULDER].x * self.width)     #get the x coordinates for the right shoulder
    self.r_shldr_y = int(self.imagePoints.landmark[self.keyPoints.RIGHT_SHOULDER].y * self.height)    #get the y coordinates for the right shoulder
    
    self.l_ear_x = int(self.imagePoints.landmark[self.keyPoints.LEFT_EAR].x * self.width)         #get the x coordinates for the left ear
    self.l_ear_y = int(self.imagePoints.landmark[self.keyPoints.LEFT_EAR].y * self.height)        #get the y coordinates for the left ear
    
    self.r_ear_x = int(self.imagePoints.landmark[self.keyPoints.RIGHT_EAR].x * self.width)        #get the x coordinates for the right ear
    self.r_ear_y = int(self.imagePoints.landmark[self.keyPoints.RIGHT_EAR].y * self.height)       #get the y coordinates for the right ear
    
    self.nose_x = int(self.imagePoints.landmark[self.keyPoints.NOSE].x * self.width)              #get the x coordinates for the nose
    self.nose_y = int(self.imagePoints.landmark[self.keyPoints.NOSE].y * self.height)             #get the y coordinates for the nose
  
  def checkPosture(self, frame):
    self.height, self.width = frame.shape[:2]                                                     #get the height and width of the frame
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)                                                #convert the frame from BGR to RGB    
    self.results = self.pose.process(frame)                                                       #get the landmarks from the frame
    self.imagePoints = self.results.pose_landmarks                                                #get the landmarks from the frame    
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)                                                #convert the frame from RGB to BGR
    if self.results.pose_landmarks:
      self.landmarkCoordinates()                                                                         #get the coordinates for the landmarks 
    
      neckAngle = self.findAngle(self.l_shldr_x, self.l_shldr_y, self.l_ear_x, self.l_ear_y)          #calculate the angle between the left shoulder and left ear
      torsoAngle = self.findAngle(self.nose_x, self.nose_y, self.l_shldr_x, self.l_shldr_y)           #calculate the angle between the nose and left shoulder

      cv2.circle(frame, (self.l_shldr_x, self.l_shldr_y), 5, (255, 0, 0), -1)
      cv2.circle(frame, (self.r_shldr_x, self.r_shldr_y), 5, (255, 0, 0), -1)
      cv2.circle(frame, (self.l_ear_x, self.l_ear_y), 5, (255, 0, 0), -1)
      cv2.circle(frame, (self.r_ear_x, self.r_ear_y), 5, (255, 0, 0), -1)
      cv2.circle(frame, (self.nose_x, self.nose_y), 5, (255, 0, 0), -1)
      
      if neckAngle > 26 and neckAngle < 29 and torsoAngle > 136 and torsoAngle < 139:               #check if the user has good posture (angles determined experimentally)
        status = 'Good Posture'
        lineColor = (0, 255, 0)
      else:
        status = 'Bad Posture'
        lineColor = (0, 0, 255)
        
      cv2.putText(frame, status, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, lineColor, 2)                           #display the status of the user's posture
      cv2.line(frame, (self.l_shldr_x, self.l_shldr_y), (self.l_ear_x, self.l_ear_y), lineColor, 4)               #draw the lines between the landmarks
      cv2.line(frame, (self.l_shldr_x, self.l_shldr_y), (self.r_shldr_x, self.r_shldr_y), lineColor, 4)           #draw the lines between the landmarks
      cv2.line(frame, (self.l_shldr_x, self.l_shldr_y), (self.nose_x, self.nose_y), lineColor, 4)                 #draw the lines between the landmarks
      cv2.line(frame, (self.nose_x, self.nose_y), (self.r_shldr_x, self.r_shldr_y), lineColor, 4)                 #draw the lines between the landmarks
      cv2.line(frame, (self.r_shldr_x, self.r_shldr_y), (self.r_ear_x, self.r_ear_y), lineColor, 4)               #draw the lines between the landmarks    
    
      cv2.putText(frame, 'Neck : ' + str(int(neckAngle)) + '  Torso : ' + str(int(torsoAngle)), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)        #display neck and torse angles
    cv2.imshow('Posture', frame)          #show the frame
 
  def __init__(self, notifier):
    self.notifier = notifier                                                                            #initialize the notifier
    self.pose = mp.solutions.pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)       #initialize the pose class with the confidence values
    self.keyPoints = mp.solutions.pose.PoseLandmark                                                     #initialize the pose landmarks 