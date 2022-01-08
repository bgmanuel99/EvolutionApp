from tkinter import *
from frames.evolutionFrame import EvolutionFrame
from frames.electionsFrame import ElectionsFrame
from frames.informationFrame import InformationFrame
from frames.environmentFrame import EnvironmentFrame

# The TopFrame is the main frame of the app and contains all the others
class TopFrame(Frame):

    def __init__(self, root):
        Frame.__init__(self, root)
        self.config(bg="gray8")

        self.elections_frame = ElectionsFrame(self)
        self.elections_frame.grid(row=0, column=0, padx=2, pady=2)

        self.evolution_frame = EvolutionFrame(self)
        self.evolution_frame.grid(row=0, column=1, sticky="nsew", padx=(0, 2), pady=2)

        self.environment_frame = EnvironmentFrame(self)
        self.environment_frame.grid(row=1, column=0, sticky="nsew", padx=2, pady=(0, 2))

        self.information_frame = InformationFrame(self)
        self.information_frame.grid(row=1, column=1, padx=(0, 2), pady=(0, 2))