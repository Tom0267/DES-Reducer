import customtkinter
import tkinter
from imutils.video import FileVideoStream
from imutils.video import VideoStream
from PIL import Image, ImageTk
from imutils import face_utils
from time import time
from Config import config
import numpy as np
import threading
import imutils
import time
import dlib
import cv2
import csv

class GUI(customtkinter.CTk):
    def videoLoop(self):   
        frame = self.vs.read() 
        frame = imutils.resize(frame, height = 500, width=450)
        frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        captured_image = Image.fromarray(frame) 
        photo_image = ImageTk.PhotoImage(image=captured_image) 
        self.label_widget.photo_image = photo_image 
        self.label_widget.configure(image=photo_image) 
        self.label_widget.after(10, self.videoLoop) 

    def start(self):
        self.videoLoop()
        self.app.mainloop()
        
    def onClose(self):
        self.file.close()
        self.vs.stop()
        self.app.quit()
        self.app.destroy()
        
    def Blinks(self):
        self.relaxButton.configure(fg_color='#1f538d')
        self.BlinksButton.configure(fg_color='green')
        self.Description.configure(state = "normal")
        self.Description.delete("0.0", 'end')
        self.Description.insert("0.0", "Please blink 10 times to configure the blink threshold.")
        self.Description.configure(state = "disabled")
        
    
    def Relax(self):
        self.BlinksButton.configure(fg_color='#1f538d')
        self.relaxButton.configure(fg_color='green')
        self.Description.configure(state = "normal")
        self.Description.delete("0.0", 'end')
        self.Description.insert("0.0", "Please look to the center of the screen and relax while I configure.")
        self.Description.configure(state = "disabled")
        
    
    def __init__(self, detector, predictor, notifier):
        self.vs = VideoStream(src=0).start()
        
        self.file = open('Resources/configData.csv', 'w')
        self.writer = csv.writer(self.file)
        self.config = config(detector, predictor, notifier)
        
        
        self.app = customtkinter.CTk()
        self.app.protocol("WM_DELETE_WINDOW", self.onClose)
        customtkinter.set_appearance_mode('system')
        customtkinter.set_default_color_theme('dark-blue')
        self.app.title("Eye Care")
        self.app.geometry("1000x800")
        
        self.leftFrame = customtkinter.CTkFrame(self.app)
        self.leftFrame.pack(side='left', fill='y')
        self.rightFrame = customtkinter.CTkFrame(self.app)
        self.rightFrame.pack(side='right', fill='y')
        self.middleFrame = customtkinter.CTkFrame(self.app)
        self.middleFrame.pack(side='top', fill='both')
        
        
        self.ButtonFrame = customtkinter.CTkFrame(self.leftFrame)
        self.ButtonFrame.pack(side='left', fill='y', pady=10, padx=10)
        self.ImageFrame = customtkinter.CTkFrame(self.rightFrame)
        self.ImageFrame.pack(side='right', fill='y', pady=10, padx=10)
        self.VideoFrame = customtkinter.CTkFrame(self.middleFrame)
        self.VideoFrame.pack(side='top',fill='x', pady=10, padx=10)
        self.TextFrame = customtkinter.CTkFrame(self.middleFrame)
        self.TextFrame.pack(fill='both', pady=10, padx=10)
        

        self.label_widget = customtkinter.CTkLabel(self.VideoFrame, text="") 
        self.label_widget.pack() 
        self.ConfigureButton = customtkinter.CTkButton(self.middleFrame, text="Configure", command= self.config.configure, hover_color='blue')
        self.ConfigureButton.pack(padx=10, pady=10,)
        self.BlinksButton = customtkinter.CTkButton(self.ButtonFrame, text="Configure Blinks", command= self.Blinks, hover_color='blue') 
        self.BlinksButton.pack(padx=10, pady=10) 
        self.relaxButton = customtkinter.CTkButton(self.ButtonFrame, text="Configure Relax", command= self.Relax, hover_color='blue')
        self.relaxButton.pack(padx=10, pady=10)
        
        self.Description = customtkinter.CTkTextbox(self.TextFrame)
        self.Description.insert('0.0',"Please align the monitor at eye level 2ft away from your face then select a configuration option on the left pannel to begin.")
        self.Description.configure(state='disabled', wrap = 'word', font = ('Arial', 20))
        self.Description.pack(padx=10, pady=10, fill='both')
        
        self.start()
            