from tkinter import *
from tkinter import ttk
from frame.characteristicsFrame import CharacteristicsFrame

class InformationFrame(Frame):

    def __init__(self, root):
        Frame.__init__(self, root)
        self.config(bg="gray40")

        self.characteristicsFrame = CharacteristicsFrame(self)
        self.characteristicsFrame.pack(side=LEFT, anchor=W, padx=(2, 0))

        self.terminal_frame = Frame(self, width=500, height=200)
        self.terminal_frame.pack(padx=2, pady=2)
        self.terminal_frame.propagate(False)

        terminal_scrollbar_style = ttk.Style()
        terminal_scrollbar_style.theme_use("alt")
        terminal_scrollbar_style.element_create("Arrowless.Vertical.Scrollbar.trough", "from", "default")
        terminal_scrollbar_style.layout("Arrowless.Vertical.TScrollbar",
        [(
            "Arrowless.Vertical.Scrollbar.trough", 
            {
                "children": [
                    (
                        "Arrowless.Vertical.Scrollbar.thumb",
                        {
                            "sticky": "nswe"
                        }
                    )
                ],
                "sticky": "ns"
            }
        )])
        terminal_scrollbar_style.map("Arrowless.Vertical.TScrollbar",
            foreground=[("pressed", "gray55"), ("active", "gray55")],
            background=[("pressed", "gray55"), ("active", "gray55")]
        )
        terminal_scrollbar_style.configure(
            "Arrowless.Vertical.TScrollbar", 
            troughcolor="gray15", 
            background="gray55"
        )

        self.terminal_scrollbar = ttk.Scrollbar(self.terminal_frame, style="Arrowless.Vertical.TScrollbar")
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