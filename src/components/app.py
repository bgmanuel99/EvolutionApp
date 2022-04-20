import os
from tkinter import *
from components.layout.initialFrame import InitialFrame
from components.layout.topFrame import TopFrame
from components.layout.bottomFrame import BottomFrame
from components.layout.rootMenu import RootMenuBar
from components.interfaces.observer import Observer
from components.audio.soundEffects import SoundEffects

class Application(Tk, Observer):

    """Main winfow of the application. It inherits from TK which is the root object of tkinter module to create the GUI"""

    def __init__(self):
        super().__init__()
        self.title("Evolution")
        self.iconbitmap(os.getcwd().replace("\\", "/") + "/assets/icon/evolution.ico")
        self.resizable(0, 0)
        self.protocol("WM_DELETE_WINDOW", self.exit)

        # Set the volume of the application to 100%
        SoundEffects.button_click.set_volume(1)
        SoundEffects.error_click.set_volume(1)
        SoundEffects.checkbutton_click.set_volume(1)

        # Create the intro frame for the application
        self.initial_frame = InitialFrame(self)
        self.initial_frame.pack(fill=BOTH, side=LEFT)

        self.initial_frame.subscribe(self)

        # This variable will set a time in between messages on the initial frame so the user can see the widgets that are been loaded
        self.delay_time = 0

        self.load_main_widgets()

    def load_main_widgets(self):
        """This method loads all the widgets of the application and subscribes the widgets between them so they can comunicate"""

        self.delay_time += 200

        if self.delay_time == 200:
            # Main menu bar for the main window
            self.initial_frame.set_progress_information("Main Menu")
            self.root_menu_bar = RootMenuBar(self)
            self.initial_frame.set_progress_bar(10)

        if self.delay_time == 400:
            # Top frame of the main window
            self.initial_frame.set_progress_information("Top Frame")
            self.top_frame = TopFrame(self)
            self.initial_frame.set_progress_bar(30)

        if self.delay_time == 600:
            # Bottom frame of the main window
            self.initial_frame.set_progress_information("Bottom Frame")
            self.bottom_frame = BottomFrame(self)
            self.initial_frame.set_progress_bar(50)

        if self.delay_time == 800:
            # Subscribers and observers for the Main Menu
            self.initial_frame.set_progress_information("subscribers for the Main Menu")
            self.root_menu_bar.subscribe(self.top_frame.information_frame)
            self.root_menu_bar.subscribe(self.top_frame.elections_frame)
            self.root_menu_bar.subscribe(self.top_frame.environment_frame)
            self.root_menu_bar.subscribe(self)
            self.initial_frame.set_progress_bar(60)

        if self.delay_time == 1000:
            # Subscribers and observers for the Information Frame
            self.initial_frame.set_progress_information("subscribers for the Information Frame")
            self.top_frame.information_frame.terminal_frame.subscribe(self.top_frame.elections_frame)
            self.top_frame.information_frame.terminal_frame.subscribe(self)
            self.initial_frame.set_progress_bar(70)

        if self.delay_time == 1200:
            # Subscribers and observers for the Elections Frame
            self.initial_frame.set_progress_information("subscribers for the Elections Frame")
            self.top_frame.elections_frame.subscribe(self.top_frame.evolution_frame)
            self.top_frame.elections_frame.subscribe(self.top_frame.information_frame)
            self.top_frame.elections_frame.subscribe(self.top_frame.environment_frame)
            self.initial_frame.set_progress_bar(80)

        if self.delay_time == 1400:
            # Subscribers and observers for the Evolution Frame
            self.initial_frame.set_progress_information("subscribers for the Evolution Frame")
            self.top_frame.evolution_frame.subscribe(self.top_frame.information_frame)
            self.top_frame.evolution_frame.subscribe(self.top_frame.elections_frame)
            self.top_frame.evolution_frame.subscribe(self)
            self.initial_frame.set_progress_bar(90)

        if self.delay_time == 1600:
            # Subscribers and observers for the Environment Frame
            self.initial_frame.set_progress_information("subscribers for the Environment Frame")
            self.top_frame.environment_frame.subscribe(self.top_frame.elections_frame)
            self.top_frame.environment_frame.subscribe(self.top_frame.evolution_frame)
            self.top_frame.environment_frame.subscribe(self.top_frame.information_frame)
            self.top_frame.environment_frame.subscribe(self.root_menu_bar)
            self.initial_frame.set_progress_bar(100)
            self.initial_frame.show_click_message()
            self.delay_time = 0
            return

        self.after(200, self.load_main_widgets)

    def load_main_app(self):
        """This method packs all the widgets of the application"""

        self.initial_frame.pack_forget()

        # Set the menu bar
        self.config(menu=self.root_menu_bar, bg="gray8")

        # Pack the top frame of the application
        self.top_frame.pack(fill=BOTH)

        # Pack the bottom frame of the application
        self.bottom_frame.pack(fill=BOTH, padx=3, ipady=3)

    def update(self, *args) -> None:
        """Receive the update from the publisher"""

        if args[0] == "exit":
            self.destroy()
        elif args[0] == "load_app":
            self.load_main_app()
        elif args[0] == "finish_application":
            self.destroy()

    def exit(self):
        """This method will be called whenever the application is exit"""
        
        if self.top_frame.evolution_frame.algorithm_running_status: self.top_frame.evolution_frame.stop_algorithm_execution = True
        else: self.destroy()