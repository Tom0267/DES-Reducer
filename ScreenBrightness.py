import screen_brightness_control as sbc
import cv2
class BrightnessControl:

    def cameraExposure(self):
        camera = cv2.VideoCapture(self.cameraIndex, cv2.CAP_DSHOW)              #initialize the camera
        camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)                            #0.25 turns OFF auto exposure         
        camera.set(cv2.CAP_PROP_EXPOSURE, self.exposureValue)                   #sets the exposure value of the camera    
        return camera

    def calculateBrightness(self, image) -> float:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)                          #convert image to hsv
        average_brightness = (cv2.mean(image)[2]/255)*200                       #calculate the average intensity value of the image
        return average_brightness                                               #returns the calculated brightness

    def setBrightness(self, brightness) -> None:
        brightness = brightness + self.brightness_offset                          #adjust brightness
        brightness = round(brightness)                                            #round value to nearest integer number
        sbc.set_brightness(brightness)                                            #set brightness

    def update(self, frame) -> None:
        brightness = self.calculateBrightness(frame)                                                    #calculate the brightness of the frame
        if brightness > 100:                                                                            #check if the brightness is greater than 150
            self.badFrames += 1                                                                         #increment the bad frames counter
            if self.badFrames > 20 and self.badFrames < 22:                                             #check if the bad frames counter is greater than 20 and less than 22
                self.notifier.notify("Screen Glare", "Adjust your screen to reduce glare.", "critical")  #display tray notification
        else:                                                                                           #if the brightness is less than 150
            self.badFrames = 0                                                                          #reset the bad frames counter
        self.setBrightness(brightness)                                                                  #call the set brightness function
        
    def __init__(self, notifier) -> None:
        self.notifier = notifier
        self.brightness_offset = 10                    #adjust to offset the brightness up/down. 
        self.cameraIndex = 0                           #select camera
        self.exposureValue = 15                        #use in with brightness_offset. A lower number means lower brightness.
        self.badFrames = 0                             #initialize the bad frames counter
        self.cameraExposure()