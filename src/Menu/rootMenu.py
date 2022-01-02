from tkinter import Menu

# This class contains the main tool bar of the app
class RootMenuBar(Menu):

    def __init__(self, root):
        Menu.__init__(self, root)

        self.file_menu = Menu(self, tearoff=0)
        self.edit_menu = Menu(self, tearoff=0)
        self.run_menu = Menu(self, tearoff=0)
        self.terminal_menu = Menu(self, tearoff=0)
        self.help_menu = Menu(self, tearoff=0)

        self.add_cascade(label="File", menu=self.file_menu)
        self.add_cascade(label="Edit", menu=self.edit_menu)
        self.add_cascade(label="Run", menu=self.run_menu)
        self.add_cascade(label="Terminal", menu=self.terminal_menu)
        self.add_cascade(label="Help", menu=self.help_menu)