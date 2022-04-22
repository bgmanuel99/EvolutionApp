import math
import random
import threading
import datetime
from tkinter import *
from time import time
from typing import List
from collections import Counter
from tkinter import messagebox as MessageBox
from components.models.species import Species
from components.models.gradients import GradientFrame
from components.interfaces.observer import Observer
from components.interfaces.publisher import Publisher
from components.generator.reportsLogGenerator import ReportsLogGenerator

class EvolutionFrame(Frame, Observer, Publisher):

    """This is the main application frame. Used to show the genetic algorithm in execution by recreating the species and the environments on it"""

    def __init__(self, root):
        Frame.__init__(self, root)
        self.config(bg="dark turquoise")

        self._observers: List[Observer] = []

        self.gradient = GradientFrame(self, "SpringGreen4", "OliveDrab1")
        self.gradient.pack(expand=True, fill=BOTH)
        self.gradient.config(bd=0, highlightthickness=0, relief='ridge')

        self.evolution_frame = Canvas(self.gradient)
        self.evolution_frame.pack(expand=True, fill=BOTH, padx=2, pady=2)
        self.evolution_frame.config(bg="pale green", bd=0, highlightthickness=0)

        self.execution_status = False

        self.species_parameters = {}
        self.species_bodies = {}
        self.species_color_by_velocity = {
            "0.3": "gray5",
            "0.4": "midnight blue",
            "0.5": "navy",
            "0.6": "medium blue",
            "0.7": "blue",
            "0.8": "deep sky blue",
            "0.9": "light sky blue",
            "1.0": "light blue"
        }
        self.food_bodies = {}
        self.food_size = 5

        self.type_of_notification = ""
        self.message = ""
        self.extra_message_data = []

        self.calculations_characteristics_data = {
            "actual_epoch": 0,
            "number_of_individuals": 0,
            "number_of_food": 0,
            "number_of_non_survival_individuals": 0,
            "number_of_survival_individuals": 0,
            "number_of_evolving_individuals": 0,
            "maximum_number_of_individuals": 0,
            "minimum_number_of_individuals": 0,
            "minimum_number_of_food": 0,
            "maximum_velocity_of_an_individual": 0,
            "minimum_velocity_of_an_individual": 0,
            "maximum_size_of_an_individual": 0,
            "minimum_size_of_an_individual": 0,
            "most_appearing_velocity": (0, 0),
            "most_appearing_size": (0, 0),
            "epoch_time": 0
        }

        self.notifications_characteristics_data = {
            "actual_epoch": None,
            "number_of_individuals": None,
            "number_of_food": None,
            "number_of_non_survival_individuals": None,
            "number_of_survival_individuals": None,
            "number_of_evolving_individuals": None,
            "maximum_number_of_individuals": None,
            "minimum_number_of_individuals": None,
            "minimum_number_of_food": None,
            "maximum_velocity_of_an_individual": None,
            "minimum_velocity_of_an_individual": None,
            "maximum_size_of_an_individual": None,
            "minimum_size_of_an_individual": None,
            "most_appearing_velocity": None,
            "most_appearing_size": None
        }

        self.time_of_actual_epoch = 0
        self.total_time_per_epoch = 20000
        self.total_time_per_epoch_percentage = 0.01
        self.next_epoch = False
        self.algorithm_percentage = 0
        self.minimal_algorithm_percentage = 0
        self.actual_epoch = 1
        self.needed_food_to_survive_and_evolve = [1, 2]
        self.velocity_initializing_values = [0.5, 0.7]
        self.velocity_limits = [0.5, 1]

        self.temp_food_tags = []
        self.all_threads_finished = 0
        
        # Locks for the critics sections of the code
        self.wall_collision_lock = threading.Lock()
        self.species_and_food_collision_lock = threading.Lock()

        # Variables to track the spend time on the execution of each epoch
        self.start_time_of_epoch = 0
        self.end_time_of_epoch = 0
        self.start_stopped_time_of_epoch = 0
        self.end_stopped_time_of_epoch = 0
        self.full_stopped_time_of_epoch = 0
        self.scale_of_time = ""

        # This variable indicates if the algorithm finished becaused there are no more individuals left
        self.abrupt_stop_of_execution = False

        # Variable to know the path of the evolution report log to track
        self.actual_evolution_report_log = None

        #Variable to know if the algorithm should make a tracking of the execution of the algorithm to insert into the report log
        self.track_evolution_report = False

        # This variable contains the value of the actual epoch temporarely to be passed to the election panel and then writed to the evolution report log
        # It is always restarted after the algorithm execution is finished, but not when it is restarted
        self.temp_actual_epoch = 1

        # Variable for the application to know if the genetic algorithm is running
        self.algorithm_running_status = False

        # Variable to stop the algorithm if the application is closed while the genetic algorithm is running
        self.stop_algorithm_execution = False

        # Variable to know which environment is the genetic algorithm running on
        self.actual_environment = "mediterranean"

    def update(self, *args) -> None:
        """Receive the update from the publisher"""
        
        if args[0] == "run":
            self.type_of_notification = "update_epoch_time"
            self.scale_of_time = "restart"
            self.notify()
            self.start_time_of_epoch = int(time() * 1000)

            self.track_evolution_report = args[2][0]

            if self.track_evolution_report:
                # Set the new evolution report log
                start_algorithm_date = datetime.datetime.now()
                self.actual_evolution_report_log = args[2][1]

                time_of_creation_of_evolution_report_log = [
                    start_algorithm_date.strftime("%H"),
                    start_algorithm_date.strftime("%M"),
                    start_algorithm_date.strftime("%S"),
                    start_algorithm_date.strftime("%d"),
                    start_algorithm_date.strftime("%m"),
                    start_algorithm_date.strftime("%Y")
                ]

                # Creates, if not exists, and initilialize evolution report log
                ReportsLogGenerator.initilize_evolution_report_log(reports_path=self.actual_evolution_report_log, data=[args[1][0], args[1][1], args[1][2]], time_of_creation=time_of_creation_of_evolution_report_log)

                self.prepare_notification("message", "Evolution report log created at ", ["gray70", 1, 0, False])
                self.prepare_notification("message", "{}".format(time_of_creation_of_evolution_report_log[0]), ["OliveDrab1", 0, 0, False])
                self.prepare_notification("message", ":", ["gray70", 0, 0, False])
                self.prepare_notification("message", "{}".format(time_of_creation_of_evolution_report_log[1]), ["OliveDrab1", 0, 0, False])
                self.prepare_notification("message", ":", ["gray70", 0, 0, False])
                self.prepare_notification("message", "{} {}".format(time_of_creation_of_evolution_report_log[2], time_of_creation_of_evolution_report_log[3]), ["OliveDrab1", 0, 0, False])
                self.prepare_notification("message", "/", ["gray70", 0, 0, False])
                self.prepare_notification("message", "{}".format(time_of_creation_of_evolution_report_log[4]), ["OliveDrab1", 0, 0, False])
                self.prepare_notification("message", "/", ["gray70", 0, 0, False])
                self.prepare_notification("message", "{}".format(time_of_creation_of_evolution_report_log[5]), ["OliveDrab1", 0, 0, False])
                self.prepare_notification("message", ". Initiating recording of data", ["gray70", 0, 0, False])

                ReportsLogGenerator.write_message_to_evolution_log(reports_path=self.actual_evolution_report_log, message="The algorithm is running in the {} environment".format(self.actual_environment.upper()))

                # Write message to the evolution report log that the values are been initialized for the algorithm to be started
                ReportsLogGenerator.write_message_to_evolution_log(reports_path=self.actual_evolution_report_log, message="Initializing values for the first epoch in order to start the algorithm...")

            # Initilialize the algorithm values
            self.prepare_notification("message", "Initializing values to start the algorithm...", ["gray70", 1, 0, False])
            self.initialize(args[1][0], args[1][1], args[1][2])
            self.prepare_notification("message", " Done", ["OliveDrab1", 0, 0, False])

            if self.track_evolution_report:
                # Writting the initial data of the actual epoch to the evolution report log
                self.prepare_notification("message", "Writting initial data from epoch ", ["gray70", 1, 0, False])
                self.prepare_notification("message", str(self.actual_epoch), ["OliveDrab1", 0, 0, False])
                self.prepare_notification("message", " to the report log... ", ["gray70", 0, 0, False])
                ReportsLogGenerator.write_evolution_data_to_log(reports_path=self.actual_evolution_report_log, data=self.calculations_characteristics_data, running_state="initializing_epoch")
                self.prepare_notification("message", "Done", ["OliveDrab1", 0, 0, False])

                self.prepare_notification("message", "Running epoch ", ["gray70", 1, 0, False])
                self.prepare_notification("message", str(self.actual_epoch), ["OliveDrab1", 0, 0, False])

            # Start the algorithm execution
            self.run_algorithm()

            self.algorithm_running_status = True
        elif args[0] == "stop":
            self.start_stopped_time_of_epoch = int(time() * 1000)
            self.stop()
            self.prepare_notification("message", "Algorithm stopped at epoch ", ["gray70", 1, 0, False])
            self.prepare_notification("message", str(self.actual_epoch), ["OliveDrab1", 0, 0, False])
        elif args[0] == "continue":
            self.end_stopped_time_of_epoch = int(time() * 1000)
            self.full_stopped_time_of_epoch += (self.end_stopped_time_of_epoch - self.start_stopped_time_of_epoch)
            self.start_stopped_time_of_epoch = 0
            self.end_stopped_time_of_epoch = 0
            self.run_algorithm()
            self.prepare_notification("message", "Cotinuing algorithm execution", ["gray70", 1, 0, False])
        elif args[0] == "restart":
            if self.track_evolution_report:
                # Write message to the evolution report log that the algorithm has been restarted
                ReportsLogGenerator.write_message_to_evolution_log(reports_path=self.actual_evolution_report_log, message="The algorithm stopped abruptly at epoch {}".format(self.actual_epoch))

            # Restart al the values of the evolution frame in use by the algorithm
            self.restart()

            self.algorithm_running_status = False
            self.prepare_notification("message", "Restarting the execution of the algorithm", ["gray70", 1, 2, True])
        elif args[0] == "change_environment":
            if args[1] == "polar":
                self.gradient.set_new_colors("magenta4", "RoyalBlue2")
                self.evolution_frame.config(bg="light sky blue")
                self.needed_food_to_survive_and_evolve = [2, 3]
                self.velocity_initializing_values = [0.3, 0.5]
                self.velocity_limits = [0.3, 0.8]
                self.actual_environment = "polar"
            elif args[1] == "mediterranean":
                self.gradient.set_new_colors("SpringGreen4", "OliveDrab1")
                self.evolution_frame.config(bg="pale green")
                self.needed_food_to_survive_and_evolve = [1, 2]
                self.velocity_initializing_values = [0.5, 0.7]
                self.velocity_limits = [0.5, 1]
                self.actual_environment = "mediterranean"
            elif args[1] == "desert":
                self.gradient.set_new_colors("brown", "goldenrod1")
                self.evolution_frame.config(bg="khaki1")
                self.needed_food_to_survive_and_evolve = [1, 2]
                self.velocity_initializing_values = [0.5, 0.7]
                self.velocity_limits = [0.5, 1]
                self.actual_environment = "desert"

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
        elif self.type_of_notification == "finish_execution":
            for observers in self._observers:
                observers.update(self.type_of_notification, self.temp_actual_epoch)
        elif self.type_of_notification == "update_characteristics_data":
            for observers in self._observers:
                observers.update(self.type_of_notification, self.notifications_characteristics_data)
        elif self.type_of_notification == "progress_epoch_bar":
            for observers in self._observers:
                observers.update(self.type_of_notification, self.next_epoch)
        elif self.type_of_notification == "progress_algorithm_bar":
            for observers in self._observers:
                observers.update(self.type_of_notification, self.algorithm_percentage)
        elif self.type_of_notification == "update_epoch_time":
            for observers in self._observers:
                observers.update(self.type_of_notification, self.transform_time(self.start_time_of_epoch, self.end_time_of_epoch, self.scale_of_time), self.scale_of_time)
        elif self.type_of_notification == "finish_application":
            for observers in self._observers:
                observers.update(self.type_of_notification)

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
        if species_object.food_pieces != self.needed_food_to_survive_and_evolve[1]:
            for food_tag, food in self.food_bodies.items():
                if species_object.food_pieces == self.needed_food_to_survive_and_evolve[1]: break
                self.species_and_food_collision_lock.acquire()
                food_collision_response = self.species_and_food_collision(tag, food)
                self.species_and_food_collision_lock.release()
                if food_collision_response:
                    species_object.add_piece()
                    if species_object.food_pieces == self.needed_food_to_survive_and_evolve[0]:
                        self.prepare_characteristics_notification(
                            number_of_non_survival_individuals=self.calculations_characteristics_data["number_of_non_survival_individuals"] - 1
                        )

                        if self.track_evolution_report:
                            # Write new data for the non survival individuals left on the algorithm to the report log
                            ReportsLogGenerator.write_evolution_data_to_log(reports_path=self.actual_evolution_report_log, data=[self.calculations_characteristics_data["number_of_non_survival_individuals"]], running_state="running_epoch")
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
                # If the application is going to be closed while the algorithm is running, this variable will be set to True to stop the execution and creation of new threads
                if self.stop_algorithm_execution:
                    self.type_of_notification = "finish_application"
                    self.notify()
                    return

                # This calculation is made for the progress bar
                if self.time_of_actual_epoch == int(round(self.total_time_per_epoch * self.total_time_per_epoch_percentage, 0)):
                    self.type_of_notification = "progress_epoch_bar"
                    self.next_epoch = False
                    self.notify()
                    self.total_time_per_epoch_percentage = round(self.total_time_per_epoch_percentage + 0.01, 2)

                # If the execution of the epoch reach 20 seconds then the data of the epoch is processed and the genetic algorithm is executed
                if self.time_of_actual_epoch == self.total_time_per_epoch:
                    # If it is the last epoch then the data of the epoch is processed and the algorithm is stopped
                    if self.process_next_epoch(self.actual_epoch == self.epochs):
                        self.all_threads_finished = len(self.species_bodies)
                        self.finish_algorithm_execution()
                        return

                self.time_of_actual_epoch += 10

                # Delete the food bodies that had been eaten after all the threads had been executed
                for food_tag in self.temp_food_tags:
                    if food_tag not in self.food_bodies: continue
                    del(self.food_bodies[food_tag])
                    self.evolution_frame.delete(food_tag)

                # Prepares the information to be send to the characteristics terminal
                new_number_of_survival_individuals = len([tag for tag, individual in self.species_parameters.items() if individual.food_pieces >= self.needed_food_to_survive_and_evolve[0]])
                new_number_of_evolving_individuals = len([tag for tag, individual in self.species_parameters.items() if individual.food_pieces == self.needed_food_to_survive_and_evolve[1]])
                new_minimum_number_of_food = len(self.food_bodies) if len(self.food_bodies) < self.calculations_characteristics_data["minimum_number_of_food"] else None

                # Prepare the information to be send to the evolution report log
                evolution_report_running_state_data = [
                    new_number_of_survival_individuals if new_number_of_survival_individuals > self.calculations_characteristics_data["number_of_survival_individuals"] else None,
                    new_number_of_evolving_individuals if new_number_of_evolving_individuals > self.calculations_characteristics_data["number_of_evolving_individuals"] else None
                ]

                # Update characteristics terminal
                self.prepare_characteristics_notification(
                    number_of_food=len(self.food_bodies), number_of_survival_individuals=new_number_of_survival_individuals, 
                    number_of_evolving_individuals=new_number_of_evolving_individuals, minimum_number_of_food=new_minimum_number_of_food
                )

                if self.track_evolution_report:
                    if any([report_data != None for report_data in evolution_report_running_state_data]): ReportsLogGenerator.write_evolution_data_to_log(reports_path=self.actual_evolution_report_log, data=evolution_report_running_state_data, running_state="running_epoch")

                # Reinitialize the variables so the next threads are correctly executed
                self.temp_food_tags = []
                self.all_threads_finished = 0
                thread_num = 0

                # Execute a thread for each individual in order to do it's pertinent calculations 
                for tag, species_body in self.species_bodies.items():
                    threading.Thread(name="thread{}".format(thread_num), target=self.evaluate_individual, args=(tag, species_body)).start()
                    thread_num += 1

                self.evolution_frame.after(10, self.move_species)
            else: self.evolution_frame.after(1, self.move_species)
    
    def process_next_epoch(self, finish=False):
        """This function will process the actual epoch data to use in the genetic algorithm"""

        # Restart epoch timer
        self.time_of_actual_epoch = 0

        # Calculate the time of execution for the epoch
        self.end_time_of_epoch = int(time() * 1000)
        self.calculations_characteristics_data["epoch_time"] = int(round(((self.end_time_of_epoch - self.start_time_of_epoch) - self.full_stopped_time_of_epoch) / 1000, 0))
        self.type_of_notification = "update_epoch_time"
        self.scale_of_time = "seconds"
        self.notify()
        self.end_time_of_epoch = 0
        self.start_stopped_time_of_epoch = 0
        self.end_stopped_time_of_epoch = 0
        self.full_stopped_time_of_epoch = 0
        self.scale_of_time = ""

        if self.track_evolution_report:
            # Writting the ending data of the actual epoch to the evolution report log
            self.prepare_notification("message", "Writting ending data from epoch ", ["gray70", 1, 0, False])
            self.prepare_notification("message", str(self.actual_epoch), ["OliveDrab1", 0, 0, False])
            self.prepare_notification("message", " to the report log... ", ["gray70", 0, 0, False])
            ReportsLogGenerator.write_evolution_data_to_log(reports_path=self.actual_evolution_report_log, data=self.calculations_characteristics_data, running_state="ending_epoch")
            self.prepare_notification("message", "Done", ["OliveDrab1", 0, 0, False])

        # Get the start time for the next epoch
        self.start_time_of_epoch = int(time() * 1000)

        if self.track_evolution_report:
            # Write message to the evolution report log that the epoch data is been processed in the genetic algorithm
            ReportsLogGenerator.write_message_to_evolution_log(reports_path=self.actual_evolution_report_log, message="Processing data from epoch {} in the Genetic Algorithm...".format(self.actual_epoch))

        self.prepare_notification("message", "Processing data of epoch ", ["gray70", 1, 0, False])
        self.prepare_notification("message", str(self.actual_epoch), ["OliveDrab1", 0, 0, False])
        self.prepare_notification("message", " in the genetic algorithm... ", ["gray70", 0, 0, False])

        # Call the genetic algorithm function to process the new data
        # If it returns True, then it means there are no survivals left and the algorithm has to stopped it's execution
        # If it return False, the algorithm will continue with the execution in a normal way
        if self.genetic_algorithm(): self.abrupt_stop_of_execution = True

        self.prepare_notification("message", "Done", ["OliveDrab1", 0, 0, False])

        if finish or self.abrupt_stop_of_execution:
            if self.track_evolution_report:
                # Writting the last epoch data processed by the genetic algorithm
                self.prepare_notification("message", "Writting final data of the algorithm to the report log... ", ["gray70", 1, 0, False])
                ReportsLogGenerator.write_evolution_data_to_log(reports_path=self.actual_evolution_report_log, data=self.calculations_characteristics_data, running_state="ending_algorithm")
                self.prepare_notification("message", "Done", ["OliveDrab1", 0, 0, False])

            if self.abrupt_stop_of_execution and not finish:
                self.prepare_notification("message", "The algorithm has stopped at epoch ", ["gray70", 1, 0, False])
                self.prepare_notification("message", str(self.actual_epoch), ["OliveDrab1", 0, 0, False])
                self.prepare_notification("message", " because there are no survivals left!", ["gray70", 0, 2, True])
            else:
                self.prepare_notification("message", "Finished algorithm at epoch ", ["gray70", 1, 0, False])
                self.prepare_notification("message", str(self.actual_epoch), ["OliveDrab1", 0, 2, True])

            return True
        else:
            # Set next epoch
            self.actual_epoch += 1

            if self.track_evolution_report:
                # Writting the initial data of the actual epoch to the evolution report log
                # The initial data of an epoch is the data from the last epoch, processed by the genetic algorithm
                self.prepare_notification("message", "Writting initial data from epoch ", ["gray70", 1, 0, False])
                self.prepare_notification("message", str(self.actual_epoch), ["OliveDrab1", 0, 0, False])
                self.prepare_notification("message", " to the report log... ", ["gray70", 0, 0, False])
                ReportsLogGenerator.write_evolution_data_to_log(reports_path=self.actual_evolution_report_log, data=self.calculations_characteristics_data, running_state="initializing_epoch")
                self.prepare_notification("message", "Done", ["OliveDrab1", 0, 0, False])

            self.prepare_notification("message", "Running epoch ", ["gray70", 1, 0, False])
            self.prepare_notification("message", str(self.actual_epoch), ["OliveDrab1", 0, 0, False])

            # Restart the epoch percentage variable for the progress bar to be restarted
            self.total_time_per_epoch_percentage = 0
            self.type_of_notification = "progress_epoch_bar"
            self.next_epoch = True
            self.notify()
            self.total_time_per_epoch_percentage = 0.01

            # Update algorithm progress bar as well after an epoch has conclude
            self.type_of_notification = "progress_algorithm_bar"
            self.notify()
            self.algorithm_percentage += self.minimal_algorithm_percentage
        
        return False
    
    def genetic_algorithm(self):
        """This is the main function of the genetic algorithm"""

        # Evaluate which of the individuals should survive and reproduce to the next epoch
        reproduce_individuals = self.evaluate()

        # If the lenght of the self.species_bodies is 0 it means that any individual could survive the epoch so the algorithm shall finish
        if len(self.species_bodies) == 0: return True

        # Delete the resting food on the terrain
        for food in self.food_bodies.keys(): self.evolution_frame.delete(food)
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
                fill=self.species_color_by_velocity[str(round((abs(self.species_parameters[tag].velocity[0])+abs(self.species_parameters[tag].velocity[1]))/2, 1))], 
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

        list_of_speeds = [round((abs(species.velocity[0])+abs(species.velocity[1]))/2, 1) for species in self.species_parameters.values()]
        list_of_sizes = [species.size for species in self.species_parameters.values()]
        new_maximum_number_of_individuals = len(self.species_parameters) if len(self.species_parameters) > self.calculations_characteristics_data["maximum_number_of_individuals"] else None
        new_minimum_number_of_individuals = len(self.species_parameters) if len(self.species_parameters) < self.calculations_characteristics_data["minimum_number_of_individuals"] else None
        new_maximum_velocity_of_individual = max(list_of_speeds) if max(list_of_speeds) > self.calculations_characteristics_data["maximum_velocity_of_an_individual"] else None
        new_minimum_velocity_of_individual = min(list_of_speeds) if min(list_of_speeds) < self.calculations_characteristics_data["minimum_velocity_of_an_individual"] else None
        new_maximum_size_of_individual = max(list_of_sizes) if max(list_of_sizes) > self.calculations_characteristics_data["maximum_size_of_an_individual"] else None
        new_minimum_size_of_individual = min(list_of_sizes) if max(list_of_sizes) < self.calculations_characteristics_data["minimum_size_of_an_individual"] else None
        new_most_appearing_velocity = (Counter(list_of_speeds).most_common()[0] 
                                       if Counter(list_of_speeds).most_common()[0][1] > self.calculations_characteristics_data["most_appearing_velocity"][1] 
                                       else None)
        new_most_appearing_size = (Counter(list_of_sizes).most_common()[0]
                                   if Counter(list_of_sizes).most_common()[0][1] > self.calculations_characteristics_data["most_appearing_size"][1]
                                   else None)

        self.prepare_characteristics_notification(
            actual_epoch=self.actual_epoch+1, number_of_individuals=len(self.species_parameters), number_of_food=len(self.food_bodies), 
            number_of_non_survival_individuals=len(self.species_parameters), number_of_survival_individuals=0, number_of_evolving_individuals=0, 
            maximum_number_of_individuals=new_maximum_number_of_individuals, minimum_number_of_individuals=new_minimum_number_of_individuals, 
            maximum_velocity_of_an_individual=new_maximum_velocity_of_individual, minimum_velocity_of_an_individual=new_minimum_velocity_of_individual, 
            maximum_size_of_an_individual=new_maximum_size_of_individual, minimum_size_of_an_individual=new_minimum_size_of_individual, 
            most_appearing_velocity=new_most_appearing_velocity, most_appearing_size=new_most_appearing_size
        )

        # At the top of this method, if there are no survivals in the actual epoch, it will return True so the algorithm finish it's execution
        # Otherwise if there are survivals and the algorithm could run propertly then the method will return False to continue with the execution
        return False
    
    def evaluate(self):
        """
        This function will evaluate which individuals should reproduce or die.
        The ones who shall die, because did'nt get any food, will be erased.
        The ones to reproduce will be passed as a return of the function.
        """

        delete_species_tags = []
        reproduce_species_tags = []

        for tag, species in self.species_parameters.items():
            if species.food_pieces < self.needed_food_to_survive_and_evolve[0]: delete_species_tags.append(tag)
            elif species.food_pieces == self.needed_food_to_survive_and_evolve[0]: species.food_pieces = 0
            elif species.food_pieces == self.needed_food_to_survive_and_evolve[1]: 
                species.food_pieces = 0
                reproduce_species_tags.append(tag)

        for tag in delete_species_tags:
            del(self.species_bodies[tag])
            del(self.species_parameters[tag])
            self.evolution_frame.delete(tag)

        return reproduce_species_tags

    def mutate_size(self, size):
        """This method will slightly mutate the size of each new individual inserted for the genetic algorithm"""

        new_size = size + random.choice([-1, 1])
        if new_size < 10 or new_size > 17: return size
        return new_size

    def mutate_velocity(self, velocity):
        """This method will slightly mutate the velocity of each new individual inserted for the genetic algorithm"""

        new_velocity_x = velocity[0] + random.choice([-0.1, 0.1])
        new_velocity_y = velocity[1] + random.choice([-0.1, 0.1])
        if new_velocity_x < self.velocity_limits[0] or new_velocity_x > self.velocity_limits[1]: new_velocity_x = velocity[0]
        if new_velocity_y < self.velocity_limits[0] or new_velocity_y > self.velocity_limits[1]: new_velocity_y = velocity[1]
        return [new_velocity_x, new_velocity_y]

    def wall_collision(self, species):
        """Calculates if there is a collision between a wall of the canvas and a species bounds"""

        coords = self.evolution_frame.coords(species)
        if coords[0] < 2: return True, 0
        elif coords[1] < 2: return True, 1
        elif coords[2] > 897: return True, 2
        elif coords[3] > 497: return True, 3
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
            size = random.randrange(12, 14)
            velocity_x = round(random.uniform(self.velocity_initializing_values[0], self.velocity_initializing_values[1]), 1) * random.choice([-1, 1])
            velocity_y = round(random.uniform(self.velocity_initializing_values[0], self.velocity_initializing_values[1]), 1) * random.choice([-1, 1])
            
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
                fill=self.species_color_by_velocity[str(round((abs(species.velocity[0])+abs(species.velocity[1]))/2, 1))], 
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
        self.algorithm_percentage = 100 / epochs
        self.minimal_algorithm_percentage = 100 / epochs

        self.all_threads_finished = len(self.species_bodies)

        # First calculations for the characteristics terminal
        list_of_speeds = [round((abs(species.velocity[0])+abs(species.velocity[1]))/2, 1) for species in self.species_parameters.values()]
        list_of_sizes = [species.size for species in self.species_parameters.values()]
        self.prepare_characteristics_notification(
            actual_epoch=1, number_of_individuals=len(self.species_parameters), number_of_food=len(self.food_bodies), 
            number_of_non_survival_individuals=len(self.species_parameters), maximum_number_of_individuals=len(self.species_parameters), 
            minimum_number_of_individuals=len(self.species_parameters), minimum_number_of_food=len(self.food_bodies), 
            maximum_velocity_of_an_individual=max(list_of_speeds), minimum_velocity_of_an_individual=min(list_of_speeds),
            maximum_size_of_an_individual=max(list_of_sizes), minimum_size_of_an_individual=min(list_of_sizes),
            most_appearing_velocity=Counter(list_of_speeds).most_common()[0], most_appearing_size=Counter(list_of_sizes).most_common()[0]
        )

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
            # Delete any object on the canvas
            for tag in [tag for tag in self.species_bodies]:
                self.evolution_frame.delete(tag)

            for tag in [tag for tag in self.food_bodies]:
                self.evolution_frame.delete(tag)

            # Reset variables for species, food and epoch
            self.species_parameters = {}
            self.species_bodies = {}
            self.food_bodies = {}
            self.time_of_actual_epoch = 0
            self.actual_epoch = 1

            # Reset variables for the progress bars
            self.total_time_per_epoch_percentage = 0.01
            self.next_epoch = False
            self.algorithm_percentage = 0
            self.minimal_algorithm_percentage = 0

            # Reset variables for the calculation of time of execution for the epochs
            self.type_of_notification = "update_epoch_time"
            self.scale_of_time = "restart"
            self.notify()
            self.start_time_of_epoch = 0
            self.end_time_of_epoch = 0
            self.start_stopped_time_of_epoch = 0
            self.end_stopped_time_of_epoch = 0
            self.full_stopped_time_of_epoch = 0
            self.scale_of_time = ""

            # Reset the value of the variable which tracks if the evolution report log shall be writted
            self.track_evolution_report = False

            # Reset variables on the characteristics terminal
            self.prepare_characteristics_notification(
                actual_epoch=0, number_of_individuals=0, number_of_food=0, number_of_non_survival_individuals=0, number_of_survival_individuals=0,
                number_of_evolving_individuals=0, maximum_number_of_individuals=0, minimum_number_of_individuals=0, minimum_number_of_food=0,
                maximum_velocity_of_an_individual=0, minimum_velocity_of_an_individual=0, maximum_size_of_an_individual=0, minimum_size_of_an_individual=0,
                most_appearing_velocity=(0, 0), most_appearing_size=(0, 0)
            )
        else: self.after(1, self.restart)

    def finish_algorithm_execution(self):
        """This function will be called when the genetic algorithm finish it's execution passing throughout all the epochs"""

        self.temp_actual_epoch = self.actual_epoch
        
        self.restart()
        
        self.type_of_notification = "finish_execution"
        self.notify()

        self.temp_actual_epoch = 1

        self.algorithm_running_status = False

        if self.abrupt_stop_of_execution: MessageBox.showwarning(message="The algorithm stopped because there are no survivals left", title="Algorithm warning")

        # Reset the value that indicates if the algorithm has stopped because it finished or because there were no more individuals left
        self.abrupt_stop_of_execution = False

    def prepare_notification(self, type, message, extra):
        """This function prepares the notification for the messages data to be passed to the main terminal"""
        self.type_of_notification = type
        self.message = message
        self.extra_message_data = extra
        self.notify()

    def prepare_characteristics_notification(
        self, actual_epoch=None, number_of_individuals=None, number_of_food=None, number_of_non_survival_individuals=None, number_of_survival_individuals=None,
        number_of_evolving_individuals=None, maximum_number_of_individuals=None, minimum_number_of_individuals=None, minimum_number_of_food=None,
        maximum_velocity_of_an_individual=None, minimum_velocity_of_an_individual=None, maximum_size_of_an_individual=None, minimum_size_of_an_individual=None,
        most_appearing_velocity=None, most_appearing_size=None):
        """This function prepares the notification for the updating data to be passed to the characteristics terminal"""

        if actual_epoch != None: self.calculations_characteristics_data["actual_epoch"] = actual_epoch
        if number_of_individuals != None: self.calculations_characteristics_data["number_of_individuals"] = number_of_individuals
        if number_of_food != None: self.calculations_characteristics_data["number_of_food"] = number_of_food
        if number_of_non_survival_individuals != None: self.calculations_characteristics_data["number_of_non_survival_individuals"] = number_of_non_survival_individuals
        if number_of_survival_individuals != None: self.calculations_characteristics_data["number_of_survival_individuals"] = number_of_survival_individuals
        if number_of_evolving_individuals != None: self.calculations_characteristics_data["number_of_evolving_individuals"] = number_of_evolving_individuals
        if maximum_number_of_individuals != None: self.calculations_characteristics_data["maximum_number_of_individuals"] = maximum_number_of_individuals
        if minimum_number_of_individuals != None: self.calculations_characteristics_data["minimum_number_of_individuals"] = minimum_number_of_individuals
        if minimum_number_of_food != None: self.calculations_characteristics_data["minimum_number_of_food"] = minimum_number_of_food
        if maximum_velocity_of_an_individual != None: self.calculations_characteristics_data["maximum_velocity_of_an_individual"] = maximum_velocity_of_an_individual
        if minimum_velocity_of_an_individual != None: self.calculations_characteristics_data["minimum_velocity_of_an_individual"] = minimum_velocity_of_an_individual
        if maximum_size_of_an_individual != None: self.calculations_characteristics_data["maximum_size_of_an_individual"] = maximum_size_of_an_individual
        if minimum_size_of_an_individual != None: self.calculations_characteristics_data["minimum_size_of_an_individual"] = minimum_size_of_an_individual
        if most_appearing_velocity != None: self.calculations_characteristics_data["most_appearing_velocity"] = most_appearing_velocity
        if most_appearing_size != None: self.calculations_characteristics_data["most_appearing_size"] = most_appearing_size

        self.notifications_characteristics_data = {
            "actual_epoch": actual_epoch,
            "number_of_individuals": number_of_individuals,
            "number_of_food": number_of_food,
            "number_of_non_survival_individuals": number_of_non_survival_individuals,
            "number_of_survival_individuals": number_of_survival_individuals,
            "number_of_evolving_individuals": number_of_evolving_individuals,
            "maximum_number_of_individuals": maximum_number_of_individuals,
            "minimum_number_of_individuals": minimum_number_of_individuals,
            "minimum_number_of_food": minimum_number_of_food,
            "maximum_velocity_of_an_individual": maximum_velocity_of_an_individual,
            "minimum_velocity_of_an_individual": minimum_velocity_of_an_individual,
            "maximum_size_of_an_individual": maximum_size_of_an_individual,
            "minimum_size_of_an_individual": minimum_size_of_an_individual,
            "most_appearing_velocity": most_appearing_velocity,
            "most_appearing_size": most_appearing_size
        }

        self.type_of_notification = "update_characteristics_data"
        self.notify()

    def transform_time(self, start_time, end_time, scale):
        """This method will transform time passed in milliseconds to the choosen scale"""

        # The final time of the epoch will be the substract of the end time and the start time, minus the time the epoch might have been stopped by the user
        final_time = (end_time - start_time) - self.full_stopped_time_of_epoch

        if scale == "seconds": return int(round(final_time / 1000, 0))
        elif scale == "minutes": return int(round((final_time / 1000) / 60, 0))
        elif scale == "hours": return int(round(((final_time / 1000) / 60) / 60, 0))
        elif scale == "restart": return 0