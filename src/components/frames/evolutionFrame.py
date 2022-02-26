from tkinter import *
import math
import random
from components.models.gradients import GradientFrame
from components.interfaces.observer import Observer
from components.interfaces.publisher import Publisher
from components.models.species import Species

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

        self.execution_status = False

        self.species_parameters = {}
        self.species_bodies = {}
        self.food_bodies = {}

    def update(self, Publisher: Publisher, *args) -> None:
        """Receive the update from the publisher"""
        
        if args[0] == "run":
            self.initialize(args[1][0], args[1][1], args[1][2])
        elif args[0] == "stop": self.stop()
        elif args[0] == "continue": self.run_algorithm()
        elif args[0] == "restart": self.restart()

    def move_species(self):
        """Continually moves the individuals of the species while the genetics algorithm is running"""
        
        """ self.evolution_frame.move(self.oval, 0.5, 0)
        self.evolution_frame.move(self.oval1, -0.5, 0)
        if self.wall_collision(self.oval):
            self.evolution_frame.delete("1")
            self.execution_status = False
        if self.species_collision(self.oval, self.oval1):
            self.evolution_frame.delete("1")
            self.evolution_frame.delete("3")
            self.execution_status = False """

        if self.execution_status: self.evolution_frame.after(10, self.move_species)

    def wall_collision(self, species):
        """Calculates if there is a collision between a wall of the canvas and a species bounds"""

        coords = self.evolution_frame.coords(species)
        if coords[0] < 0 or coords[1] < 0 or coords[2] > 900 or coords[3] > 500: return True

    def species_collision(self, tag1, tag2):
        """Calculates if there is a collision between two species bounds"""
        species1_coords = self.evolution_frame.coords(self.species_bodies[tag1])
        species1_size = self.species_parameters[tag1].size
        species2_coords = self.evolution_frame.coords(self.species_bodies[tag2])
        species2_size = self.species_parameters[tag2].size

        distance = math.sqrt(
            (((species1_coords[0]+species1_size) - (species2_coords[0]+species2_size)) * ((species1_coords[0]+species1_size) - (species2_coords[0]+species2_size))) + 
            (((species1_coords[1]+species1_size) - (species2_coords[1]+species2_size)) * ((species1_coords[1]+species1_size) - (species2_coords[1]+species2_size))))

        if distance < (species1_size + species2_size): return True

    def initialize(self, individuals, food, epochs):
        """Initialize the parameters the genetic algorithm will use"""

        taken_coords = {}
        self.tag_number_for_species = individuals

        # Calculate all the species parameters
        for index in range(individuals):
            size = random.randrange(6, 9)
            velocity = random.uniform(0.5, 0.7)
            
            new_coords = []
            still_collide = True
            while(still_collide):
                still_collide = False
                new_coords = [random.randrange(20, 881), random.randrange(20, 481)]

                for tag, coords in taken_coords.items():
                    if self.initialization_collisions(new_coords, coords, size, self.species_parameters[tag].size): still_collide = True

            taken_coords["S-"+str(index)] = new_coords
            self.species_parameters["S-"+str(index)] = Species(size, velocity)

        food_taken_coords = []

        # Calculate food coordinates
        for index in range(food):
            new_coords = []
            still_collide = True
            while(still_collide):
                still_collide = False
                new_coords = [random.randrange(20, 881), random.randrange(20, 481)]

                for tag, coords in taken_coords.items():
                    if self.initialization_collisions(new_coords, coords, 3, self.species_parameters[tag].size): still_collide = True

                for coords in food_taken_coords:
                    if self.initialization_collisions(new_coords, coords, 3, 3): still_collide = True
            
            food_taken_coords.append(new_coords)

        # Create the species and draw them in the canvas
        for tag, species in self.species_parameters.items():
            species_coords = taken_coords[tag]
            self.species_bodies[str(tag)] = self.evolution_frame.create_oval(
                species_coords[0]-species.size, 
                species_coords[1]-species.size, 
                species_coords[0]+species.size, 
                species_coords[1]+species.size, 
                fill="blue", 
                tags=str(tag)
            )

        # Create the food and draw them in the canvas
        for index in range(len(food_taken_coords)):
            coords = food_taken_coords[index]
            self.food_bodies["F-"+str(index)] = self.evolution_frame.create_oval(coords[0]-3, coords[1]-3, coords[0]+3, coords[1]+3, fill="green", tags="F-"+str(index))

        self.epochs = epochs

        self.run_algorithm()

    def initialization_collisions(self, coords1, coords2, species1_size, species2_size):
        """Calculates if two points in the canvas are colliding"""

        distance = math.sqrt(
            ((coords1[0] - coords2[0]) * (coords1[0] - coords2[0])) + 
            ((coords1[1] - coords2[1]) * (coords1[1] - coords2[1])))

        if distance < (species1_size + species2_size): return True

    def run_algorithm(self):
        """This function will start the execution of the genetic algorithm"""

        self.execution_status = True
        self.move_species()

    def stop(self):
        """This function will stop the execution of the genetic algorithm"""

        self.execution_status = False

    def restart(self):
        """This function restarts the genetic algorithm"""

        for tag in [tag for tag in self.species_bodies]:
            self.evolution_frame.delete(tag)

        for tag in [tag for tag in self.food_bodies]:
            self.evolution_frame.delete(tag)

        self.species_parameters = {}
        self.species_bodies = {}
        self.food_bodies = {}