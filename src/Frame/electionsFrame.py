import os
from tkinter import *
from PIL import ImageTk, Image

class ElectionsFrame(Frame):

    def __init__(self, root):
        Frame.__init__(self, root, width=300, height=700)
        self.config(bg="gray40")

        # The top frame with the different options the user can use to change characteristics, insert new objects and start the application
        self.options_frame = Frame(self, width=300, height=500)
        self.options_frame.pack(fill=BOTH, padx=2, pady=(2, 0))
        self.options_frame.configure(background="blue")

        # The bottom frame which consist of the different buttons to change in between environments
        self.environment_frame = Frame(self, width=300, height=200)
        self.environment_frame.pack(fill=BOTH, padx=2, pady=2)
        self.environment_frame.configure(background="gray40")

        # Polar Frame, Image and Button
        self.polar_environment_frame = Frame(self.environment_frame, width=300, height=66)
        self.polar_environment_frame.pack(fill=BOTH, pady=2)
        self.polar_environment_frame.config(background="gray70")

        self.polar_image = ImageTk.PhotoImage(Image.open(os.getcwd().replace("\\", "/")[0:-3] + "/images/environment/polar.png"))
        self.polar_image_label = Label(self.polar_environment_frame, image=self.polar_image)
        self.polar_image_label.place(x=2, y=2, width=130, height=62)

        self.polar_button = Button(self.polar_environment_frame, text="POLAR")
        self.polar_button.place(x=132, y=2, width=166, height=62)
        self.polar_button.config(font=("Terminal"))

        # Mediterranean Frame, Image and Button
        self.mediterranean_environment_frame = Frame(self.environment_frame, width=300, height=65)
        self.mediterranean_environment_frame.pack(fill=BOTH, pady=(0, 2))
        self.mediterranean_environment_frame.config(background="gray80")

        self.mediterranean_image = ImageTk.PhotoImage(Image.open(os.getcwd().replace("\\", "/")[0:-3] + "images/environment/mediterranean.png"))
        self.mediterranean_image_label = Label(self.mediterranean_environment_frame, image=self.mediterranean_image)
        self.mediterranean_image_label.place(x=2, y=2, width=130, height=62)

        self.mediterranean_button = Button(self.mediterranean_environment_frame, text="MEDITERRANEAN")
        self.mediterranean_button.place(x=132, y=2, width=166, height=62)
        self.mediterranean_button.config(font=("Terminal"))

        # Desert Frame, Image and Button
        self.desert_environment_frame = Frame(self.environment_frame, width=300, height=65)
        self.desert_environment_frame.pack(fill=BOTH)
        self.desert_environment_frame.config(background="gray90")

        self.desert_image = ImageTk.PhotoImage(Image.open(os.getcwd().replace("\\", "/")[0:-3] + "images/environment/desert.png"))
        self.desert_image_label = Label(self.desert_environment_frame, image=self.desert_image)
        self.desert_image_label.place(x=2, y=2, width=130, height=62)

        self.desert_button = Button(self.desert_environment_frame, text="DESERT")
        self.desert_button.place(x=132, y=2, width=166, height=62)
        self.desert_button.config(font=("Terminal"))