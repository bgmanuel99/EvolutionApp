from tkinter import *
from Frame.mainFrame import MainFrame
from Frame.bottomFrame import BottomFrame
from Menu.rootMenu import RootMenuBar

if __name__ == "__main__":
    root = Tk()
    root.title("Evolution")
    root.iconbitmap("../Images/Icon/Evolucion.ico")
    root.resizable(0, 0)

    MainFrame(root)
    BottomFrame(root)

    root.config(menu=RootMenuBar(root))

    root.mainloop()