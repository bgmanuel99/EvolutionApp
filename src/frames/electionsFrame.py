from tkinter import *

class ElectionsFrame(Frame):

    def __init__(self, root):
        Frame.__init__(self, root)
        self.config(bg="dark turquoise")

        # This frame contains the different options the user can use to change characteristics, insert new objects and start the application
        self.options_frame = Frame(self, width=300, height=500)
        self.options_frame.pack(fill=BOTH, padx=2, pady=2)
        self.options_frame.configure(background="blue")