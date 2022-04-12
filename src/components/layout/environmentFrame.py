import os
from tkinter import *
from typing import List
from PIL import ImageTk, Image
from components.models.gradients import GradientFrame
from components.interfaces.observer import Observer
from components.interfaces.publisher import Publisher
from components.audio.soundEffects import SoundEffects
from components.generator.reportsLogGenerator import ReportsLogGenerator

class EnvironmentFrame(Frame, Publisher, Observer):

    """This class contains the different buttons to change in between environments"""

    def __init__(self, root):
        Frame.__init__(self, root)
        self.config(background="dark turquoise")

        self._observers: List[Observer] = []

        self.type_of_notification = ""
        self.type_of_environment = ""

        self.gradient_canvas = GradientFrame(self, "OliveDrab1", "SpringGreen4")
        self.gradient_canvas.pack()
        self.gradient_canvas.config(bd=0, highlightthickness=0, relief='ridge')

        # Polar Frame, Image and Button
        self.polar_environment_frame = Frame(self.gradient_canvas, width=300, height=69)
        self.polar_environment_frame.pack(fill=BOTH, padx=2, pady=2)
        self.polar_environment_frame.config(background="gray8")

        self.polar_image = ImageTk.PhotoImage(Image.open(os.getcwd().replace("\\", "/") + "/assets/images/polar.png"))
        self.polar_image_label = Label(self.polar_environment_frame, image=self.polar_image)
        self.polar_image_label.place(x=2, y=2, width=130, height=65)

        self.polar_button = Button(self.polar_environment_frame, text="POLAR", command=lambda: self.pre_notify_environment("polar"))
        self.polar_button.place(x=132, y=2, width=166, height=65)
        self.polar_button.config(font=("Terminal"), background="medium purple", activebackground="medium purple")
        self.polar_button.bind("<Enter>", lambda event: self.polar_button.config(cursor="hand2"))
        self.polar_button.bind("<Button-1>", self.play_button_sound)

        # Mediterranean Frame, Image and Button
        self.mediterranean_environment_frame = Frame(self.gradient_canvas, width=300, height=69)
        self.mediterranean_environment_frame.pack(fill=BOTH, padx=2)
        self.mediterranean_environment_frame.config(background="gray8")

        self.mediterranean_image = ImageTk.PhotoImage(Image.open(os.getcwd().replace("\\", "/") + "/assets/images/mediterranean.png"))
        self.mediterranean_image_label = Label(self.mediterranean_environment_frame, image=self.mediterranean_image)
        self.mediterranean_image_label.place(x=2, y=2, width=130, height=65)

        self.mediterranean_button = Button(self.mediterranean_environment_frame, text="MEDITERRANEAN", command=lambda: self.pre_notify_environment("mediterranean"))
        self.mediterranean_button.place(x=132, y=2, width=166, height=65)
        self.mediterranean_button.config(font=("Terminal"), background="aquamarine2", activebackground="aquamarine2")
        self.mediterranean_button.bind("<Enter>", lambda event: self.mediterranean_button.config(cursor="hand2"))
        self.mediterranean_button.bind("<Button-1>", self.play_button_sound)

        # Desert Frame, Image and Button
        self.desert_environment_frame = Frame(self.gradient_canvas, width=300, height=68)
        self.desert_environment_frame.pack(fill=BOTH, padx=2, pady=2)
        self.desert_environment_frame.config(background="gray8")

        self.desert_image = ImageTk.PhotoImage(Image.open(os.getcwd().replace("\\", "/") + "/assets/images/desert.png"))
        self.desert_image_label = Label(self.desert_environment_frame, image=self.desert_image)
        self.desert_image_label.place(x=2, y=2, width=130, height=64)

        self.desert_button = Button(self.desert_environment_frame, text="DESERT", command=lambda: self.pre_notify_environment("desert"))
        self.desert_button.place(x=132, y=2, width=166, height=64)
        self.desert_button.config(font=("Terminal"), background="burlywood1", activebackground="burlywood1")
        self.desert_button.bind("<Enter>", lambda event: self.desert_button.config(cursor="hand2"))
        self.desert_button.bind("<Button-1>", self.play_button_sound)

        # Variables for sending messages to the main terminal or the errors terminal
        self.type_of_notification = ""
        self.message = ""
        self.extra_message_data = ""

    def subscribe(self, observer: Observer) -> None:
        """Subscribes an observer to the publisher"""

        self._observers.append(observer)

    def unsubscribe(self, observer: Observer) -> None:
        """Unsubscribes an observer from the publisher"""

        self._observers.remove(observer)

    def notify(self) -> None:
        """Notify all observer about an event"""

        if self.type_of_notification == "change_environment":
            for observers in self._observers:
                observers.update(self.type_of_notification, self.type_of_environment)
        elif self.type_of_notification == "message" or self.type_of_notification == "error" or self.type_of_notification == "warning" or self.type_of_notification == "info":
            for observers in self._observers:
                observers.update(self.type_of_notification, self.message, self.extra_message_data)

    def update(self, *args) -> None:
        """Receive the update from the publisher"""

        if args[0] == "switch_buttons_state": self.switch_buttons_state(args[1])
        elif args[0] in ["polar", "mediterranean", "desert"]:
            if self.polar_button["state"] == DISABLED or self.mediterranean_button["state"] == DISABLED or self.desert_button["state"] == DISABLED:
                self.prepare_notification("warning", "You can not use the environment buttons when the algorithm is already running", [1, 0])
                ReportsLogGenerator.write_error_data_to_log(type="warning", message="You can not use the environment buttons when the algorithm is already running")
            else: self.pre_notify_environment(args[0])

    def pre_notify_environment(self, type_of_environment):
        """This method prepares the information about the changing environment before is notified to the observers of this frame"""

        # Change the gradient of this frame
        self.change_gradient(type_of_environment)

        # Change the gradient of the rest of the frames
        self.type_of_notification = "change_environment"
        self.type_of_environment = type_of_environment
        self.notify()

    def change_gradient(self, type_of_environment):
        """This method changes the color of the gradient according to the type of environment the user chooses"""

        if type_of_environment == "polar":
            self.gradient_canvas.set_new_colors("RoyalBlue2", "magenta4")
        elif type_of_environment == "mediterranean":
            self.gradient_canvas.set_new_colors("OliveDrab1", "SpringGreen4")
        elif type_of_environment == "desert":
            self.gradient_canvas.set_new_colors("goldenrod1", "brown")

    def prepare_notification(self, type, message, extra):
        """This method will be called when a message is send from the election frame to the main terminal or the errors terminal"""
        
        self.type_of_notification = type
        self.message = message
        self.extra_message_data = extra
        self.notify()

    def play_button_sound(self, event):
        """This method loads and plays the sound of a button been pressed"""

        if self.polar_button["state"] == DISABLED or self.mediterranean_button["state"] == DISABLED or self.desert_button["state"] == DISABLED:
            SoundEffects.error_click.play(loops=0)
            self.prepare_notification("warning", "You cannot use the environment buttons when the algorithm is already running", [1, 0])
            ReportsLogGenerator.write_error_data_to_log(type="warning", message="You cannot use the environment buttons when the algorithm is already running")
        else:
            SoundEffects.button_click.play(loops=0)

    def switch_buttons_state(self, button_state):
        """This method will be called when the state of the environment buttons need to be changed to disabled or normal"""

        self.polar_button.config(state=button_state)
        self.mediterranean_button.config(state=button_state)
        self.desert_button.config(state=button_state)