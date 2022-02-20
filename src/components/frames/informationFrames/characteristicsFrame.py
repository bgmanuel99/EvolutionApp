from tkinter import *

class CharacteristicsFrame(Frame):

    """This is the characteristics terminal from which the user will see all the species of the evolution frame and their real-time characteristics"""

    def __init__(self, root):
        Frame.__init__(self, root, width=900, height=180)
        self.config(background="gray8")