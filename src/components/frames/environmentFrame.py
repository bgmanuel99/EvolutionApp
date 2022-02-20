import os
from tkinter import *
from PIL import ImageTk, Image
from components.models.gradients import GradientFrame

class EnvironmentFrame(Frame):

    """This class contains the different buttons to change in between environments"""

    def __init__(self, root):
        Frame.__init__(self, root)
        self.config(background="dark turquoise")

        self.gradient_canvas = GradientFrame(self, "RoyalBlue2", "magenta4")
        self.gradient_canvas.pack()
        self.gradient_canvas.config(bd=0, highlightthickness=0, relief='ridge')

        # Polar Frame, Image and Button
        self.polar_environment_frame = Frame(self.gradient_canvas, width=300, height=69)
        self.polar_environment_frame.pack(fill=BOTH, padx=2, pady=2)
        self.polar_environment_frame.config(background="gray8")

        self.polar_image = ImageTk.PhotoImage(Image.open(os.getcwd().replace("\\", "/") + "/assets/images/polar.png"))
        self.polar_image_label = Label(self.polar_environment_frame, image=self.polar_image)
        self.polar_image_label.place(x=2, y=2, width=130, height=65)

        self.polar_button = Button(self.polar_environment_frame, text="POLAR")
        self.polar_button.place(x=132, y=2, width=166, height=65)
        self.polar_button.config(font=("Terminal"), background="medium purple", activebackground="medium purple")

        # Mediterranean Frame, Image and Button
        self.mediterranean_environment_frame = Frame(self.gradient_canvas, width=300, height=69)
        self.mediterranean_environment_frame.pack(fill=BOTH, padx=2)
        self.mediterranean_environment_frame.config(background="gray8")

        self.mediterranean_image = ImageTk.PhotoImage(Image.open(os.getcwd().replace("\\", "/") + "/assets/images/mediterranean.png"))
        self.mediterranean_image_label = Label(self.mediterranean_environment_frame, image=self.mediterranean_image)
        self.mediterranean_image_label.place(x=2, y=2, width=130, height=65)

        self.mediterranean_button = Button(self.mediterranean_environment_frame, text="MEDITERRANEAN")
        self.mediterranean_button.place(x=132, y=2, width=166, height=65)
        self.mediterranean_button.config(font=("Terminal"), background="aquamarine2", activebackground="aquamarine2")

        # Desert Frame, Image and Button
        self.desert_environment_frame = Frame(self.gradient_canvas, width=300, height=68)
        self.desert_environment_frame.pack(fill=BOTH, padx=2, pady=2)
        self.desert_environment_frame.config(background="gray8")

        self.desert_image = ImageTk.PhotoImage(Image.open(os.getcwd().replace("\\", "/") + "/assets/images/desert.png"))
        self.desert_image_label = Label(self.desert_environment_frame, image=self.desert_image)
        self.desert_image_label.place(x=2, y=2, width=130, height=64)

        self.desert_button = Button(self.desert_environment_frame, text="DESERT")
        self.desert_button.place(x=132, y=2, width=166, height=64)
        self.desert_button.config(font=("Terminal"), background="burlywood1", activebackground="burlywood1")