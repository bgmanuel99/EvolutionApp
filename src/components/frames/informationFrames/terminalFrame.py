import os
import csv
from tkinter import *
from components.interfaces.observer import Observer
from components.interfaces.publisher import Publisher
from typing import List

class TerminalFrame(Frame, Publisher):

    """
    This is the command terminal, from which the user will introduce commands to be executed in the application.
    It is also an Observer for some classes, like the root menu, to know it's state and changes.
    """

    def __init__(self, root):
        Frame.__init__(self, root, width=900, height=180)
        self.config(background="gray8")
        self.propagate(False)

        self._observers: List[Observer] = []

        self.terminal_scrollbar = Scrollbar(self)
        self.terminal_scrollbar.pack(side=RIGHT, fill=Y)

        self.terminal = Text(self)
        self.terminal.pack(fill=BOTH, padx=6)
        self.terminal.config(
            font=("Terminal", 11), 
            wrap=WORD, 
            background="gray8", 
            foreground="springgreen", 
            insertbackground="gray70", 
            relief=FLAT, 
            yscrollcommand=self.terminal_scrollbar.set
        )
        self.terminal_scrollbar.config(command=self.terminal.yview)
        self.terminal.bind("<Return>", self.proccess_command)
        self.terminal.bind("<Button-1>", lambda event: self.terminal.config(state="normal"))
        self.init_terminal()
        self.terminal.config(state="disabled")

        self.evolution_command = ""

    def subscribe(self, observer: Observer) -> None:
        """Subscribes an observer to the publisher"""

        self._observers.append(observer)

    def unsubscribe(self, observer: Observer) -> None:
        """Unsubscribes an observer from the publisher"""

        self._observers.remove(observer)

    def notify(self) -> None:
        """Notify all observer about an event"""
        
        for observers in self._observers:
            observers.update(self.evolution_command)

    def write_command(self):
        """Inserts a new line for the user to introduce the next command"""

        self.terminal.insert("end", "T > ", "gray70")

    def proccess_command(self, event):
        """Process the commands introduced by a user from the terminal"""

        command = self.terminal.get("end-1c linestart", "end-1c").split(" ")
        
        if len(command) < 3:
            self.new_line()
            self.write_message("Unknown command, use help to see the possible commands", "red", True)
            self.write_command()
            self.terminal.config(state="disabled")
            return
        
        command = command[2]

        self.new_line()

        if command.lower() == "run":
            self.evolution_command = "run"
            self.write_command()
            self.notify()
        elif command.lower() == "stop":
            self.evolution_command = "stop"
            self.write_command()
            self.notify()
        elif command.lower() == "continue":
            self.evolution_command = "continue"
            self.write_command()
            self.notify()
        elif command.lower() == "restart":
            self.evolution_command = "restart"
            self.write_command()
            self.notify()
        elif command.lower() == "help":
            self.new_line()
            
            with open(os.getcwd().replace("\\", "/") + "/archive/commandDescriptions.csv", newline="\n") as csvFile:
                reader = csv.reader(csvFile, delimiter=",")

                for command, description in reader:
                    self.write_message(command + "  ", color="springgreen")
                    self.write_message(description, new_line=True)

            self.new_line()
            self.write_command()
        elif command.lower() == "clear":
            self.clear_terminal()
        elif command.lower() == "exit":
            self.evolution_command = "exit"
            self.write_command()
            self.notify()
            return
        else:
            self.write_message("Unknown command, use help to see the possible commands", "red", True)
            self.write_command()

        # The reason to finally disable the terminal is for the return key not to insert a break in the text
        # The break lines will be managed with the write_message and new_line functions
        self.terminal.config(state="disabled")

    def new_line(self):
        """Inserts a new line in the terminal"""

        self.terminal.insert("end", "\n")

    def write_message(self, message, color="gray70", new_line=False):
        """Inserts a new message in the terminal"""

        if color not in self.terminal.tag_names(): self.tag_configure(color)

        self.terminal.insert("end", "{}{}".format(message, "\n" if new_line else ""), color)

    def tag_configure(self, color):
        """Inserts a new color into de configuration of the terminal so it can be used as a tag"""

        self.terminal.tag_configure(color, foreground=color)

    def init_terminal(self):
        """Initialize the command terminal"""

        self.write_message("Evolution App\n", "gray70", True)
        self.write_message("You can type help to see different commands to use in the terminal\n", "gray70", True)
        self.write_command()

    def clear_terminal(self):
        """Clears the actual terminal"""

        self.terminal.config(state="normal")
        self.terminal.delete("1.0", END)
        self.init_terminal()
        self.terminal.config(state="disabled")

    def copy_text(self):
        """Copy the selected text from the terminal"""

        self.clipboard_clear()
        self.terminal.clipboard_append(self.terminal.selection_get())

    def paste_text(self):
        """Paste text to the terminal"""

        self.terminal.insert("end", self.clipboard_get())

    def process_message(self, message="", color="gray70", before_lines=0, after_lines=0, new_command=False):
        """This method receives incoming messages from other panels in the application and show them in the terminal"""

        self.terminal.config(state="normal")
        
        for _ in range(before_lines):
            self.new_line()

        self.write_message(message, color)

        for _ in range(after_lines):
            self.new_line()

        if new_command: self.write_command()
        
        self.terminal.config(state="disabled")