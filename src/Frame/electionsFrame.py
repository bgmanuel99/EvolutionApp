from tkinter import *

class ElectionsFrame(Frame):

    def __init__(self, root):
        Frame.__init__(self, root)
        self.config(bg="gray40")

        self.options_frame = Frame(self, width=380, height=500)
        self.options_frame.pack(fill=BOTH, padx=2, pady=(2, 0))
        self.options_frame.configure(background="blue")

        self.environment_frame = Frame(self, width=380, height=200)
        self.environment_frame.pack(fill=BOTH, padx=2, pady=2)
        self.environment_frame.configure(background="orange")