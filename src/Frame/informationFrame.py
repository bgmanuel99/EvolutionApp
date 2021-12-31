from tkinter import *
from frame.characteristicsFrame import CharacteristicsFrame

class InformationFrame(Frame):

    def __init__(self, root):
        Frame.__init__(self, root)
        self.config(bg="gray50")

        self.characteristicsFrame = CharacteristicsFrame(self)
        self.characteristicsFrame.pack(side=LEFT, anchor=W)

        