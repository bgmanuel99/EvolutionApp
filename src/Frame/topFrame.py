from tkinter import *
from frame.evolutionFrame import EvolutionFrame
from frame.electionsFrame import ElectionsFrame
from frame.informationFrame import InformationFrame

class TopFrame(Frame):

    def __init__(self, root):
        Frame.__init__(self, root)
        self.config(bg="gray60")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.elections_frame = ElectionsFrame(self)
        self.elections_frame.grid(row=0, column=0, rowspan=2)

        self.evolution_frame = EvolutionFrame(self)
        self.evolution_frame.grid(row=0, column=1)

        self.information_frame = InformationFrame(self)
        self.information_frame.grid(row=1, column=1)

        self.grid(sticky="nsew")