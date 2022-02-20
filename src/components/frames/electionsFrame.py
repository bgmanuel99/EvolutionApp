from tkinter import *
from components.models.gradients import GradientFrame

class ElectionsFrame(Frame):

    """This frame contains the different options the user can use to change characteristics, insert new objects and start the application"""

    def __init__(self, root):
        Frame.__init__(self, root)
        self.config(bg="dark turquoise")

        self.gradient = GradientFrame(self, "magenta4", "RoyalBlue2")
        self.gradient.pack()
        self.gradient.config(bd=0, highlightthickness=0, relief='ridge')

        self.options_frame = Frame(self.gradient, width=300, height=500)
        self.options_frame.pack(fill=BOTH, padx=2, pady=2)
        self.options_frame.configure(background="gray8")

        """ self.start_button = Button(self.options_frame)
        self.start_button.pack(expand=True, fill=BOTH, side=BOTTOM, anchor=S) """