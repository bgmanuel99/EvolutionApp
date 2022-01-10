from tkinter import *

class TerminalFrame(Frame):

    def __init__(self, root):
        Frame.__init__(self, root, width=900, height=180)
        self.config(background="gray8")
        self.propagate(False)

        self.terminal_scrollbar = Scrollbar(self)
        self.terminal_scrollbar.pack(side=RIGHT, fill=Y)

        self.terminal = Text(self)
        self.terminal.pack(fill=BOTH, padx=6)
        self.terminal.config(
            font=("Terminal", 11), 
            wrap=WORD, 
            background="gray8", 
            relief=FLAT, 
            foreground="dark turquoise", 
            yscrollcommand=self.terminal_scrollbar.set
        )
        self.terminal_scrollbar.config(command=self.terminal.yview)
        self.write_to_terminal("Evolution App", "gray70", True, True)

    def write_to_terminal(self, message, color, nextLine=False, newCommand=False):
        if color not in self.terminal.tag_names(): self.terminal.tag_configure(color, foreground=color)

        self.terminal.insert("end", "{}{}{}".format("> " if newCommand else "", message, "\n" if nextLine else ""), color)