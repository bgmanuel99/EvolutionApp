from tkinter import *
from time import time
from typing import List
from tkinter.ttk import Progressbar
from tkinter import messagebox as MessageBox
from tkinter import filedialog as FileDialog
from components.models.gradients import GradientFrame
from components.interfaces.observer import Observer
from components.interfaces.publisher import Publisher
from components.audio.soundEffects import SoundEffects
from components.generator.reportsLogGenerator import ReportsLogGenerator

class ElectionsFrame(Frame, Publisher, Observer):

    """This frame contains the different options the user can use to change characteristics, insert new objects and start the application"""

    def __init__(self, root):
        Frame.__init__(self, root)
        self.config(bg="dark turquoise")

        self._observers: List[Observer] = []

        self.gradient = GradientFrame(self, "SpringGreen4", "OliveDrab1")
        self.gradient.pack()
        self.gradient.config(bd=0, highlightthickness=0, relief='ridge')

        self.options_frame = Frame(self.gradient, width=300, height=500)
        self.options_frame.pack(fill=BOTH, padx=2, pady=2)
        self.options_frame.pack_propagate(0)
        self.options_frame.configure(background="gray8")

        self.individuals_label = Label(self.options_frame, text="Number of individuals:", anchor="w")
        self.individuals_label.place(x=20, y=20, width=120, height=20)
        self.individuals_label.config(background="gray8", foreground="white", font=("Terminal", 11))

        self.individuals_entry_variable_status = ""
        self.individuals_entry = Entry(self.options_frame)
        self.individuals_entry.place(x=160, y=20, width=120, height=20)
        self.individuals_entry.config(foreground="black", font=("Terminal", 11), justify=CENTER)
        self.individuals_entry.bind("<Key>", self.process_individuals_data_update)
        self.individuals_entry.bind("<KeyRelease>", self.process_individuals_data)

        self.food_label = Label(self.options_frame, text="Initial food per epoch:", anchor="w")
        self.food_label.place(x=20, y=60, width=120, height=20)
        self.food_label.config(background="gray8", foreground="white", font=("Terminal", 11))

        self.food_entry_variable_status = ""
        self.food_entry = Entry(self.options_frame)
        self.food_entry.place(x=160, y=60, width=120, height=20)
        self.food_entry.config(foreground="black", font=("Terminal", 11), justify=CENTER)
        self.food_entry.bind("<Key>", self.process_food_data_update)
        self.food_entry.bind("<KeyRelease>", self.process_food_data)

        self.epochs_label = Label(self.options_frame, text="Number of epochs:", anchor="w")
        self.epochs_label.place(x=20, y=100, width=120, height=20)
        self.epochs_label.config(background="gray8", foreground="white", font=("Terminal", 11))

        self.epochs_entry_variable_status = ""
        self.epochs_entry = Entry(self.options_frame)
        self.epochs_entry.place(x=160, y=100, width=120, height=20)
        self.epochs_entry.config(foreground="black", font=("Terminal", 11), justify=CENTER)
        self.epochs_entry.bind("<Key>", self.process_epochs_data_update)
        self.epochs_entry.bind("<KeyRelease>", self.process_epochs_data)

        self.default_value = IntVar()
        self.default_values_button = Checkbutton(self.options_frame, variable=self.default_value, onvalue=1, offvalue=0, command=self.process_default)
        self.default_values_button.place(x=17, y=145)
        self.default_values_button.config(background="gray8", foreground="black", font=("Terminal", 11))
        self.default_values_button.bind("<Enter>", lambda event: self.default_values_button.config(cursor="hand2"))
        self.default_values_button.bind("<Button-1>", self.play_default_values_checkbutton_sound)

        self.default_values_label = Label(self.options_frame, text="Default values", anchor="w")
        self.default_values_label.place(x=40, y=145, width=80, height=20)
        self.default_values_label.config(background="gray8", foreground="white", font=("Terminal", 11))

        self.evolution_report_log_value = IntVar()
        self.evolution_report_log_checkbutton = Checkbutton(self.options_frame, variable=self.evolution_report_log_value, onvalue=1, offvalue=0, command=self.process_report_log)
        self.evolution_report_log_checkbutton.place(x=155, y=145)
        self.evolution_report_log_checkbutton.config(background="gray8", foreground="black", font=("Terminal", 11))
        self.evolution_report_log_checkbutton.bind("<Enter>", lambda event: self.evolution_report_log_checkbutton.config(cursor="hand2"))
        self.evolution_report_log_checkbutton.bind("<Button-1>", self.play_default_values_checkbutton_sound)

        self.evolution_report_log_label = Label(self.options_frame, text="Create report log", anchor="w")
        self.evolution_report_log_label.place(x=178, y=145, width=100, height=20)
        self.evolution_report_log_label.config(background="gray8", foreground="white", font=("Terminal", 11))

        self.execution_button_text = StringVar()
        self.execution_button_text.set("Run")
        self.execution_button = Button(self.options_frame, textvariable=self.execution_button_text, command=lambda: self.process_execution_button(self.execution_button_text.get().lower()))
        self.execution_button.place(x=20, y=190, width=260, height=50)
        self.execution_button.config(font=("Terminal"))
        self.execution_button.bind("<Enter>", lambda event: self.execution_button.config(cursor="hand2"))
        self.execution_button.bind("<Button-1>", self.play_run_button_sound)

        self.restart_button_text = StringVar()
        self.restart_button_text.set("Restart")
        self.restart_button = Button(self.options_frame, textvariable=self.restart_button_text, command=self.process_restart_button)
        self.restart_button.place(x=20, y=270, width=260, height=50)
        self.restart_button.config(font=("Terminal"), state="disabled")
        self.restart_button.bind("<Enter>", lambda event: self.restart_button.config(cursor="hand2"))
        self.restart_button.bind("<Button-1>", self.play_restart_button_sound)

        self.epoch_progress_bar_label_variable = StringVar()
        self.epoch_progress_bar_label_variable.set("Progress for epoch: 1")
        self.epoch_progress_bar_label = Label(self.options_frame, textvariable=self.epoch_progress_bar_label_variable, anchor="w")
        self.epoch_progress_bar_label.place(x=20, y=340, width=120, height=20)
        self.epoch_progress_bar_label.config(background="gray8", foreground="white", font=("Terminal", 11))

        self.epoch_progress_bar_color_gradient = GradientFrame(self.options_frame, color1="SpringGreen4", color2="OliveDrab1")
        self.epoch_progress_bar_color_gradient.place(x=8, y=368, width=284, height=24)
        self.epoch_progress_bar_color_gradient.config(bd=0, highlightthickness=0, relief='ridge')

        self.epoch_progress = IntVar()
        self.epoch_progress.set(0)
        self.epoch_progress_bar = Progressbar(self.epoch_progress_bar_color_gradient, variable=self.epoch_progress)
        self.epoch_progress_bar.place(x=2, y=2, width=280, height=20)
        self.epoch_progress_bar.config(maximum=100)

        self.algorithm_progress_bar_label = Label(self.options_frame, text="Progress for the algorithm:", anchor="w")
        self.algorithm_progress_bar_label.place(x=20, y=420, width=140, height=20)
        self.algorithm_progress_bar_label.config(background="gray8", foreground="white", font=("Terminal", 11))

        self.algorithm_progress_bar_color_gradient = GradientFrame(self.options_frame, color1="OliveDrab1", color2="SpringGreen4")
        self.algorithm_progress_bar_color_gradient.place(x=8, y=448, width=284, height=24)
        self.algorithm_progress_bar_color_gradient.config(bd=0, highlightthickness=0, relief='ridge')

        self.algorithm_progress = IntVar()
        self.algorithm_progress.set(0)
        self.algorithm_progress_bar = Progressbar(self.algorithm_progress_bar_color_gradient, variable=self.algorithm_progress)
        self.algorithm_progress_bar.place(x=2, y=2, width=280, height=20)
        self.algorithm_progress_bar.config(maximum=100)

        self.type_of_notification = "stop"
        self.default_evolution_data = [5, 15, 10]
        self.min_max_individuals_data = [5, 15]
        self.min_max_food_data = [10, 60]
        self.min_max_epochs_data = [5, 100]

        # Variables for sending messages to the main terminal and the errors terminal
        self.type_of_notification = ""
        self.message = ""
        self.extra_message_data = []
        self.set_terminal_status = True

        # Variables for the calculation of the time of execution of the algorithm
        self.start_time_of_algorithm = 0
        self.end_time_of_algorithm = 0
        self.start_stopped_time_of_algorithm = 0
        self.end_stopped_time_of_algorithm = 0
        self.full_stopped_time_of_algorithm = 0
        self.scale_of_time = ""

        # Variable for the update of the environment buttons status
        self.switch_environment_status = ""

        # Variable to know if the running command came from the root menu, the main terminal or from pressing the button of run in this frame
        self.execution_origin = "in_frame"

        # Variable to contain if it should be created or not in the evolution frame and, if it should be created, then the file path is passed too
        self.evolution_report_log_information = [False, ""]

        # Variable for setting a default path for the evolution report log
        self.default_evolution_report_log_path = None

        # Variable to check if there are operators or any other non valid character inserted by the user in the entry widgets
        self.non_valid_characters = ["%", "/", "*", "-", "+", ":", "[", "]", "¨", "{", "}", "=", "!", "¡", "?", "¿", "'", '"', ",", ";", ".", "_", "-", "|", "\\", "ª", "#", "º", "@", "·", "&", "$", "ç", "~", "<", ">"]

    def process_execution_button(self, type_of_execution):
        """Manage the execution button, to change the label, initialize the algorithm data in the external file and notify the observer"""

        if type_of_execution == "run" and self.execution_button_text.get().lower() == "run":
            if self.default_value.get() == 0:
                if self.fault_of_data():
                    if self.execution_origin == "out_frame":
                        self.type_of_notification = "execution_failed"
                        self.notify()
                        self.execution_origin = "in_frame"
                    return
                else:
                    self.type_of_notification = "update_time"
                    self.scale_of_time = "restart"
                    self.notify()
                    self.start_time_of_algorithm = int(time() * 1000)
                    self.prepare_notification("message", "Using the passed values on the election panel to operate in the genetic algorithm:", ["gray70", 2, 0, False])
                    self.prepare_notification("message", "Number of individuals   -> ", ["gray70", 1, 0, False])
                    self.prepare_notification("message", "{}".format(self.individuals_entry.get()), ["OliveDrab1", 0, 0, False])
                    self.prepare_notification("message", "Number of initial food  -> ", ["gray70", 1, 0, False])
                    self.prepare_notification("message", "{}".format(self.food_entry.get()), ["OliveDrab1", 0, 0, False])
                    self.prepare_notification("message", "Number of epochs        -> ", ["gray70", 1, 0, False])
                    self.prepare_notification("message", "{}".format(self.epochs_entry.get()), ["OliveDrab1", 0, 1, False])
            else:
                self.type_of_notification = "update_time"
                self.scale_of_time = "restart"
                self.notify()
                self.start_time_of_algorithm = int(time() * 1000)
                self.prepare_notification("message", "Using default values to operate in the genetic algorithm:", ["gray70", 2, 0, False])
                self.prepare_notification("message", "Number of individuals   -> ", ["gray70", 1, 0, False])
                self.prepare_notification("message", "{}".format(self.default_evolution_data[0]), ["OliveDrab1", 0, 0, False])
                self.prepare_notification("message", "Number of initial food  -> ", ["gray70", 1, 0, False])
                self.prepare_notification("message", "{}".format(self.default_evolution_data[1]), ["OliveDrab1", 0, 0, False])
                self.prepare_notification("message", "Number of epochs        -> ", ["gray70", 1, 0, False])
                self.prepare_notification("message", "{}".format(self.default_evolution_data[2]), ["OliveDrab1", 0, 1, False])
            
            # If the user activated the creation of a report log for the algorithm execution then the application ask for a path to save the result file with the information
            # The path is then send to the evolution frame in order for it to write the data into the file while the algorithm runs
            self.evolution_report_log_information = [False, ""]
            if self.evolution_report_log_value.get() == 1:
                if self.default_evolution_report_log_path != None:
                    self.evolution_report_log_information[0] = True
                    self.evolution_report_log_information[1] = self.default_evolution_report_log_path
                    self.prepare_notification("message", "Using default path for the report log --> ", ["gray70", 1, 0, False])
                    self.prepare_notification("message", self.default_evolution_report_log_path, ["OliveDrab1", 0, 1, False])
                else:
                    files = [("All Files", "*.*"), ("Text Document", "*.txt")]
                    evolution_report_log_path = FileDialog.asksaveasfile(defaultextension=".txt", filetypes=files)

                    if evolution_report_log_path != None:
                        self.evolution_report_log_information[0] = True
                        self.evolution_report_log_information[1] = evolution_report_log_path.name
                        self.prepare_notification("message", "Selected path for the evolution report log -> ", ["gray70", 1, 0, False])
                        self.prepare_notification("message", evolution_report_log_path.name, ["OliveDrab1", 0, 1, False])
                    else:
                        self.prepare_notification("message", "The creation of a report log for the algorithm was activated but no path was provided, so the application won't create the report", ["gray70", 1, 1, False])
                        ReportsLogGenerator.write_error_data_to_log("warning/info", "The creation of a report log for the algorithm was activated but no path was provided / The application won't create the report")

            self.execution_origin = "in_frame"
            self.restart_button.config(state="normal")
            self.execution_button_text.set("Stop")
            self.default_values_button.config(state="disabled")
            self.evolution_report_log_checkbutton.config(state="disabled")
            self.type_of_notification = "terminal_status"
            self.set_terminal_status = False
            self.notify()
            self.type_of_notification = "switch_buttons_state"
            self.switch_environment_status = "disabled"
            self.notify()
            self.type_of_notification = "run"
            self.notify()
        elif type_of_execution == "run":
            self.prepare_notification("warning", "The algorithm is already running", [1, 0])
            ReportsLogGenerator.write_error_data_to_log(type="warning", message="The algorithm is already running")
            return

        if type_of_execution == "stop" and self.execution_button_text.get().lower() == "stop":
            self.start_stopped_time_of_algorithm = int(time() * 1000)
            self.execution_button_text.set("Continue")
            self.type_of_notification = "stop"
            self.notify()
        elif type_of_execution == "stop":
            self.prepare_notification("warning", "The algorithm was already stopped", [1, 0])
            ReportsLogGenerator.write_error_data_to_log(type="warning", message="The algorithm was already stopped")
            return

        if type_of_execution == "continue" and self.execution_button_text.get().lower() == "continue":
            self.end_stopped_time_of_algorithm = int(time() * 1000)
            self.full_stopped_time_of_algorithm += (self.end_stopped_time_of_algorithm - self.start_stopped_time_of_algorithm)
            self.start_stopped_time_of_algorithm = 0
            self.end_stopped_time_of_algorithm = 0
            self.execution_button_text.set("Stop")
            self.type_of_notification = "continue"
            self.notify()
        elif type_of_execution == "continue":
            if self.restart_button["state"] != DISABLED:
                self.prepare_notification("warning", "The algorithm is already running", [1, 0])
                ReportsLogGenerator.write_error_data_to_log(type="warning", message="The algorithm is already running")
            else:
                self.prepare_notification("warning", "You cannot continue the execution of the algorithm as it has not been started", [1, 0])
                ReportsLogGenerator.write_error_data_to_log(type="warning", message="You cannot continue the execution of the algorithm as it has not been started")
            return

    def process_restart_button(self):
        """Manage the reinitialization of the genetic algorithm and its values"""

        if self.execution_button_text.get().lower() != "run":
            result = MessageBox.askokcancel("Ask", "Are you sure")
            if result:
                #Restart the buttons of the frame
                self.restart_button.config(state="disabled")
                self.execution_button_text.set("Run")
                self.default_values_button.config(state="normal")
                self.evolution_report_log_checkbutton.config(state="normal")

                # Restart the progress bars
                self.epoch_progress.set(0)
                self.epoch_progress_bar_label_variable.set("Progress for epoch: 0")
                self.algorithm_progress.set(0)

                # Restart the algorithm on the evolution frame
                self.type_of_notification = "restart"
                self.notify()

                # Set the status for the main terminal to normal again
                self.type_of_notification = "terminal_status"
                self.set_terminal_status = True
                self.notify()

                # Get the end time of the algorithm to calculate the full time it took to execute
                # In this case it will not be the full time, but only the time will be until the restart button is pressed
                self.type_of_notification = "update_time"
                self.scale_of_time = "restart"
                self.notify()
                self.start_time_of_algorithm = 0
                self.end_time_of_algorithm = 0
                self.start_stopped_time_of_algorithm = 0
                self.end_stopped_time_of_algorithm = 0
                self.full_stopped_time_of_algorithm = 0
                self.scale_of_time = ""

                # Set to normal the status of the environment buttons
                self.type_of_notification = "switch_buttons_state"
                self.switch_environment_status = "normal"
                self.notify()
        else:
            self.prepare_notification("warning", "You first have to run the algorithm in order to restart it's values", [1, 0])
            ReportsLogGenerator.write_error_data_to_log(type="warning", message="You first have to run the algorithm in order to restart it's values")

    def fault_of_data(self):
        """
        Analyze the data to be process by the algorithm before starting it.
        In case there is an error the algorithm wont start.
        """

        if self.individuals_entry.get() == "" or self.food_entry.get() == "" or self.epochs_entry.get() == "":
            self.prepare_notification("error", "You have to introduce all values for the individuals, food and epochs data in order to run the algorithm or press the default button", [1, 0])
            ReportsLogGenerator.write_error_data_to_log(type="error", message="You have to introduce all values for the individuals, food and epochs data in order to run the algorithm or press the default button")
            return True
        elif self.individuals_entry_variable_status == "error" or self.food_entry_variable_status == "error" or self.epochs_entry_variable_status == "error":
            self.prepare_notification("error", "You have inserted wrong data in the entry widgets", [1, 0])
            ReportsLogGenerator.write_error_data_to_log(type="error", message="You have inserted wrong data in the entry widgets")
            return True
        elif self.individuals_entry_variable_status == "num_error" or self.food_entry_variable_status == "num_error" or self.epochs_entry_variable_status == "num_error":
            self.prepare_notification("error", "Values for the algorithm should be between:\nIndividuals --> [{}, {}]\nFood --> [{}, {}]\nEpochs --> [{}, {}]".format(
                self.min_max_individuals_data[0],
                self.min_max_individuals_data[1],
                self.min_max_food_data[0],
                self.min_max_food_data[1],
                self.min_max_epochs_data[0],
                self.min_max_epochs_data[1]
            ), [1, 0])
            ReportsLogGenerator.write_error_data_to_log(type="error", message="Passed values for the algorithm are off limits, choose another ones between the stablished limit values.")
            return True
        
        return False

    def process_default(self):
        """Disables and enables the insertion of data in the election panel, depending on whether or not the default button is activated."""

        if self.default_value.get() == 1:
            self.individuals_entry.config(state="disabled")
            self.food_entry.config(state="disabled")
            self.epochs_entry.config(state="disabled")
            self.prepare_notification("message", "Default data --> ", ["gray70", 2, 0, False])
            self.prepare_notification("message", "ACTIVE", ["OliveDrab1", 0, 2, True])
        elif self.default_value.get() == 0:
            self.individuals_entry.config(state="normal")
            self.food_entry.config(state="normal")
            self.epochs_entry.config(state="normal")
            self.prepare_notification("message", "Default data --> ", ["gray70", 2, 0, False])
            self.prepare_notification("message", "DEACTIVE", ["OliveDrab1", 0, 2, True])

    def process_report_log(self):
        """Sends information to the main terminal whenever the report log checkbutton is activated or deactivated"""

        if self.evolution_report_log_value.get() == 1:
            self.prepare_notification("message", "Create evolution report log --> ", ["gray70", 2, 0, False])
            self.prepare_notification("message", "ACTIVE", ["OliveDrab1", 0, 2, True])
        elif self.evolution_report_log_value.get() == 0:
            self.prepare_notification("message", "Create evolution report log --> ", ["gray70", 2, 0, False])
            self.prepare_notification("message", "DEACTIVE", ["OliveDrab1", 0, 2, True])

    """
    When the user inserts data into the entry the stored value is the one before the insert so for the algorithm to get the new value there has to be an update on the entry widget.
    This method will serve like and "update" method binded to the widget but will do nothing. So when a user press and release a key from the board the stored values will go as follows:
        1. The user press the 1 key and the stored value will be "", because it stores the value before the 1 was inserted
        2. The user release the 1 key and then the stored value will be "1" because the release event updated the widget and the new value could be stored and took from the get() method of the widget
    So what is really happening is that the second event binded to the entry widget gave back the real value the user inserted after updating the so said widget.
    This is done for the three entry widgets on the elections panel
    """
    def process_individuals_data_update(self, event):
        pass

    def process_food_data_update(self, event):
        pass

    def process_epochs_data_update(self, event):
        pass

    def process_individuals_data(self, event):
        """Looks for errors in the individuals entry data"""
        
        if any([char.isalpha() or char in self.non_valid_characters for char in self.individuals_entry.get()]):
            self.individuals_entry.config(foreground="red")
            self.individuals_entry_variable_status = "error"
        elif self.individuals_entry.get() != "" and (int(self.individuals_entry.get()) < self.min_max_individuals_data[0] or int(self.individuals_entry.get()) > self.min_max_individuals_data[1]):
            self.individuals_entry.config(foreground="red")
            self.individuals_entry_variable_status = "num_error"
        else:
            self.individuals_entry.config(foreground="black")
            self.individuals_entry_variable_status = "ok"

    def process_food_data(self, event):
        """Looks for errors in the food entry data"""
        
        if any([char.isalpha() or char in self.non_valid_characters for char in self.food_entry.get()]):
            self.food_entry.config(foreground="red")
            self.food_entry_variable_status = "error"
        elif self.food_entry.get() != "" and (int(self.food_entry.get()) < self.min_max_food_data[0] or int(self.food_entry.get()) > self.min_max_food_data[1]):
            self.food_entry.config(foreground="red")
            self.food_entry_variable_status = "num_error"
        else:
            self.food_entry.config(foreground="black")
            self.food_entry_variable_status = "ok"

    def process_epochs_data(self, event):
        """Looks for errors in the epochs entry data"""

        if any([char.isalpha() or char in self.non_valid_characters for char in self.epochs_entry.get()]):
            self.epochs_entry.config(foreground="red")
            self.epochs_entry_variable_status = "error"
        elif self.epochs_entry.get() != "" and (int(self.epochs_entry.get()) < self.min_max_epochs_data[0] or int(self.epochs_entry.get()) > self.min_max_epochs_data[1]):
            self.epochs_entry.config(foreground="red")
            self.epochs_entry_variable_status = "num_error"
        else:
            self.epochs_entry.config(foreground="black")
            self.epochs_entry_variable_status = "ok"
    
    def subscribe(self, observer: Observer) -> None:
        """Subscribes an observer to the publisher"""

        self._observers.append(observer)

    def unsubscribe(self, observer: Observer) -> None:
        """Unsubscribes an observer from the publisher"""

        self._observers.remove(observer)

    def notify(self) -> None:
        """Notify all observer about an event"""

        if self.type_of_notification == "run":
            data = self.default_evolution_data
            if self.default_value.get() == 0:
                data = [int(self.individuals_entry.get()), int(self.food_entry.get()), int(self.epochs_entry.get())]
            for observers in self._observers:
                observers.update(self.type_of_notification, data, self.evolution_report_log_information)
        elif self.type_of_notification == "stop" or self.type_of_notification == "continue" or self.type_of_notification == "restart":
            for observers in self._observers:
                observers.update(self.type_of_notification)
        elif self.type_of_notification == "message" or self.type_of_notification == "error" or self.type_of_notification == "warning" or self.type_of_notification == "info":
            for observers in self._observers:
                observers.update(self.type_of_notification, self.message, self.extra_message_data)
        elif self.type_of_notification == "terminal_status":
            for observers in self._observers:
                observers.update(self.type_of_notification, self.set_terminal_status)
        elif self.type_of_notification == "update_time":
            for observers in self._observers:
                observers.update(self.type_of_notification, self.transform_time(self.start_time_of_algorithm, self.end_time_of_algorithm, self.scale_of_time), self.scale_of_time)
        elif self.type_of_notification == "switch_buttons_state":
            for observers in self._observers:
                observers.update(self.type_of_notification, self.switch_environment_status)
        elif self.type_of_notification == "execution_failed":
            for observers in self._observers:
                observers.update(self.type_of_notification)

    def update(self, *args) -> None:
        """Receive the update from the publisher"""

        if args[0] in ["run", "stop", "continue"]:
            self.execution_origin = "out_frame"
            self.process_execution_button(args[0])
        elif args[0] == "restart": self.process_restart_button()
        elif args[0] == "finish_execution":
            # Get the end time of the algorithm to calculate the full time it took to execute
            # In this case the time calcultated will be the full time the algorithm has been in execution
            self.end_time_of_algorithm = int(time() * 1000)
            self.type_of_notification = "update_time"
            self.scale_of_time = "minutes"
            self.notify()

            if self.evolution_report_log_information[0]:
                # Write last data of the execution of the algorithm to the evolution report log
                ReportsLogGenerator.write_evolution_data_to_log(
                    reports_path=self.evolution_report_log_information[1], 
                    data=[args[1], [self.transform_time(self.start_time_of_algorithm, self.end_time_of_algorithm, self.scale_of_time), self.scale_of_time]], 
                    running_state="finish_report_data"
                )

            # Reset the variables that calculate the time of execution of the algorithm
            self.start_time_of_algorithm = 0
            self.end_time_of_algorithm = 0
            self.start_stopped_time_of_algorithm = 0
            self.end_stopped_time_of_algorithm = 0
            self.full_stopped_time_of_algorithm = 0
            self.scale_of_time = ""

            # Restart all the buttons on the panel and set the main terminal to normal state
            self.restart_button.config(state="disabled")
            self.execution_button_text.set("Run")
            self.default_values_button.config(state="normal")
            self.evolution_report_log_checkbutton.config(state="normal")

            # This notification makes the main terminal available
            self.type_of_notification = "terminal_status"
            self.set_terminal_status = True
            self.notify()

            # Restart the progress bars
            self.epoch_progress.set(0)
            self.epoch_progress_bar_label_variable.set("Progress for epoch: 0")
            self.algorithm_progress.set(0)

            # Set to normal the status of the environment buttons
            self.type_of_notification = "switch_buttons_state"
            self.switch_environment_status = "normal"
            self.notify()
        elif args[0] == "progress_epoch_bar":
            self.epoch_progress.set(self.epoch_progress.get() + 1)
            if args[1]: 
                self.epoch_progress_bar_label_variable.set("Progress for epoch: " + str(int(self.epoch_progress_bar_label_variable.get()[-1]) + 1))
                self.epoch_progress.set(0)
        elif args[0] == "progress_algorithm_bar":
            self.algorithm_progress.set(args[1])
        elif args[0] == "change_environment":
            if args[1] == "polar":
                self.gradient.set_new_colors("magenta4", "RoyalBlue2")
                self.epoch_progress_bar_color_gradient.set_new_colors("magenta4", "RoyalBlue2")
                self.algorithm_progress_bar_color_gradient.set_new_colors("RoyalBlue2", "magenta4")
                self.min_max_food_data = [10, 60]
            elif args[1] == "mediterranean":
                self.gradient.set_new_colors("SpringGreen4", "OliveDrab1")
                self.epoch_progress_bar_color_gradient.set_new_colors("SpringGreen4", "OliveDrab1")
                self.algorithm_progress_bar_color_gradient.set_new_colors("OliveDrab1", "SpringGreen4")
                self.min_max_food_data = [10, 60]
            elif args[1] == "desert":
                self.gradient.set_new_colors("brown", "goldenrod1")
                self.epoch_progress_bar_color_gradient.set_new_colors("brown", "goldenrod1")
                self.algorithm_progress_bar_color_gradient.set_new_colors("goldenrod1", "brown")
                self.min_max_food_data = [5, 30]
        elif args[0] == "set_default_path":
            self.default_evolution_report_log_path = args[1]
        elif args[0] == "unset_default_path":
            self.default_evolution_report_log_path = None

    def prepare_notification(self, type, message, extra):
        """This method will be called when a message is send from the election frame to the main terminal or the errors terminal"""
        
        self.type_of_notification = type
        self.message = message
        self.extra_message_data = extra
        self.notify()

    def transform_time(self, start_time, end_time, scale):
        """This method will transform time passed in milliseconds to the choosen scale"""

        # The final time of the algorithm will be the substract of the end time and the start time, minus the time the algorithm might have been stopped by the user
        final_time = (end_time - start_time) - self.full_stopped_time_of_algorithm

        if scale == "seconds": return int(round(final_time / 1000, 0))
        elif scale == "minutes": return int(round((final_time / 1000) / 60, 0))
        elif scale == "hours": return int(round(((final_time / 1000) / 60) / 60, 0))
        elif scale == "restart": return 0

    def play_run_button_sound(self, event):
        """This method loads and plays the sound of a button been pressed for the (run, stop, continue) button"""

        SoundEffects.button_click.play(loops=0)

    def play_restart_button_sound(self, event):
        """This method loads and plays the sound of a button been pressed for the restart button"""

        if self.restart_button["state"] == DISABLED:
            SoundEffects.error_click.play(loops=0)
            self.prepare_notification("warning", "You first have to run the algorithm in order to restart it's values", [1, 0])
            ReportsLogGenerator.write_error_data_to_log(type="warning", message="You first have to run the algorithm in order to restart it's values")
        else: SoundEffects.button_click.play(loops=0)

    def play_default_values_checkbutton_sound(self, event):
        """This method loads and plays the sound of a checkbutton been pressed for the default values checkbutton"""

        if self.default_values_button["state"] == DISABLED or self.evolution_report_log_checkbutton["state"] == DISABLED:
            SoundEffects.error_click.play(loops=0)
            self.prepare_notification("warning", "You cannot change the default values nor the create report log status while the algorithm is running", [1, 0])
            ReportsLogGenerator.write_error_data_to_log(type="warning", message="You cannot change the default values nor the create report log status while the algorithm is running")
        else: SoundEffects.checkbutton_click.play(loops=0)