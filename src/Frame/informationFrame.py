from tkinter import *
from frame.characteristicsFrame import CharacteristicsFrame

class InformationFrame(Frame):

    def __init__(self, root):
        Frame.__init__(self, root, width=980, height=200)
        self.config(bg="gray40")

        self.characteristicsFrame = CharacteristicsFrame(self)
        self.characteristicsFrame.pack(side=LEFT, anchor=W, padx=(2, 0))

        self.terminal_frame = Frame(self, width=500, height=200)
        self.terminal_frame.pack(padx=2, pady=2)
        self.terminal_frame.propagate(False)

        self.terminal_scrollbar = Scrollbar(self.terminal_frame)
        self.terminal_scrollbar.pack(side=RIGHT, fill=Y)

        self.terminal = Text(self.terminal_frame)
        self.terminal.pack()
        self.terminal.config(
            font=("Terminal", 12), 
            wrap=WORD, 
            background="gray8", 
            relief=FLAT, 
            foreground="dark turquoise", 
            yscrollcommand=self.terminal_scrollbar.set
        )
        self.terminal_scrollbar.config(command=self.terminal.yview)

    def write_to_terminal(self, message, color, nextLine):
        if color not in self.terminal.tag_names(): self.terminal.tag_configure(color, foreground=color)

        self.terminal.insert("end", "> {}{}".format(message, "\n" if nextLine else ""), color)