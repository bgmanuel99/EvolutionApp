import random
from tkinter import *

class Species:

    """This class represents the species that will be simulated with the genetic algorithm"""
    
    def __init__(self, size, velocity):
        self.size = size
        self.velocity = velocity
        self.energy = 0
        self.movement_time = 0
        self.time_to_switch_movement = random.randint(2000, 3000)