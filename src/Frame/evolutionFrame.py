from tkinter import *

class EvolutionFrame(Frame):

    def __init__(self, root):
        Frame.__init__(self, root, width=980, height=500)
        self.config(bg="dark turquoise")

        self.evolution_frame = Canvas(self)
        self.evolution_frame.pack(expand=True, fill=BOTH, padx=2, pady=2)