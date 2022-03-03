from tkinter import *
from tkinter import messagebox as MessageBox
from components.models.gradients import GradientFrame
from components.interfaces.observer import Observer
from components.interfaces.publisher import Publisher
from typing import List

class ElectionsFrame(Frame, Publisher, Observer):

    """This frame contains the different options the user can use to change characteristics, insert new objects and start the application"""

    def __init__(self, root):
        Frame.__init__(self, root)
        self.config(bg="dark turquoise")

        self._observers: List[Observer] = []

        self.gradient = GradientFrame(self, "magenta4", "RoyalBlue2")
        self.gradient.pack()
        self.gradient.config(bd=0, highlightthickness=0, relief='ridge')

        self.options_frame = Frame(self.gradient, width=300, height=500)
        self.options_frame.pack(fill=BOTH, padx=2, pady=2)
        self.options_frame.pack_propagate(0)
        self.options_frame.configure(background="gray8")

        self.execution_button_text = StringVar()
        self.execution_button_text.set("Run")
        self.execution_button = Button(self.options_frame, textvariable=self.execution_button_text, command=lambda: self.process_execution_button(self.execution_button_text.get().lower()))
        self.execution_button.place(x=20, y=360, width=260, height=50)
        self.execution_button.config(font=("Terminal"))

        self.restart_button_text = StringVar()
        self.restart_button_text.set("Restart")
        self.restart_button = Button(self.options_frame, textvariable=self.restart_button_text, command=self.process_restart_button)
        self.restart_button.place(x=20, y=430, width=260, height=50)
        self.restart_button.config(font=("Terminal"), state="disabled")

        self.individuals_label = Label(self.options_frame, text="Number of individuals:", anchor="w")
        self.individuals_label.place(x=20, y=20, width=120, height=20)
        self.individuals_label.config(background="gray8", foreground="white", font=("Terminal", 11))

        self.individuals_entry_variable = ""
        self.individuals_entry_variable_status = ""
        self.individuals_entry = Entry(self.options_frame, textvariable=self.individuals_entry_variable)
        self.individuals_entry.place(x=160, y=20, width=120, height=20)
        self.individuals_entry.config(foreground="black", font=("Terminal", 11), justify=CENTER)
        self.individuals_entry.bind("<Key>", self.process_individuals_data)

        self.food_label = Label(self.options_frame, text="Initial food per epoch:", anchor="w")
        self.food_label.place(x=20, y=60, width=120, height=20)
        self.food_label.config(background="gray8", foreground="white", font=("Terminal", 11))

        self.food_entry_variable = ""
        self.food_entry_variable_status = ""
        self.food_entry = Entry(self.options_frame, textvariable=self.food_entry_variable)
        self.food_entry.place(x=160, y=60, width=120, height=20)
        self.food_entry.config(foreground="black", font=("Terminal", 11), justify=CENTER)
        self.food_entry.bind("<Key>", self.process_food_data)

        self.epochs_label = Label(self.options_frame, text="Number of epochs:", anchor="w")
        self.epochs_label.place(x=20, y=100, width=120, height=20)
        self.epochs_label.config(background="gray8", foreground="white", font=("Terminal", 11))

        self.epochs_entry_variable = ""
        self.epochs_entry_variable_status = ""
        self.epochs_entry = Entry(self.options_frame, textvariable=self.epochs_entry_variable)
        self.epochs_entry.place(x=160, y=100, width=120, height=20)
        self.epochs_entry.config(foreground="black", font=("Terminal", 11), justify=CENTER)
        self.epochs_entry.bind("<Key>", self.process_epochs_data)

        self.type_of_notification = "stop"

        self.default_value = IntVar()
        self.default_values_button = Checkbutton(self.options_frame, variable=self.default_value, onvalue=1, offvalue=0, command=self.process_default)
        self.default_values_button.place(x=17, y=140)
        self.default_values_button.config(background="gray8", foreground="black", font=("Terminal", 11))

        self.default_values_label = Label(self.options_frame, text="Default values", anchor="w")
        self.default_values_label.place(x=40, y=140, width=120, height=20)
        self.default_values_label.config(background="gray8", foreground="white", font=("Terminal", 11))

    def process_execution_button(self, type_of_execution):
        """Manage the execution button, to change the label, initialize the algorithm data in the external file and notify the observer"""

        if type_of_execution == "run" and self.execution_button_text.get().lower() == "run":
            if self.default_value.get() == 0:
                if self.fault_of_data(): return
                else: self.type_of_notification = "passed_values"
            else: self.type_of_notification = "default_values"
            self.notify()
            self.restart_button
            self.restart_button.config(state="normal")
            self.execution_button_text.set("Stop")
            self.type_of_notification = "run"
            self.notify()
        elif type_of_execution == "stop" and self.execution_button_text.get().lower() == "stop":
            self.execution_button_text.set("Continue")
            self.type_of_notification = "stop"
            self.notify()
        elif type_of_execution == "continue" and self.execution_button_text.get().lower() == "continue":
            self.execution_button_text.set("Stop")
            self.type_of_notification = "continue"
            self.notify()

    def process_restart_button(self):
        """Manage the reinitialization of the genetic algorithm and its values"""

        if self.execution_button_text.get().lower() != "run":
            result = MessageBox.askokcancel("Ask", "Are you sure")
            if result:
                self.restart_button.config(state="disabled")
                self.execution_button_text.set("Run")
                self.type_of_notification = "restart"
                self.notify()
        else:
            self.type_of_notification = "warning"
            self.error_message = "You first have to run the algorithm in order to restart it's values"
            self.notify()

    def fault_of_data(self):
        """
        Analyze the data to be process by the algorithm before starting it.
        In case there is an error the algorithm wont start.
        """

        if self.individuals_entry_variable == "" or self.food_entry_variable == "" or self.epochs_entry_variable == "":
            self.type_of_notification = "error"
            self.error_message = "You have to introduce all values for the individuals, food and epochs data in order to run the algorithm or press the default button"
            self.notify()
            return True
        elif self.individuals_entry_variable_status == "error" or self.food_entry_variable_status == "error" or self.epochs_entry_variable_status == "error":
            self.type_of_notification = "error"
            self.error_message = "You have inserted wrong data in the elections panel"
            self.notify()
            return True
        
        return False

    def process_default(self):
        """Disables and enables the insertion of data in the election panel, depending on whether or not the default button is activated."""

        if self.default_value.get() == 1:
            self.individuals_entry.config(state="disabled")
            self.food_entry.config(state="disabled")
            self.epochs_entry.config(state="disabled")
        elif self.default_value.get() == 0:
            self.individuals_entry.config(state="normal")
            self.food_entry.config(state="normal")
            self.epochs_entry.config(state="normal")

    def process_individuals_data(self, event):
        """Looks for errors in the individuals entry data"""

        if event.keysym == "BackSpace":
            self.individuals_entry_variable = self.individuals_entry_variable[:-1]
        else:
            self.individuals_entry_variable += event.char
        
        if any([char.isalpha() for char in self.individuals_entry_variable]):
            self.individuals_entry.config(foreground="red")
            self.individuals_entry_variable_status = "error"
        else:
            self.individuals_entry.config(foreground="black")
            self.individuals_entry_variable_status = "ok"

    def process_food_data(self, event):
        """Looks for errors in the food entry data"""

        if event.keysym == "BackSpace":
            self.food_entry_variable = self.food_entry_variable[:-1]
        else:
            self.food_entry_variable += event.char
        
        if any([char.isalpha() for char in self.food_entry_variable]):
            self.food_entry.config(foreground="red")
            self.food_entry_variable_status = "error"
        else:
            self.food_entry.config(foreground="black")
            self.food_entry_variable_status = "ok"

    def process_epochs_data(self, event):
        """Looks for errors in the epochs entry data"""

        if event.keysym == "BackSpace":
            self.epochs_entry_variable = self.epochs_entry_variable[:-1]
        else:
            self.epochs_entry_variable += event.char

        if any([char.isalpha() for char in self.epochs_entry_variable]):
            self.epochs_entry.config(foreground="red")
            self.epochs_entry_variable_status = "error"
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
            data = []
            if self.default_value.get() == 0:
                data = [int(self.individuals_entry_variable), int(self.food_entry_variable), int(self.epochs_entry_variable)]
            elif self.default_value.get() == 1:
                data = [10, 5, 10]
            for observers in self._observers:
                observers.update(self, self.type_of_notification, data)
        elif self.type_of_notification == "stop" or self.type_of_notification == "continue" or self.type_of_notification == "restart":
            for observers in self._observers:
                observers.update(self, self.type_of_notification)
        elif self.type_of_notification == "error" or self.type_of_notification == "warning":
            for observers in self._observers:
                observers.update(self, self.type_of_notification, self.error_message)
        elif self.type_of_notification == "default_values":
            self.type_of_notification = "values"
            for observers in self._observers:
                observers.update(
                    self, 
                    self.type_of_notification, 
                    "Using default values to operate in the genetic algorithm:\n\nNumber of individuals   -> 10\nNumber of initial food  ->  5\nNumber of epochs        -> 10"
                )
        elif self.type_of_notification == "passed_values":
            self.type_of_notification = "values"
            for observers in self._observers:
                observers.update(
                    self,
                    self.type_of_notification,
                    "Using the passed values on the election panel to operate in the genetic algorithm:\n\nNumber of individuals   -> {}\nNumber of initial food  -> {}\nNumber of epochs        -> {}\n".format(self.individuals_entry_variable, self.food_entry_variable, self.epochs_entry_variable)
                )

    def update(self, Publisher: Publisher, *args) -> None:
        """Receive the update from the publisher"""

        if args[0] in ["run", "stop", "continue"]: self.process_execution_button(args[0])
        elif args[0] == "restart": self.process_restart_button()