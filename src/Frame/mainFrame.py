from tkinter import *

class MainFrame(Frame):

    def __init__(self, root):
        Frame.__init__(self, root, width=1280, height=700)
        self.pack(expand=True, fill=BOTH)