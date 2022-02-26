import os
from tkinter import *
from components.frames.topFrame import TopFrame
from components.frames.bottomFrame import BottomFrame
from components.menu.rootMenu import RootMenuBar
from components.interfaces.observer import Observer
from components.interfaces.publisher import Publisher

class Application(Tk, Observer):

    """Main winfow of the application. It inherits from TK which is the root object of tkinter module to create the GUI"""

    def __init__(self):
        super().__init__()
        self.title("Evolution")
        self.iconbitmap(os.getcwd().replace("\\", "/") + "/assets/icon/evolution.ico")
        self.resizable(0, 0)

        # Main menu bar for the main window
        self.root_menu_bar = RootMenuBar(self)
        self.config(menu=self.root_menu_bar, bg="gray8")

        # Top frame of the main window
        self.top_frame = TopFrame(self)
        self.top_frame.pack(fill=BOTH)

        # Bottom frame of the main window
        self.bottom_frame = BottomFrame(self)
        self.bottom_frame.pack(fill=BOTH, padx=3, ipady=3)

        self.root_menu_bar.subscribe(self.top_frame.information_frame)
        self.root_menu_bar.subscribe(self.top_frame.elections_frame)
        self.top_frame.information_frame.terminal_frame.subscribe(self.top_frame.elections_frame)
        self.top_frame.information_frame.terminal_frame.subscribe(self)
        self.top_frame.elections_frame.subscribe(self.top_frame.evolution_frame)
        self.top_frame.elections_frame.subscribe(self.top_frame.information_frame.errors_frame)

    def update(self, Publisher: Publisher, *args) -> None:
        """Receive the update from the publisher"""

        if args[0] == "exit":
            self.destroy()