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
        self.terminal.bind("<Button-1>", self.process_pressed_terminal)
        self.init_terminal()
        self.terminal.config(state="disabled")

        self.evolution_command = ""
        self.modifiable_terminal = True

        # Variable to set a default path for the evolution report log
        self.default_path = ""

    def subscribe(self, observer: Observer) -> None:
        """Subscribes an observer to the publisher"""

        self._observers.append(observer)

    def unsubscribe(self, observer: Observer) -> None:
        """Unsubscribes an observer from the publisher"""

        self._observers.remove(observer)

    def notify(self) -> None:
        """Notify all observer about an event"""
        
        if self.evolution_command == "set_default_path":
            for observers in self._observers:
                observers.update(self.evolution_command, self.default_path)
        else:
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
        
        type_of_command = command[2]

        if type_of_command.lower() == "run":
            self.evolution_command = "run"
            self.notify()
        elif type_of_command.lower() == "help":
            self.new_line()
            self.new_line()
            
            with open(os.getcwd().replace("\\", "/") + "/archive/commandDescriptions.csv", newline="\n") as csvFile:
                reader = csv.reader(csvFile, delimiter=",")

                for command, description in reader:
                    self.write_message(command + "  ", color="springgreen")
                    self.write_message(description, new_line=True)

            self.new_line()
            self.write_command()
        elif type_of_command.lower() == "clear":
            self.clear_terminal()
        elif type_of_command.lower() == "exit":
            self.evolution_command = "exit"
            self.notify()
            return
        elif type_of_command.lower() == "set":
            if len(command) < 4:
                self.new_line()
                self.new_line()
                self.write_message("You have to insert a path to set the default report log", "red", True)
                self.new_line()
                self.write_command()
            else:
                final_path = command[3].replace('"', "") + " "
                
                # If the lenght of the command list is more than 4 it means the user introduced a path with spaces
                if len(command) > 4:
                    for index in range(4, len(command)):
                        final_path += command[index].replace('"', "") + " "

                # Get out of the final path the last space
                final_path = final_path[:-1]

                if not os.path.exists(final_path):
                    self.new_line()
                    self.new_line()
                    self.write_message("The path does'nt exists, insert a correct path", "red", True)
                    self.new_line()
                    self.write_command()
                elif not os.path.isfile(final_path):
                    self.new_line()
                    self.new_line()
                    self.write_message("The path needs to end at a txt file --> path_to_file/*.txt, where * means any name for the file", "red", True)
                    self.new_line()
                    self.write_command()
                elif not final_path.lower().endswith(".txt"):
                    self.new_line()
                    self.new_line()
                    self.write_message("The provided file should have a txt extension --> *.txt", "red", True)
                    self.new_line()
                    self.write_command()
                else:
                    self.new_line()
                    self.new_line()
                    self.write_message("Setting the default path to --> ")
                    self.write_message(final_path, "OliveDrab1", True)
                    self.new_line()
                    self.write_command()
                    self.default_path = final_path
                    self.evolution_command = "set_default_path"
                    self.notify()
        elif type_of_command.lower() == "unset":
            self.new_line()
            self.new_line()
            self.write_message("Unsetting the stored default path", "gray70", True)
            self.new_line()
            self.write_command()
            self.evolution_command = "unset_default_path"
            self.notify()
        else:
            self.new_line()
            self.write_message("Unknown command, use help to see the possible commands", "red", True)
            self.new_line()
            self.write_command()

        # The reason to finally disable the terminal is for the return key not to insert a break in the text
        # The break lines will be managed with the write_message and new_line functions
        self.terminal.config(state="disabled")

    def process_pressed_terminal(self, event):
        """Process whenever the terminal is clicked with the left button of the mouse"""

        if self.modifiable_terminal: self.terminal.config(state="normal")

    def new_line(self):
        """Inserts a new line in the terminal"""

        self.terminal.insert("end", "\n")

    def write_message(self, message, color="gray70", new_line=False):
        """Inserts a new message in the terminal"""

        if color not in self.terminal.tag_names(): self.tag_configure(color)

        self.terminal.insert("end", "{}{}".format(message, "\n" if new_line else ""), color)

        # Move the view of the terminal to the bottom each time something new is write in it
        self.terminal.yview_moveto("1.0")

    def tag_configure(self, color):
        """Inserts a new color into de configuration of the terminal so it can be used as a tag"""

        self.terminal.tag_configure(color, foreground=color)

    def init_terminal(self):
        """Initialize the command terminal"""

        self.write_message("Evolution App\n", "gray70", True)
        self.write_message("You can type help to see the available commands to use in the terminal\n", "gray70", True)
        self.write_command()

    def clear_terminal(self):
        """Clears the actual terminal"""

        if self.modifiable_terminal:
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

    def switch_terminal_status(self, status):
        """Sets the status for the terminal in order for it to be modifiable or not"""

        self.modifiable_terminal = status