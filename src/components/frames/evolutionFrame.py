import os
from tkinter import *
from components.models.gradients import GradientFrame
from components.interfaces.observer import Observer
from components.interfaces.publisher import Publisher
from io import open

class EvolutionFrame(Frame, Observer):

    """This is the main application frame. Used to show the genetic algorithm in execution by recreating the species and the environments on it"""

    def __init__(self, root):
        Frame.__init__(self, root)
        self.config(bg="dark turquoise")

        self.gradient = GradientFrame(self, "magenta4", "RoyalBlue2")
        self.gradient.pack(expand=True, fill=BOTH)
        self.gradient.config(bd=0, highlightthickness=0, relief='ridge')

        self.evolution_frame = Canvas(self.gradient)
        self.evolution_frame.pack(expand=True, fill=BOTH, padx=2, pady=2)

        self.x0 = 50 - 6
        self.y0 = 50 - 6
        self.x1 = 50 + 6
        self.y1 = 50 + 6
        self.oval = self.evolution_frame.create_oval(self.x0, self.y0, self.x1, self.y1, fill="blue")
        self.x0 = 50 - 12
        self.y0 = 50 - 12
        self.x1 = 50 + 12
        self.y1 = 50 + 12
        self.oval_sense = self.evolution_frame.create_oval(self.x0, self.y0, self.x1, self.y1)

        """ self.move_species() """

    def update(self, Publisher: Publisher, *args) -> None:
        """Receive the update from the publisher"""

        if args[0] == "run":
            file = open(os.getcwd().replace("\\", "/") + "/archive/initialValuesForGeneticAlgorithm.txt", "r")
            data = file.read().split(" ")
            self.initialize(data[0], data[1], data[2])
        elif args[0] == "stop": self.stop()

    def move_species(self):
        """Continually moves the individuals of the species while the genetics algorithm is running"""
        self.evolution_frame.move(self.oval, 0.5, 0)
        self.evolution_frame.move(self.oval_sense, 0.5, 0)
        self.evolution_frame.after(10, self.move_species)

    def initialize(self, individuals, food, epochs):
        """Initialize parameters the genetics algorithm will use"""
        
        self.run()

    def run(self):
        """This function will start the execution of the genetic algorithm"""

        print("inside evolution frame run function")

    def stop(self):
        """This function will stop the execution of the genetic algorithm"""

        print("inside evolution frame stop function")