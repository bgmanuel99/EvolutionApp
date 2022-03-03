from tkinter import *
from components.interfaces.observer import Observer
from components.interfaces.publisher import Publisher
from typing import List

class RootMenuBar(Menu, Publisher):

    """
    This is the root (main) menu bar of the application.
    It is also a publisher so it can notify its state and changes to other observers like the command terminal.
    """

    def __init__(self, root: Tk):
        Menu.__init__(self, root)

        self._observers: List[Observer] = []
        self.pressed_command = ""

        self.file_menu = Menu(self, tearoff=0)
        self.file_menu.add_command(label="Open", command=None)
        self.file_menu.add_command(label="Save", command=None)
        self.file_menu.add_command(label="Save as...", command=None)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=root.destroy)

        self.edit_menu = Menu(self, tearoff=0)
        self.edit_menu.add_command(label="Copy", command=lambda: self.pre_notify("copy"))
        self.edit_menu.add_command(label="Paste", command=lambda: self.pre_notify("paste"))

        self.run_menu = Menu(self, tearoff=0)
        self.run_menu.add_command(label="Run", command=lambda: self.pre_notify("run"))
        self.run_menu.add_command(label="Stop", command=lambda: self.pre_notify("stop"))
        self.run_menu.add_command(label="Continue", command=lambda: self.pre_notify("continue"))
        self.run_menu.add_command(label="Restart", command=lambda: self.pre_notify("restart"))

        self.terminal_menu = Menu(self, tearoff=0)
        self.terminal_menu.add_command(label="Clear terminal", command=lambda: self.pre_notify("clear"))

        self.help_menu = Menu(self, tearoff=0)
        self.help_menu.add_command(label="Help", command=None)
        self.help_menu.add_separator()
        self.help_menu.add_command(label="About...", command=None)

        self.add_cascade(label="File", menu=self.file_menu)
        self.add_cascade(label="Edit", menu=self.edit_menu)
        self.add_cascade(label="Run", menu=self.run_menu)
        self.add_cascade(label="Terminal", menu=self.terminal_menu)
        self.add_cascade(label="Help", menu=self.help_menu)

    def subscribe(self, observer: Observer) -> None:
        """Subscribes an observer to the publisher"""

        self._observers.append(observer)

    def unsubscribe(self, observer: Observer) -> None:
        """Unsubscribes an observer from the publisher"""

        self._observers.remove(observer)

    def pre_notify(self, command):
        """
        This method is called before the notify method of the publisher to change an internal variable 
        and so the observers can now the state of the menu
        """
        
        self.pressed_command = command
        self.notify()

    def notify(self) -> None:
        """Notify all observer about an event"""

        for observers in self._observers:
            observers.update(self, self.pressed_command)