from tkinter import *

class ErrorsFrame(Frame):

    """This is the errors terminal from which the user will see all the errors happening in the application while running"""

    def __init__(self, root):
        Frame.__init__(self, root, width=900, height=180)
        self.config(background="gray8")
        self.propagate(False)

        self.errors_terminal_scrollbar = Scrollbar(self)
        self.errors_terminal_scrollbar.pack(side=RIGHT, fill=Y)

        self.errors_terminal = Text(self)
        self.errors_terminal.pack(fill=BOTH, padx=6)
        self.errors_terminal.config(
            font=("Terminal", 11), 
            wrap=WORD, 
            background="gray8", 
            relief=FLAT, 
            yscrollcommand=self.errors_terminal_scrollbar.set
        )
        self.errors_terminal_scrollbar.config(command=self.errors_terminal.yview)
        self.write_message("Evolution App", "gray70", True)
        self.errors_terminal.config(state="disabled")

        self.tag_configure("gold")
        self.tag_configure("red")
        self.tag_configure("OliveDrab1")

    def new_line(self):
        """Inserts a new line in the terminal"""

        self.errors_terminal.insert("end", "\n")

    def write_message(self, message, color, new_line=False):
        """Inserts a new message in the terminal"""

        if color not in self.errors_terminal.tag_names(): self.tag_configure(color)

        self.errors_terminal.insert("end", "{}{}".format(message, "\n" if new_line else ""), color)

    def tag_configure(self, color):
        """Inserts a new color into de configuration of the terminal so it can be used as a tag"""
        
        self.errors_terminal.tag_configure(color, foreground=color)

    def write_info(self, message="", before_breaks=0, after_breaks=0):
        """This method inserts a new info message to the errors terminal"""

        self.errors_terminal.config(state="normal")

        for _ in range(before_breaks):
            self.new_line()

        self.errors_terminal.insert("end", "[INFO] ", "OliveDrab1")
        self.errors_terminal.insert("end", message, "gray70")

        for _ in range(after_breaks):
            self.new_line()

        # Move the view of the terminal to the bottom each time something new is write in it
        self.errors_terminal.yview_moveto("1.0")

        self.errors_terminal.config(state="disabled")

    def write_warning(self, message="", before_breaks=0, after_breaks=0):
        """This method inserts a new warning message to the errors terminal"""

        self.errors_terminal.config(state="normal")

        for _ in range(before_breaks):
            self.new_line()

        self.errors_terminal.insert("end", "[WARNING] ", "gold")
        self.errors_terminal.insert("end", message, "gray70")

        for _ in range(after_breaks):
            self.new_line()

        # Move the view of the terminal to the bottom each time something new is write in it
        self.errors_terminal.yview_moveto("1.0")

        self.errors_terminal.config(state="disabled")

    def write_error(self, message="", before_breaks=0, after_breaks=0):
        """This method inserts a new error message to the errors terminal"""

        self.errors_terminal.config(state="normal")

        for _ in range(before_breaks):
            self.new_line()

        self.errors_terminal.insert("end", "[ERROR] ", "red")
        self.errors_terminal.insert("end", message, "gray70")

        for _ in range(after_breaks):
            self.new_line()

        # Move the view of the terminal to the bottom each time something new is write in it
        self.errors_terminal.yview_moveto("1.0")

        self.errors_terminal.config(state="disabled")