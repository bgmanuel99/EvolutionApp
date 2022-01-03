from tkinter import *

class EvolutionFrame(Frame):

    def __init__(self, root):
        Frame.__init__(self, root, width=900, height=500)
        self.config(bg="gray40")

        self.evolution_frame = Canvas(self)
        self.evolution_frame.pack(expand=True, fill=BOTH, padx=4, pady=4)