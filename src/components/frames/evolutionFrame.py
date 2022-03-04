import math
import random
from tkinter import *
from typing import List
from components.models.gradients import GradientFrame
from components.interfaces.observer import Observer
from components.interfaces.publisher import Publisher
from components.models.species import Species

class EvolutionFrame(Frame, Observer, Publisher):

    """This is the main application frame. Used to show the genetic algorithm in execution by recreating the species and the environments on it"""

    def __init__(self, root):
        Frame.__init__(self, root)
        self.config(bg="dark turquoise")

        self._observers: List[Observer] = []

        self.gradient = GradientFrame(self, "magenta4", "RoyalBlue2")
        self.gradient.pack(expand=True, fill=BOTH)
        self.gradient.config(bd=0, highlightthickness=0, relief='ridge')

        self.evolution_frame = Canvas(self.gradient)
        self.evolution_frame.pack(expand=True, fill=BOTH, padx=2, pady=2)

        self.execution_status = False

        self.species_parameters = {}
        self.species_bodies = {}
        self.food_bodies = {}

        self.type_of_notification = ""
        self.message = ""
        self.extra_message_data = []

    def update(self, Publisher: Publisher, *args) -> None:
        """Receive the update from the publisher"""
        
        if args[0] == "run":
            self.prepare_notification("message", "Initializing values to start the algorithm...", ["gray70", 0, 0, False])
            self.initialize(args[1][0], args[1][1], args[1][2])
            self.prepare_notification("message", " Done", ["gray70", 0, 1, False])
        elif args[0] == "stop":
            self.stop()
            self.prepare_notification("message", "Algorithm stopped", ["gray70", 1, 1, False])
        elif args[0] == "continue":
            self.run_algorithm()
            self.prepare_notification("message", "Cotinuing algorithm execution", ["gray70", 1, 1, False])
        elif args[0] == "restart":
            self.restart()
            self.prepare_notification("message", "Restarting the execution of the algorithm", ["gray70", 1, 2, True])

    def subscribe(self, observer: Observer) -> None:
        """Subscribes an observer to the publisher"""

        self._observers.append(observer)

    def unsubscribe(self, observer: Observer) -> None:
        """Unsubscribes an observer from the publisher"""

        self._observers.remove(observer)

    def notify(self) -> None:
        """Notify all observer about an event"""

        if self.type_of_notification == "message":
            for observers in self._observers:
                observers.update(self, self.type_of_notification, self.message, self.extra_message_data)

    def move_species(self):
        """Continually moves the individuals of the species while the genetics algorithm is running"""

        for tag, species_body in self.species_bodies.items():
            species_object: Species = self.species_parameters[tag]
            species_velocity = species_object.velocity
            self.evolution_frame.move(species_body, species_velocity[0], species_velocity[1])

            species_object.movement_time += 10
            if species_object.movement_time >= species_object.time_to_switch_movement:
                species_object.movement_time = 0
                species_object.time_to_switch_movement = random.randint(2000, 3000)
                species_object.velocity = [
                    species_velocity[0] * random.choice([-1, 1]), 
                    species_velocity[1] * random.choice([-1, 1])
                ]

            collision, wall_type = self.wall_collision(species_body)
            if collision:
                if wall_type == 0 or wall_type == 2:
                    species_object.velocity = [species_velocity[0] * -1, species_velocity[1]]
                elif wall_type == 1 or wall_type == 3:
                    species_object.velocity = [species_velocity[0], species_velocity[1] * -1]

        if self.execution_status: self.evolution_frame.after(10, self.move_species)

    def wall_collision(self, species):
        """Calculates if there is a collision between a wall of the canvas and a species bounds"""

        coords = self.evolution_frame.coords(species)
        if coords[0] < 0: return True, 0
        elif coords[1] < 0: return True, 1
        elif coords[2] > 900: return True, 2
        elif coords[3] > 500: return True, 3
        return False, 0

    def species_collision(self, tag1, tag2):
        """Calculates if there is a collision between two species bounds"""
        species1_coords = self.evolution_frame.coords(self.species_bodies[tag1])
        species1_size = self.species_parameters[tag1].size
        species2_coords = self.evolution_frame.coords(self.species_bodies[tag2])
        species2_size = self.species_parameters[tag2].size

        distance = math.sqrt(
            (((species1_coords[0]+species1_size) - (species2_coords[0]+species2_size)) * 
            ((species1_coords[0]+species1_size) - (species2_coords[0]+species2_size))) + 
            (((species1_coords[1]+species1_size) - (species2_coords[1]+species2_size)) * 
            ((species1_coords[1]+species1_size) - (species2_coords[1]+species2_size))))

        if distance < (species1_size + species2_size): return True

    def initialize(self, individuals, food, epochs):
        """Initialize the parameters the genetic algorithm will use"""

        taken_coords = {}
        self.tag_number_for_species = individuals

        # Calculate all the species parameters
        for index in range(individuals):
            size = random.randrange(6, 9)
            velocity_x = random.uniform(0.5, 0.7) * random.choice([-1, 1])
            velocity_y = random.uniform(0.5, 0.7) * random.choice([-1, 1])
            
            new_coords = []
            still_collide = True
            while(still_collide):
                still_collide = False
                new_coords = [random.randrange(20, 881), random.randrange(20, 481)]

                for tag, coords in taken_coords.items():
                    if self.initialization_collisions(new_coords, coords, size, self.species_parameters[tag].size): still_collide = True

            taken_coords["S-"+str(index)] = new_coords
            self.species_parameters["S-"+str(index)] = Species(size, [velocity_x, velocity_y])

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

        self.stop()

        for tag in [tag for tag in self.species_bodies]:
            self.evolution_frame.delete(tag)

        for tag in [tag for tag in self.food_bodies]:
            self.evolution_frame.delete(tag)

        self.species_parameters = {}
        self.species_bodies = {}
        self.food_bodies = {}

    def prepare_notification(self, type, message, extra):
        self.type_of_notification = type
        self.message = message
        self.extra_message_data = extra
        self.notify()