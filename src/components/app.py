import os
from tkinter import *
from components.audio.soundEffects import SoundEffects
from components.layout.topFrame import TopFrame
from components.layout.bottomFrame import BottomFrame
from components.layout.rootMenu import RootMenuBar
from components.interfaces.observer import Observer

class Application(Tk, Observer):

    """Main winfow of the application. It inherits from TK which is the root object of tkinter module to create the GUI"""

    def __init__(self):
        super().__init__()
        self.title("Evolution")
        self.iconbitmap(os.getcwd().replace("\\", "/") + "/assets/icon/evolution.ico")
        self.resizable(0, 0)

        # Set the volume of the application to 100%
        SoundEffects.button_click.set_volume(1)
        SoundEffects.error_click.set_volume(1)
        SoundEffects.checkbutton_click.set_volume(1)

        # Main menu bar for the main window
        self.root_menu_bar = RootMenuBar(self)
        self.config(menu=self.root_menu_bar, bg="gray8")

        # Top frame of the main window
        self.top_frame = TopFrame(self)
        self.top_frame.pack(fill=BOTH)

        # Bottom frame of the main window
        self.bottom_frame = BottomFrame(self)
        self.bottom_frame.pack(fill=BOTH, padx=3, ipady=3)

        # Subscribers and observers
        self.root_menu_bar.subscribe(self.top_frame.information_frame)
        self.root_menu_bar.subscribe(self.top_frame.elections_frame)
        self.root_menu_bar.subscribe(self.top_frame.environment_frame)
        self.top_frame.information_frame.terminal_frame.subscribe(self.top_frame.elections_frame)
        self.top_frame.information_frame.terminal_frame.subscribe(self)
        self.top_frame.elections_frame.subscribe(self.top_frame.evolution_frame)
        self.top_frame.elections_frame.subscribe(self.top_frame.information_frame)
        self.top_frame.elections_frame.subscribe(self.top_frame.environment_frame)
        self.top_frame.evolution_frame.subscribe(self.top_frame.information_frame)
        self.top_frame.evolution_frame.subscribe(self.top_frame.elections_frame)
        self.top_frame.environment_frame.subscribe(self.top_frame.elections_frame)
        self.top_frame.environment_frame.subscribe(self.top_frame.evolution_frame)
        self.top_frame.environment_frame.subscribe(self.top_frame.information_frame)
        self.top_frame.environment_frame.subscribe(self.root_menu_bar)

    def update(self, *args) -> None:
        """Receive the update from the publisher"""

        if args[0] == "exit":
            self.destroy()