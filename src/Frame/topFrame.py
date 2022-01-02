from tkinter import *
from frame.evolutionFrame import EvolutionFrame
from frame.electionsFrame import ElectionsFrame
from frame.informationFrame import InformationFrame

# The TopFrame is the main frame of the app and contains all the others
class TopFrame(Frame):

    def __init__(self, root):
        Frame.__init__(self, root)
        self.config(bg="gray8")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.elections_frame = ElectionsFrame(self)
        self.elections_frame.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=2, pady=2)

        self.evolution_frame = EvolutionFrame(self)
        self.evolution_frame.grid(row=0, column=1, sticky="nsew", padx=(0, 2), pady=2)

        self.information_frame = InformationFrame(self)
        self.information_frame.grid(row=1, column=1, sticky="nsew", padx=(0, 2), pady=(0, 2))