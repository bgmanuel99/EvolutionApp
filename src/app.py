from tkinter import *
from frame.topFrame import TopFrame
from frame.bottomFrame import BottomFrame
from menu.rootMenu import RootMenuBar

class Application(Tk):

    def __init__(self):
        super().__init__()
        self.title("Evolution")
        self.iconbitmap("../Images/Icon/Evolucion.ico")
        self.config(bg="gray60")
        self.root_menu_bar = RootMenuBar(self)
        self.config(menu=self.root_menu_bar)

        self.top_frame = TopFrame(self)
        self.top_frame.pack(expand=True, fill=BOTH)

        self.bottom_frame = BottomFrame(self)
        self.top_frame.pack(expand=True, fill=BOTH)