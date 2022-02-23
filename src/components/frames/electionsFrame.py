import os
from tkinter import *
from components.models.gradients import GradientFrame
from components.interfaces.observer import Observer
from components.interfaces.publisher import Publisher
from typing import List
from io import open

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
        self.execution_button.place(x=20, y=430, width=260, height=50)
        self.execution_button.config(font=("Terminal"))

        self.individuals_label = Label(self.options_frame, text="Number of individuals:", anchor="w")
        self.individuals_label.place(x=20, y=20, width=120, height=20)
        self.individuals_label.config(background="gray8", foreground="white", font=("Terminal", 11))

        self.individuals_entry_variable = ""
        self.individuals_entry = Entry(self.options_frame, textvariable=self.individuals_entry_variable)
        self.individuals_entry.place(x=140, y=20, width=120, height=20)
        self.individuals_entry.config(foreground="black", font=("Terminal", 11), justify=CENTER)
        self.individuals_entry.bind("<Key>", self.process_individuals_data)

        self.food_label = Label(self.options_frame, text="Initial food per epoch:", anchor="w")
        self.food_label.place(x=20, y=60, width=120, height=20)
        self.food_label.config(background="gray8", foreground="white", font=("Terminal", 11))

        self.food_entry_variable = ""
        self.food_entry = Entry(self.options_frame, textvariable=self.food_entry_variable)
        self.food_entry.place(x=140, y=60, width=120, height=20)
        self.food_entry.config(foreground="black", font=("Terminal", 11), justify=CENTER)
        self.food_entry.bind("<Key>", self.process_food_data)

        self.epochs_label = Label(self.options_frame, text="Number of epochs:", anchor="w")
        self.epochs_label.place(x=20, y=100, width=120, height=20)
        self.epochs_label.config(background="gray8", foreground="white", font=("Terminal", 11))

        self.epochs_entry_variable = ""
        self.epochs_entry = Entry(self.options_frame, textvariable=self.epochs_entry_variable)
        self.epochs_entry.place(x=140, y=100, width=120, height=20)
        self.epochs_entry.config(foreground="black", font=("Terminal", 11), justify=CENTER)
        self.epochs_entry.bind("<Key>", self.process_epochs_data)

        self.execution_status = "stop"

    def process_execution_button(self, type_of_execution):
        """Manage the execution button, to change the label, initialize the algorithm data in the external file and notify the observer"""
        if type_of_execution == "run" and self.execution_status == "stop":
            self.comunicate_data()
            self.execution_button_text.set("Stop")
            self.execution_status = "run"
            self.notify()
        elif type_of_execution == "stop" and self.execution_status == "run":
            self.execution_button_text.set("Run")
            self.execution_status = "stop"
            self.notify()

    def comunicate_data(self):
        file = open(os.getcwd().replace("\\", "/") + "/archive/initialValuesForGeneticAlgorithm.txt", "w")
        file.write(self.individuals_entry_variable + " " + self.food_entry_variable + " " + self.epochs_entry_variable)
        file.close()

    def process_individuals_data(self, event):
        """Looks for errors in the individuals entry data"""

        if event.keysym == "BackSpace":
            self.individuals_entry_variable = self.individuals_entry_variable[:-1]
        else:
            self.individuals_entry_variable += event.char
        
        if any([char.isalpha() for char in self.individuals_entry_variable]):
            self.individuals_entry.config(foreground="red")
        else:
            self.individuals_entry.config(foreground="black")

    def process_food_data(self, event):
        """Looks for errors in the food entry data"""

        if event.keysym == "BackSpace":
            self.food_entry_variable = self.food_entry_variable[:-1]
        else:
            self.food_entry_variable += event.char
        
        if any([char.isalpha() for char in self.food_entry_variable]):
            self.food_entry.config(foreground="red")
        else:
            self.food_entry.config(foreground="black")

    def process_epochs_data(self, event):
        """Looks for errors in the epochs entry data"""

        if event.keysym == "BackSpace":
            self.epochs_entry_variable = self.epochs_entry_variable[:-1]
        else:
            self.epochs_entry_variable += event.char

        if any([char.isalpha() for char in self.epochs_entry_variable]):
            self.epochs_entry.config(foreground="red")
        else:
            self.epochs_entry.config(foreground="black")
    
    def subscribe(self, observer: Observer) -> None:
        """Subscribes an observer to the publisher"""

        self._observers.append(observer)

    def unsubscribe(self, observer: Observer) -> None:
        """Unsubscribes an observer from the publisher"""

        self._observers.remove(observer)

    def notify(self) -> None:
        """Notify all observer about an event"""

        for observers in self._observers:
            observers.update(self, self.execution_status)

    def update(self, Publisher: Publisher, *args) -> None:
        """Receive the update from the publisher"""

        self.process_execution_button(args[0])