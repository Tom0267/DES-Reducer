import numpy as np
import time
class breakTime:
    def checkBreak(self):
        currentTime = np.datetime64('now')
        if currentTime - self.break1 >=  1200:            #check if the time between breaks is greater than 20 minutes
            self.notifier.show_toast("Take A Break", "You have been working for 20 minutes. Take a break to rest your eyes.", duration=5, threaded=True)
            self.break1 = currentTime  
            
    def __init__(self, notifier):
        self.notifier = notifier
        self.break1 = np.datetime64('now')