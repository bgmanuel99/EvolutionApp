from tkinter import *
from components.frames.informationFrames.characteristicsFrame import CharacteristicsFrame
from components.frames.informationFrames.errorsFrame import ErrorsFrame
from components.frames.informationFrames.terminalFrame import TerminalFrame
from components.menu.rootMenu import RootMenuBar
from components.models.gradients import GradientFrame
from components.interfaces.observer import Observer

class InformationFrame(Frame, Observer):

    """
    The information frame contains three different terminal. The command, the problems and the characteristics terminals.
    In the command terminal the user will introduce comands to execute different logics of the application.
    In the errors terminal will be shown all the errors during the execution of the main algorithm, or any other errors concerning to the app.
    In the characteristics terminal will be displayed the different species with its real-time characteristics during the execution of the main algorithm
    """

    def __init__(self, root):
        Frame.__init__(self, root)
        self.config(bg="dark turquoise")

        self.gradient = GradientFrame(self, "RoyalBlue2", "magenta4")
        self.gradient.pack()
        self.gradient.config(bd=0, highlightthickness=0, relief='ridge')

        # Main frame for the three terminal election buttons from which we choose the terminal to use
        self.panel_of_elections = Frame(self.gradient)
        self.panel_of_elections.pack(fill=BOTH, side=TOP, anchor=W, padx=2, pady=(2, 0))
        self.panel_of_elections.config(background="gray8")

        # Election button for the commands terminal, made from a frame and a label
        self.terminal_election_frame = Frame(self.panel_of_elections)
        self.terminal_election_frame.pack(side=LEFT, anchor=W, padx=(6, 5), pady=(4, 6))
        self.terminal_election_label = Label(self.terminal_election_frame, text="TERMINAL")
        self.terminal_election_label.pack(side=TOP)
        self.terminal_election_label.config(background="gray8", foreground="gray70", font=("Terminal", 11))
        self.terminal_election_focus = Frame(self.terminal_election_frame, height=2)
        self.terminal_election_focus.pack(fill=BOTH)
        self.terminal_election_focus.config(background="gray70")
        self.terminal_election_label.bind("<Button-1>", self.focus_terminal)
        self.terminal_election_label.bind("<Enter>", lambda event: self.terminal_election_label.config(cursor="hand2"))

        # Election button for the problems terminal, made from a frame and a label
        self.errors_election_frame = Frame(self.panel_of_elections)
        self.errors_election_frame.pack(side=LEFT, anchor=W, padx=(1, 5), pady=(4, 6))
        self.errors_election_label = Label(self.errors_election_frame, text="ERRORS")
        self.errors_election_label.pack(side=TOP)
        self.errors_election_label.config(background="gray8", foreground="gray50", font=("Terminal", 11))
        self.errors_election_focus = Frame(self.errors_election_frame, height=2)
        self.errors_election_focus.pack(fill=BOTH)
        self.errors_election_focus.config(background="gray8")
        self.errors_election_label.bind("<Button-1>", self.focus_errors)
        self.errors_election_label.bind("<Enter>", lambda event: self.errors_election_label.config(cursor="hand2"))

        # Election button for the characteristics terminal, made from a frame and a label
        self.characteristics_election_frame = Frame(self.panel_of_elections)
        self.characteristics_election_frame.pack(side=LEFT, anchor=W, padx=(1, 6), pady=(4, 6))
        self.characteristics_election_label = Label(self.characteristics_election_frame, text="CHARACTERISTICS")
        self.characteristics_election_label.pack()
        self.characteristics_election_label.config(background="gray8", foreground="gray50", font=("Terminal", 11))
        self.characteristics_election_focus = Frame(self.characteristics_election_frame, height=2)
        self.characteristics_election_focus.pack(fill=BOTH)
        self.characteristics_election_focus.config(background="gray8")
        self.characteristics_election_label.bind("<Button-1>", self.focus_characteristics)
        self.characteristics_election_label.bind("<Enter>", lambda event: self.characteristics_election_label.config(cursor="hand2"))

        # This are the objects which contains the three terminals. The main_frame contains the terminal to be actually displayed in the app.
        # The actual_focus_frame object is used so that if a terminal was already selected it doesnt change anything by pressing it another time.
        self.terminal_frame = TerminalFrame(self.gradient)
        self.errors_frame = ErrorsFrame(self.gradient)
        self.characteristics_frame = CharacteristicsFrame(self.gradient)
        self.main_frame = self.terminal_frame
        self.main_frame.pack(padx=2, pady=(0, 2))
        self.actual_focus_frame = "terminal"

        self.terminal_methods = {
            "clear": self.terminal_frame.clear_terminal, 
            "copy": self.terminal_frame.copy_text,
            "paste": self.terminal_frame.paste_text,
            "values": self.terminal_frame.process_message,
            "error": self.errors_frame.write_message,
            "warning": self.errors_frame.write_message
        }

    def update(self, publisher: RootMenuBar, *args) -> None:
        """Receive the update from the publisher"""

        if args[0] in ["clear", "copy", "paste"]:
            self.terminal_methods[args[0]]()
        elif args[0] == "values":
            self.terminal_methods[args[0]](args[1], "gray70", True)
        elif args[0] == "error":
            self.terminal_methods[args[0]](args[1], color="red", new_line=True)
        elif args[0] == "warning":
            self.terminal_methods[args[0]](args[1], color="yellow", new_line=True)

    def focus_terminal(self, event):
        """Change the focus of the information frame to the command terminal"""

        if self.actual_focus_frame == "terminal": return
        else:
            self.terminal_election_focus.config(background="gray70")
            self.terminal_election_label.config(foreground="gray70")
            self.errors_election_focus.config(background="gray8")
            self.errors_election_label.config(foreground="gray50")
            self.characteristics_election_focus.config(background="gray8")
            self.characteristics_election_label.config(foreground="gray50")

            self.main_frame.pack_forget()
            self.main_frame = self.terminal_frame
            self.main_frame.pack(padx=2, pady=(0, 2))
            self.actual_focus_frame = "terminal"

    def focus_errors(self, event):
        """Change the focus of the information frame to the errors terminal"""

        if self.actual_focus_frame == "errors": return
        else:
            self.errors_election_focus.config(background="gray70")
            self.errors_election_label.config(foreground="gray70")
            self.terminal_election_focus.config(background="gray8")
            self.terminal_election_label.config(foreground="gray50")
            self.characteristics_election_focus.config(background="gray8")
            self.characteristics_election_label.config(foreground="gray50")

            self.main_frame.pack_forget()
            self.main_frame = self.errors_frame
            self.main_frame.pack(padx=2, pady=(0, 2))
            self.actual_focus_frame = "errors"

    def focus_characteristics(self, event):
        """Change the focus of the information frame to the characteristics terminal"""

        if self.actual_focus_frame == "characteristics": return
        else:
            self.characteristics_election_focus.config(background="gray70")
            self.characteristics_election_label.config(foreground="gray70")
            self.terminal_election_focus.config(background="gray8")
            self.terminal_election_label.config(foreground="gray50")
            self.errors_election_focus.config(background="gray8")
            self.errors_election_label.config(foreground="gray50")

            self.main_frame.pack_forget()
            self.main_frame = self.characteristics_frame
            self.main_frame.pack(padx=2, pady=(0, 2))
            self.actual_focus_frame = "characteristics"