from tkinter import *
from components.layout.informationFrames.characteristicsFrame import CharacteristicsFrame
from components.layout.informationFrames.errorsFrame import ErrorsFrame
from components.layout.informationFrames.terminalFrame import TerminalFrame
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

        self.gradient = GradientFrame(self, "OliveDrab1", "SpringGreen4")
        self.gradient.pack()
        self.gradient.config(bd=0, highlightthickness=0, relief='ridge')

        # Main frame for the three terminal election buttons from which we choose the terminal to use
        self.panel_of_elections = Frame(self.gradient)
        self.panel_of_elections.pack(fill=BOTH, side=TOP, anchor=W, padx=2, pady=(2, 0))
        self.panel_of_elections.config(background="gray8")

        # Election button for the commands terminal, made from a frame and a label
        self.terminal_election_frame = Frame(self.panel_of_elections)
        self.terminal_election_frame.pack(side=LEFT, anchor=W, padx=(6, 2), pady=(4, 6))
        self.terminal_election_label = Label(self.terminal_election_frame, text="TERMINAL")
        self.terminal_election_label.pack(side=TOP)
        self.terminal_election_label.config(background="gray8", foreground="gray70", font=("Terminal", 11))
        self.terminal_election_focus = Frame(self.terminal_election_frame, height=2)
        self.terminal_election_focus.pack(fill=BOTH)
        self.terminal_election_focus.config(background="gray70")
        self.terminal_election_label.bind("<Button-1>", self.focus_terminal)
        self.terminal_election_label.bind("<Enter>", lambda event: self.terminal_election_label.config(cursor="hand2"))

        self.terminal_election_lateral_label = Label(self.panel_of_elections, width=3)
        self.terminal_election_lateral_label.pack(side=LEFT, anchor=W)
        self.terminal_election_lateral_label.config(background="gray8", foreground="gray70", font=("Terminal", 11))

        # Election button for the problems terminal, made from a frame and a label
        self.errors_election_frame = Frame(self.panel_of_elections)
        self.errors_election_frame.pack(side=LEFT, anchor=W, padx=(6, 2), pady=(4, 6))
        self.errors_election_label = Label(self.errors_election_frame, text="ERRORS")
        self.errors_election_label.pack(side=TOP)
        self.errors_election_label.config(background="gray8", foreground="gray50", font=("Terminal", 11))
        self.errors_election_focus = Frame(self.errors_election_frame, height=2)
        self.errors_election_focus.pack(fill=BOTH)
        self.errors_election_focus.config(background="gray8")
        self.errors_election_label.bind("<Button-1>", self.focus_errors)
        self.errors_election_label.bind("<Enter>", lambda event: self.errors_election_label.config(cursor="hand2"))

        self.errors_election_lateral_label_variable = StringVar()
        self.errors_election_lateral_label_variable.set("")
        self.errors_election_lateral_label = Label(self.panel_of_elections, textvariable=self.errors_election_lateral_label_variable, width=3)
        self.errors_election_lateral_label.pack(side=LEFT, anchor=W)
        self.errors_election_lateral_label.config(background="gray8", foreground="white", font=("Terminal", 11))

        # Election button for the characteristics terminal, made from a frame and a label
        self.characteristics_election_frame = Frame(self.panel_of_elections)
        self.characteristics_election_frame.pack(side=LEFT, anchor=W, padx=(6, 2), pady=(4, 6))
        self.characteristics_election_label = Label(self.characteristics_election_frame, text="CHARACTERISTICS")
        self.characteristics_election_label.pack(side=TOP)
        self.characteristics_election_label.config(background="gray8", foreground="gray50", font=("Terminal", 11))
        self.characteristics_election_focus = Frame(self.characteristics_election_frame, height=2)
        self.characteristics_election_focus.pack(fill=BOTH)
        self.characteristics_election_focus.config(background="gray8")
        self.characteristics_election_label.bind("<Button-1>", self.focus_characteristics)
        self.characteristics_election_label.bind("<Enter>", lambda event: self.characteristics_election_label.config(cursor="hand2"))

        self.characteristics_election_lateral_label = Label(self.panel_of_elections, width=3)
        self.characteristics_election_lateral_label.pack(side=LEFT, anchor=W)
        self.characteristics_election_lateral_label.config(background="gray8", foreground="gray70", font=("Terminal", 11))

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
            "message": self.terminal_frame.process_message,
            "error": self.errors_frame.write_error,
            "warning": self.errors_frame.write_warning,
            "terminal_status": self.terminal_frame.switch_terminal_status,
            "update_characteristics_data": self.characteristics_frame.update_data,
            "update_time": self.characteristics_frame.update_algorithm_time_of_execution,
            "update_epoch_time": self.characteristics_frame.update_epoch_time_of_execution,
            "execution_failed": self.terminal_frame.write_command,
        }

        self.errors_counter = 0
        self.warnings_counter = 0

    def update(self, *args) -> None:
        """Receive the update from the publisher"""

        if args[0] in ["clear", "copy", "paste"]: self.terminal_methods[args[0]]()
        elif args[0] == "message": self.terminal_methods[args[0]](args[1], args[2][0], args[2][1], args[2][2], args[2][3])
        elif args[0] == "error" or args[0] == "warning":
            self.terminal_methods[args[0]](args[1], args[2][0], args[2][1])

            if self.actual_focus_frame != "errors":
                if args[0] == "warning": self.warnings_counter += 1
                elif args[0] == "error": self.errors_counter += 1

                if self.warnings_counter >= 1 and self.errors_counter == 0:
                    self.errors_election_lateral_label.config(background="gold")
                elif self.errors_counter >= 1:
                    self.errors_election_lateral_label.config(background="red")

                actual_number_of_errors = self.errors_election_lateral_label_variable.get()
                if actual_number_of_errors == "": self.errors_election_lateral_label_variable.set("1")
                elif (self.warnings_counter + self.errors_counter) >= 99: self.errors_election_lateral_label_variable.set("+99")
                else: self.errors_election_lateral_label_variable.set(self.warnings_counter + self.errors_counter)
        elif args[0] == "terminal_status": self.terminal_methods[args[0]](args[1])
        elif args[0] == "update_characteristics_data": self.terminal_methods[args[0]](args[1])
        elif args[0] == "change_environment":
            if args[1] == "polar":
                self.gradient.set_new_colors("RoyalBlue2", "magenta4")
                self.terminal_frame.process_message("ACTIVE ENVIRONMENT --> ", "gray70", 2, 0, False)
                self.terminal_frame.process_message("POLAR", "OliveDrab1", 0, 2, True)
            elif args[1] == "mediterranean":
                self.gradient.set_new_colors("OliveDrab1", "SpringGreen4")
                self.terminal_frame.process_message("ACTIVE ENVIRONMENT --> ", "gray70", 2, 0, False)
                self.terminal_frame.process_message("MEDITERRANEAN", "OliveDrab1", 0, 2, True)
            elif args[1] == "desert":
                self.gradient.set_new_colors("goldenrod1", "brown")
                self.terminal_frame.process_message("ACTIVE ENVIRONMENT --> ", "gray70", 2, 0, False)
                self.terminal_frame.process_message("DESERT", "OliveDrab1", 0, 2, True)
        elif args[0] == "update_time": self.terminal_methods[args[0]](args[1], args[2])
        elif args[0] == "update_epoch_time": self.terminal_methods[args[0]](args[1], args[2])
        elif args[0] == "execution_failed": self.terminal_methods[args[0]]()

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

            self.errors_election_lateral_label.config(background="gray8")
            self.errors_election_lateral_label_variable.set("")
            self.warnings_counter = 0
            self.errors_counter = 0

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