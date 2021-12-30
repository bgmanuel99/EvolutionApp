from tkinter import *

class InformationFrame(Frame):

    def __init__(self, root):
        Frame.__init__(self, root, width=900, height=200)
        self.config(bg="magenta", padx=5, pady=5)