from tkinter import *

class ElectionsFrame(Frame):

    def __init__(self, root):
        Frame.__init__(self, root, width=380, height=700)
        self.config(bg="blue2", padx=5, pady=5)