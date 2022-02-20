from tkinter import *

class Species:

    """This class represents the species that will be simulated with the genetic algorithm"""
    
    def __init__(self, initializing, velocity, size, senses, energy):
        if initializing == "randomize":
            self.randomize()
        elif initializing == "values":
            self.velocity = velocity
            self.size = size
            self.senses = senses
            self.energy = energy

    def randomize(self):
        pass