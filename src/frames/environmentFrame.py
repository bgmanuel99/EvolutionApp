import os
from tkinter import *
from PIL import ImageTk, Image

# This class contains the different buttons to change in between environments
class EnvironmentFrame(Frame):

    def __init__(self, root):
        Frame.__init__(self, root)
        self.config(background="dark turquoise")

        # Polar Frame, Image and Button
        self.polar_environment_frame = Frame(self, width=300, height=69)
        self.polar_environment_frame.pack(fill=BOTH, padx=2, pady=2)
        self.polar_environment_frame.config(background="blue")

        self.polar_image = ImageTk.PhotoImage(Image.open(os.getcwd().replace("\\", "/")[0:-3] + "/images/environment/polar.png"))
        self.polar_image_label = Label(self.polar_environment_frame, image=self.polar_image)
        self.polar_image_label.place(x=2, y=2, width=130, height=65)

        self.polar_button = Button(self.polar_environment_frame, text="POLAR")
        self.polar_button.place(x=132, y=2, width=166, height=65)
        self.polar_button.config(font=("Terminal"))

        # Mediterranean Frame, Image and Button
        self.mediterranean_environment_frame = Frame(self, width=300, height=69)
        self.mediterranean_environment_frame.pack(fill=BOTH, padx=2)
        self.mediterranean_environment_frame.config(background="blue")

        self.mediterranean_image = ImageTk.PhotoImage(Image.open(os.getcwd().replace("\\", "/")[0:-3] + "images/environment/mediterranean.png"))
        self.mediterranean_image_label = Label(self.mediterranean_environment_frame, image=self.mediterranean_image)
        self.mediterranean_image_label.place(x=2, y=2, width=130, height=65)

        self.mediterranean_button = Button(self.mediterranean_environment_frame, text="MEDITERRANEAN")
        self.mediterranean_button.place(x=132, y=2, width=166, height=65)
        self.mediterranean_button.config(font=("Terminal"))

        # Desert Frame, Image and Button
        self.desert_environment_frame = Frame(self, width=300, height=68)
        self.desert_environment_frame.pack(fill=BOTH, padx=2, pady=2)
        self.desert_environment_frame.config(background="blue")

        self.desert_image = ImageTk.PhotoImage(Image.open(os.getcwd().replace("\\", "/")[0:-3] + "images/environment/desert.png"))
        self.desert_image_label = Label(self.desert_environment_frame, image=self.desert_image)
        self.desert_image_label.place(x=2, y=2, width=130, height=64)

        self.desert_button = Button(self.desert_environment_frame, text="DESERT")
        self.desert_button.place(x=132, y=2, width=166, height=64)
        self.desert_button.config(font=("Terminal"))