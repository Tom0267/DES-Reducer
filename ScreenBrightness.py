import cv2
import screen_brightness_control as sbc
class BrightnessControl:

    def cameraExposure(self):
        camera = cv2.VideoCapture(self.cameraIndex, cv2.CAP_DSHOW)              #initialize the camera
        camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)                            #0.25 turns OFF auto exposure         
        camera.set(cv2.CAP_PROP_EXPOSURE, self.exposureValue)                   #sets the exposure value of the camera    
        return camera

    def calculateBrightness(self, image):
        average_brightness = (cv2.mean(image)[0] / 255.0) *20               #calculate the average brightness of the image
        return average_brightness

    def setBrightness(self, brightness):
        brightness = brightness + self.brightness_offset                          #adjust brightness
        sbc.set_brightness(brightness)                                      #set brightness

    def update(self, frame):
        brightness = self.calculateBrightness(frame) * 100
        self.setBrightness(brightness)
        
    def __init__(self):
        self.brightness_offset = 20                     #adjust to offset the brightness up/down. 
        self.cameraIndex = 0                            #select camera
        self.exposureValue = 15                          #use in with brightness_offset. A lower number means lower brightness.
        self.cameraExposure()