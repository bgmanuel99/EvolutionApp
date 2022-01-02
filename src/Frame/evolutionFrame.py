from tkinter import *

class EvolutionFrame(Frame):

    def __init__(self, root):
        Frame.__init__(self, root, width=900, height=500)
        self.config(bg="gray40")

        self.evolution = Canvas(self)
        self.evolution.pack(expand=True, fill=BOTH)