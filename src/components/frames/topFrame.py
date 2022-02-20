from tkinter import *
from components.frames.evolutionFrame import EvolutionFrame
from components.frames.electionsFrame import ElectionsFrame
from components.frames.informationFrame import InformationFrame
from components.frames.environmentFrame import EnvironmentFrame

class TopFrame(Frame):

    """The top frame is the main frame of the application and contains the main logic"""

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