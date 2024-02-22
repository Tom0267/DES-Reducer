from PIL import Image, ImageTk
from Posture import Postures
from Config import config
import customtkinter
import tkinter                      #may be able to remove this import
import cv2

class GUI(customtkinter.CTk):
    def checkCamera(self):
        if not self.cap.isOpened():															    #check if the video stream was opened correctly
            self.notifier.notify("Cannot open camera", "Ensure your camera is connected.", "critical")		#display tray notification
            exit()																			            #exit the program
        
    def videoLoop(self):   
        self.checkCamera()                                                                      #check if the camera is connected
        ret, frame = self.cap.read()                                                            #read the frame from the threaded video stream
        frame = cv2.resize(frame, (450, 350))                                                   #resize the frame                     
        frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)                                           #convert the frame from BGR to RGB
        captured_image = Image.fromarray(frame)                                                 #convert the frame to an image
        photo_image = ImageTk.PhotoImage(image=captured_image)                                  #convert the image to a tkinter image 
        self.label_widget.configure(image=photo_image)                                          #configure the label to display the image
        self.label_widget.after(10, self.videoLoop)                                             #call the video loop after 10ms

    def start(self):
        self.videoLoop()                                                                        #start the video loop
        self.app.mainloop()                                                                     #start the GUI loop                                      
        
    def onClose(self):       
        self.cap.release()                                                                      #release the camera                
        self.app.quit()                                                                         #close the GUI
        self.app.destroy()                                                                      #destroy the GUI                          
        
    def Blinks(self):
        self.relaxButton.configure(fg_color='#1f538d')                                              #change the color of the relax button
        self.BlinksButton.configure(fg_color='green')                                               #change the color of the blink button
        self.Description.configure(state = "normal")                                                #enable editing textbox 
        self.Description.delete("0.0", 'end')                                                       #clear the textbox             
        self.Description.insert("0.0", "Please close your eyes.\nA notification will appear when configuration is complete\nPress Configure to begin.")   #display instructions
        self.Description.configure(state = "disabled")                                              #disable editing textbox
        self.ConfigureButton.configure(command = self.config.configureBlinks)                       #change the command of the configure button to configure blinks
    
    def Relax(self):
        self.BlinksButton.configure(fg_color='#1f538d')                                                                                       #change the color of the blink button
        self.relaxButton.configure(fg_color='green')                                                                                          #change the color of the relax button
        self.Description.configure(state = "normal")                                                                                          #enable editing textbox 
        self.Description.delete("0.0", 'end')                                                                                                 #clear the textbox                     
        self.Description.insert("0.0", "Please look to the center of the screen and relax while I configure.\nPress Configure to begin.")      #display instructions
        self.Description.configure(state = "disabled")                                                                                        #disable editing textbox                      
        self.ConfigureButton.configure(command = self.config.configureRelax)                                                                  #change the command of the configure button to configure relax
        
    def postures(self):
        self.BlinksButton.configure(fg_color='#1f538d')                                                                                       #change the color of the blink button
        self.relaxButton.configure(fg_color='#1f538d')                                                                                        #change the color of the relax button
        self.postureButton.configure(fg_color='green')                                                                                        #change the color of the posture button
        self.Description.configure(state = "normal")                                                                                          #enable editing textbox 
        self.Description.delete("0.0", 'end')                                                                                                 #clear the textbox                     
        self.Description.insert("0.0", "Please sit up straight and look to the center of the screen while I configure.\nPress Configure to begin.")      #display instructions
        self.Description.configure(state = "disabled")                                                                                        #disable editing textbox                      
        self.ConfigureButton.configure(command = self.config.configurePostures)                                                               #change the command of the configure button to configure postures
    
    def __init__(self, detector, predictor, notifier) -> None:
        self.cap = cv2.VideoCapture(0)                                              #start the video stream thread
        self.notifier = notifier                                                    #initialize the notifier class
        self.posture = Postures(notifier, False)                                    #initialize the posture class
        self.config = config(detector, predictor, self.cap, notifier, self.posture)       #initialize the config class
        self.app = customtkinter.CTk()                                              #initialize the customTKinter class                  
        self.app.protocol("WM_DELETE_WINDOW", self.onClose)                         #set the protocol for closing the GUI
        customtkinter.set_appearance_mode('system')                                 #set the appearance mode to system   
        customtkinter.set_default_color_theme('dark-blue')                          #set the default color theme to dark blue
        self.app.title("Eye Care Configurator")                                     #set the title of the GUI         
        self.app.geometry("1000x800")                                               #set the size of the GUI
        
        self.leftFrame = customtkinter.CTkFrame(self.app)                           #create the left frame
        self.leftFrame.pack(side='left', fill='y')                                  #add the left frame to the GUI
        self.rightFrame = customtkinter.CTkFrame(self.app)                          #create the right frame
        self.rightFrame.pack(side='right', fill='y')                                #add the right frame to the GUI
        self.middleFrame = customtkinter.CTkFrame(self.app)                         #create the middle frame
        self.middleFrame.pack(side='top', fill='both')                              #add the middle frame to the GUI  
        
        self.ButtonFrame = customtkinter.CTkFrame(self.leftFrame)                   #create the button frame
        self.ButtonFrame.pack(side='left', fill='y', pady=10, padx=10)              #add the button frame to the left frame
        self.ImageFrame = customtkinter.CTkFrame(self.rightFrame)                   #create the image frame
        self.ImageFrame.pack(side='right', fill='y', pady=10, padx=10)              #add the image frame to the right frame
        self.VideoFrame = customtkinter.CTkFrame(self.middleFrame)                  #create the video frame
        self.VideoFrame.pack(side='top',fill='x', pady=10, padx=10)                 #add the video frame to the middle frame
        self.TextFrame = customtkinter.CTkFrame(self.middleFrame)                   #create the text frame
        self.TextFrame.pack(fill='both', pady=10, padx=10)                          #add the text frame to the middle frame   
        
        self.label_widget = customtkinter.CTkLabel(self.VideoFrame, text="")        #create the label widget
        self.label_widget.pack()                                                    #add the label widget to the video frame
        self.ConfigureButton = customtkinter.CTkButton(self.middleFrame, text="Configure", command= None, hover_color='blue')                       #create the configure button
        self.ConfigureButton.pack(padx=10, pady=10,)                                                                                                #add the configure button to the middle frame
        self.BlinksButton = customtkinter.CTkButton(self.ButtonFrame, text="Configure Blinks", command= self.Blinks, hover_color='blue')            #create the blink button
        self.BlinksButton.pack(padx=10, pady=10)                                                                                                    #add the blink button to the button frame
        self.relaxButton = customtkinter.CTkButton(self.ButtonFrame, text="Configure Relax", command= self.Relax, hover_color='blue')               #create the relax button
        self.relaxButton.pack(padx=10, pady=10)                                                                                                     #add the relax button to the button frame
        self.postureButton = customtkinter.CTkButton(self.ButtonFrame, text="Configure Postures", command= self.postures, hover_color='blue')       #create the posture button
        self.postureButton.pack(padx=10, pady=10)                                                                                                   #add the posture button to the button frame
        
        self.Description = customtkinter.CTkTextbox(self.TextFrame)                                                                                 #create the textbox
        self.Description.insert('0.0',"Please align the monitor just below eye level 2ft away from your face then select a configuration option on the left pannel to begin.")      #add the instructions to the textbox
        self.Description.configure(state='disabled', wrap = 'word', font = ('Arial', 20))                      #configure the textbox
        self.Description.pack(padx=10, pady=10, fill='both')                                                   #add the textbox to the text frame
        
        self.start()                                                                                           #start the GUI