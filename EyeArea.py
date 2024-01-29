from scipy.spatial import distance as dist
class Eyes:
    def eyeAspectRatio(self, eye):
        A = dist.euclidean(eye[1], eye[5])                      #calculate the euclidean distance between the vertical eye landmark (x, y)-coordinates
        B = dist.euclidean(eye[2], eye[4])                      #calculate the euclidean distance between the vertical eye landmark (x, y)-coordinates
        C = dist.euclidean(eye[0], eye[3])  					#calculate the euclidean distance between the horizontal eye landmark (x, y)-coordinates
        ear = (A + B) / (2.0 * C)  		 						#calculate the eye aspect ratio
        return ear