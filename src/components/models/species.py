import random
from tkinter import *

class Species:

    """This class represents the species that will be simulated with the genetic algorithm"""
    
    def __init__(self, size, velocity):
        self.size = size
        self.velocity = velocity
        self.energy = 0
        self.movement_time = 0
        self.time_to_switch_movement = random.randint(3000, 4500)
        self.food_pieces = 0

    def add_movement_time(self, time):
        self.movement_time += time

    def restart_movement_time(self):
        self.movement_time = 0

    def restart_switch_movement_time(self):
        self.time_to_switch_movement = random.randint(3000, 4500)

    def set_velocity(self, velocity):
        self.velocity = velocity

    def add_piece(self):
        self.food_pieces += 1