from tkinter import *
from frames.informationFrames.characteristicsFrame import CharacteristicsFrame
from frames.informationFrames.problemsFrame import ProblemsFrame
from frames.informationFrames.terminalFrame import TerminalFrame

class InformationFrame(Frame):

    def __init__(self, root):
        Frame.__init__(self, root)
        self.config(bg="dark turquoise")

        self.panel_of_elections = Frame(self, width=900, height=20)
        self.panel_of_elections.pack(fill=BOTH, side=TOP, anchor=W, padx=2, pady=(2, 0))
        self.panel_of_elections.config(background="gray8")

        self.terminal_election_frame = Frame(self.panel_of_elections, width=40, height=20)
        self.terminal_election_frame.pack(side=LEFT, anchor=W, padx=(6, 5), pady=(4, 8))
        self.terminal_election_label = Label(self.terminal_election_frame, text="TERMINAL")
        self.terminal_election_label.pack()
        self.terminal_election_label.config(background="gray8", foreground="gray70", font=("Terminal", 11))

        self.problems_election_frame = Frame(self.panel_of_elections, width=40, height=20)
        self.problems_election_frame.pack(side=LEFT, anchor=W, padx=(1, 5), pady=(4, 8))
        self.problems_election_label = Label(self.problems_election_frame, text="PROBLEMS")
        self.problems_election_label.pack()
        self.problems_election_label.config(background="gray8", foreground="gray50", font=("Terminal", 11))

        self.characteristics_election_frame = Frame(self.panel_of_elections, width=40, height=20)
        self.characteristics_election_frame.pack(side=LEFT, anchor=W, padx=(1, 6), pady=(4, 8))
        self.characteristics_election_label = Label(self.characteristics_election_frame, text="CHARACTERISTICS")
        self.characteristics_election_label.pack()
        self.characteristics_election_label.config(background="gray8", foreground="gray50", font=("Terminal", 11))

        self.terminal_frame = TerminalFrame(self)
        self.problems_frame = ProblemsFrame(self)
        self.characteristics_frame = CharacteristicsFrame(self)
        self.main_frame = self.terminal_frame
        self.main_frame.pack(padx=2, pady=(0, 2))