import math
import random
import threading
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
        self.food_size = 5

        self.type_of_notification = ""
        self.message = ""
        self.extra_message_data = []

        self.time_of_actual_epoch = 0
        self.actual_epoch = 1

        self.temp_food_tags = []
        self.all_threads_finished = 0
        
        self.wall_collision_lock = threading.Lock()
        self.species_and_food_collision_lock = threading.Lock()

    def update(self, *args) -> None:
        """Receive the update from the publisher"""
        
        if args[0] == "run":
            self.prepare_notification("message", "Initializing values to start the algorithm...", ["gray70", 0, 0, False])
            self.initialize(args[1][0], args[1][1], args[1][2])
            self.prepare_notification("message", " Done", ["gray70", 0, 1, False])
            self.prepare_notification("message", "Running epoch " + str(self.actual_epoch), ["gray70", 1, 1, False])
        elif args[0] == "stop":
            self.stop()
            self.prepare_notification("message", "Algorithm stopped at epoch " + str(self.actual_epoch), ["gray70", 1, 1, False])
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
                observers.update(self.type_of_notification, self.message, self.extra_message_data)

    def evaluate_individual(self, tag, species_body):
        """
        This function will make the pertinent calculations for each individual.
        It will compute the collisions between a individual and the walls or the food.
        And it will compute the movement of the individual as well.
        """

        species_object: Species = self.species_parameters[tag]
        species_velocity = species_object.velocity
        self.evolution_frame.move(species_body, species_velocity[0], species_velocity[1])

        # Calculate collisions between the species bodie and food
        if species_object.food_pieces != 2:
            for food_tag, food in self.food_bodies.items():
                if species_object.food_pieces == 2: break
                self.species_and_food_collision_lock.acquire()
                food_collision_response = self.species_and_food_collision(tag, food)
                self.species_and_food_collision_lock.release()
                if food_collision_response:
                    species_object.add_piece()
                    self.temp_food_tags.append(food_tag)

        # Calculate collisions between the species bodie and a wall of the canvas
        self.wall_collision_lock.acquire()
        collision, wall_type = self.wall_collision(species_body)
        self.wall_collision_lock.release()
        if collision:
            if wall_type == 0 or wall_type == 2:
                species_object.set_velocity([species_velocity[0] * -1, species_velocity[1]])
            elif wall_type == 1 or wall_type == 3:
                species_object.set_velocity([species_velocity[0], species_velocity[1] * -1])

        # Calculate time of movement switch for the species
        species_object.add_movement_time(10)
        if species_object.movement_time >= species_object.time_to_switch_movement:
            species_object.restart_movement_time()
            species_object.restart_switch_movement_time()
            species_object.set_velocity([species_velocity[0] * random.choice([-1, 1]), species_velocity[1] * random.choice([-1, 1])])

        self.all_threads_finished += 1

    def move_species(self):
        """Continually moves the individuals of the species while the genetics algorithm is running"""

        if self.execution_status:
            if self.all_threads_finished == len(self.species_bodies):
                if self.time_of_actual_epoch == 20000: self.process_next_epoch(self.actual_epoch == self.epochs)
                self.time_of_actual_epoch += 10

                for food_tag in self.temp_food_tags:
                    if food_tag not in self.food_bodies: continue
                    del(self.food_bodies[food_tag])
                    self.evolution_frame.delete(food_tag)

                self.temp_food_tags = []
                self.all_threads_finished = 0
                thread_num = 0

                for tag, species_body in self.species_bodies.items():
                    threading.Thread(name="thread{}".format(thread_num), target=self.evaluate_individual, args=(tag, species_body)).start()

                self.evolution_frame.after(10, self.move_species)
            else: self.evolution_frame.after(0, self.move_species)
    
    def process_next_epoch(self, finish=False):
        """This function will process the actual epoch data to use in the genetic algorithm"""
        
        self.prepare_notification("message", "Processing data of epoch " + str(self.actual_epoch) + " in the genetic algorithm... ", ["gray70", 0, 0, False])

        # Restart epoch timer
        self.time_of_actual_epoch = 0

        # Set next epoch
        self.actual_epoch += 1

        # Call the genetic algorithm function to process the new data
        self.genetic_algorithm()

        self.prepare_notification("message", "Done", ["gray70", 0, 1, False])

        if finish: self.prepare_notification("message", "Running epoch " + str(self.actual_epoch), ["gray70", 1, 1, False])
        else: self.prepare_notification("message", "Running epoch " + str(self.actual_epoch), ["gray70", 1, 1, False])
    
    def genetic_algorithm(self):
        """This is the main function of the genetic algorithm"""

        # Evaluate which of the individuals should survive and reproduce to the next epoch
        reproduce_individuals = self.evaluate()

        # Delete the resting food on the terrain
        for food in self.food_bodies.keys():
            self.evolution_frame.delete(food)
        self.food_bodies = {}

        # Create new individuals for the next epoch
        # Firstly the new coords for the individuals must be calculated
        taken_coords = {}
        for tag, species in self.species_bodies.items():
            species_parameters: Species = self.species_parameters[tag]
            species_coords = self.evolution_frame.coords(species)
            taken_coords[tag] = [species_coords[0]+species_parameters.size, species_coords[1]+species_parameters.size]

        new_species_parameter_tags = []
        for individual in reproduce_individuals:
            self.tag_number_for_species += 1
            size = self.mutate_size(self.species_parameters[individual].size)
            velocity = self.mutate_velocity(self.species_parameters[individual].velocity)
            
            new_coords = []
            still_collide = True
            while(still_collide):
                still_collide = False
                new_coords = [random.randrange(20, 881), random.randrange(20, 481)]

                for tag, coords in taken_coords.items():
                    if self.initialization_collisions(new_coords, coords, size, self.species_parameters[tag].size): still_collide = True
                
            taken_coords["S-"+str(self.tag_number_for_species)] = new_coords
            self.species_parameters["S-"+str(self.tag_number_for_species)] = Species(size, velocity)
            new_species_parameter_tags.append("S-"+str(self.tag_number_for_species))

        food_taken_coords = []

        # Calculate the new food coords
        for _ in range(self.number_of_food):
            new_coords = []
            still_collide = True
            while(still_collide):
                still_collide = False
                new_coords = [random.randrange(20, 881), random.randrange(20, 481)]

                for tag, coords in taken_coords.items():
                    if self.initialization_collisions(new_coords, coords, self.food_size, self.species_parameters[tag].size): still_collide = True

                for coords in food_taken_coords:
                    if self.initialization_collisions(new_coords, coords, self.food_size, self.food_size): still_collide = True
            
            food_taken_coords.append(new_coords)

        # Introduce new individuals
        for tag in new_species_parameter_tags:
            self.species_bodies[str(tag)] = self.evolution_frame.create_oval(
                taken_coords[tag][0]-self.species_parameters[tag].size, 
                taken_coords[tag][1]-self.species_parameters[tag].size, 
                taken_coords[tag][0]+self.species_parameters[tag].size, 
                taken_coords[tag][1]+self.species_parameters[tag].size, 
                fill="blue", 
                tags=str(tag)
            )

        # Introduce new food
        for index in range(len(food_taken_coords)):
            self.food_bodies["F-"+str(index)] = self.evolution_frame.create_oval(
                food_taken_coords[index][0]-self.food_size, 
                food_taken_coords[index][1]-self.food_size, 
                food_taken_coords[index][0]+self.food_size, 
                food_taken_coords[index][1]+self.food_size, 
                fill="green", 
                tags="F-"+str(index)
            )
    
    def evaluate(self):
        """
        This function will evaluate which individuals should reproduce or die.
        The ones who shall die, because did'nt get any food, will be erased.
        The ones to reproduce will be passed as a return of the function.
        """

        delete_species_tags = []
        reproduce_species_tags = []

        for tag, species in self.species_parameters.items():
            if species.food_pieces == 0: delete_species_tags.append(tag)
            elif species.food_pieces == 1: species.food_pieces = 0
            elif species.food_pieces == 2: 
                species.food_pieces = 0
                reproduce_species_tags.append(tag)

        for tag in delete_species_tags:
            del(self.species_bodies[tag])
            del(self.species_parameters[tag])
            self.evolution_frame.delete(tag)
        
        return reproduce_species_tags

    def mutate_size(self, size):
        new_size = size + random.choice([-1, 1])
        if new_size < 6 or new_size > 12: return size
        return new_size

    def mutate_velocity(self, velocity):
        new_velocity_x = velocity[0] + round(random.uniform(0.05, 0.1), 2) * random.choice([-1, 1])
        new_velocity_y = velocity[1] + round(random.uniform(0.05, 0.1), 2) * random.choice([-1, 1])
        if new_velocity_x < 0.5 or new_velocity_x > 1: new_velocity_x = velocity[0]
        if new_velocity_y < 0.5 or new_velocity_y > 1: new_velocity_y = velocity[1]
        return [new_velocity_x, new_velocity_y]

    def wall_collision(self, species):
        """Calculates if there is a collision between a wall of the canvas and a species bounds"""

        coords = self.evolution_frame.coords(species)
        if coords[0] < 0: return True, 0
        elif coords[1] < 0: return True, 1
        elif coords[2] > 900: return True, 2
        elif coords[3] > 500: return True, 3
        return False, 0

    def species_and_food_collision(self, species_tag, food):
        """Calculates if there is a collision between two species bounds"""

        species_coords = self.evolution_frame.coords(self.species_bodies[species_tag])
        species_size = self.species_parameters[species_tag].size
        food_coords = self.evolution_frame.coords(food)

        distance = math.sqrt(
            (((species_coords[0]+species_size) - (food_coords[0]+self.food_size)) * ((species_coords[0]+species_size) - (food_coords[0]+self.food_size))) + 
            (((species_coords[1]+species_size) - (food_coords[1]+self.food_size)) * ((species_coords[1]+species_size) - (food_coords[1]+self.food_size)))
        )

        if distance < (species_size + self.food_size): return True
        return False

    def initialize(self, individuals, food, epochs):
        """Initialize the parameters the genetic algorithm will use"""

        taken_coords = {}
        self.tag_number_for_species = individuals

        # Calculate all the species parameters
        for index in range(individuals):
            size = random.randrange(6, 9)
            velocity_x = round(random.uniform(0.5, 0.7), 2) * random.choice([-1, 1])
            velocity_y = round(random.uniform(0.5, 0.7), 2) * random.choice([-1, 1])
            
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
        self.number_of_food = food

        # Calculate food coordinates
        for _ in range(food):
            new_coords = []
            still_collide = True
            while(still_collide):
                still_collide = False
                new_coords = [random.randrange(20, 881), random.randrange(20, 481)]

                for tag, coords in taken_coords.items():
                    if self.initialization_collisions(new_coords, coords, self.food_size, self.species_parameters[tag].size): still_collide = True

                for coords in food_taken_coords:
                    if self.initialization_collisions(new_coords, coords, self.food_size, self.food_size): still_collide = True
            
            food_taken_coords.append(new_coords)

        # Create the species and draw them in the canvas
        for tag, species in self.species_parameters.items():
            self.species_bodies[str(tag)] = self.evolution_frame.create_oval(
                taken_coords[tag][0]-species.size, 
                taken_coords[tag][1]-species.size, 
                taken_coords[tag][0]+species.size, 
                taken_coords[tag][1]+species.size, 
                fill="blue", 
                tags=str(tag)
            )

        # Create the food and draw them in the canvas
        for index in range(len(food_taken_coords)):
            self.food_bodies["F-"+str(index)] = self.evolution_frame.create_oval(
                food_taken_coords[index][0]-self.food_size, 
                food_taken_coords[index][1]-self.food_size, 
                food_taken_coords[index][0]+self.food_size, 
                food_taken_coords[index][1]+self.food_size, 
                fill="green", 
                tags="F-"+str(index)
            )

        self.epochs = epochs

        self.all_threads_finished = len(self.species_bodies)

        self.run_algorithm()

    def initialization_collisions(self, coords1, coords2, species_size, species2_size):
        """Calculates if two points in the canvas are colliding"""

        distance = math.sqrt(
            ((coords1[0] - coords2[0]) * (coords1[0] - coords2[0])) + 
            ((coords1[1] - coords2[1]) * (coords1[1] - coords2[1]))
        )

        if distance < (species_size + species2_size): return True
        return False

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

        if self.all_threads_finished == len(self.species_bodies):
            for tag in [tag for tag in self.species_bodies]:
                self.evolution_frame.delete(tag)

            for tag in [tag for tag in self.food_bodies]:
                self.evolution_frame.delete(tag)

            self.species_parameters = {}
            self.species_bodies = {}
            self.food_bodies = {}

            self.time_of_actual_epoch = 0
        else: self.after(1, self.restart)

    def prepare_notification(self, type, message, extra):
        self.type_of_notification = type
        self.message = message
        self.extra_message_data = extra
        self.notify()