import mediapipe as mp
import cv2

class Postures:
  def checkPosture(self, frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    self.results = self.pose.process(frame)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    if self.results.pose_landmarks:
      self.mp_drawing.draw_landmarks(frame, self.results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)
    cv2.imshow('Posture', frame)
 
  def __init__(self, notifier):
    self.notifier = notifier
    self.mp_drawing = mp.solutions.drawing_utils
    self.mp_pose = mp.solutions.pose
    self.pose = self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)