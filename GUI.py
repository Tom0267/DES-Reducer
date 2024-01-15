import customtkinter
import tkinter

customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("green")
root = customtkinter.CTk()
root.geometry("700x450")

class framePannel:
    def __init__(self, master):
        self.master = master
        self.frame = customtkinter.CTkFrame(master)
        self.frame.pack(pady = 20, padx = 60, fill ='both', expand = True)

















def login():
    print("Login Successful")

frame = customtkinter.CTkFrame(root)
frame.pack(pady = 20, padx = 60, fill ='both', expand = True)

label = customtkinter.CTkLabel(master = frame, text = "Configure App", font = ("Helvetica", 15))
label.pack(pady = 12, padx = 10)

entry1 = customtkinter.CTkEntry(master = frame, placeholder_text = "Username")
entry1.pack(pady = 12, padx = 10)

entry2 = customtkinter.CTkEntry(master = frame, placeholder_text ="Password")
entry2.pack(pady = 12, padx = 10)

button = customtkinter.CTkButton(master = frame, text ='Blinks', command = login, hover_color = "blue")
button.pack(pady = 12, padx = 10)

button = customtkinter.CTkButton(master = frame, text ='Squints', command = login, hover_color = "blue")
button.pack(pady = 12, padx = 10)

root.mainloop()