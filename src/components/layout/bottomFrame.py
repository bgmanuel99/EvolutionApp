from tkinter import *
from datetime import datetime

class BottomFrame(Frame):

    """The bottom frame is only a display frame, where the name, version and clock of the application are shown"""

    def __init__(self, root):
        Frame.__init__(self, root)
        self.config(background="gray8")

        # Name and version Label
        self.name_version_label = Label(self, text="Evolution")
        self.name_version_label.pack(side=LEFT, anchor=SW, fill=Y)
        self.name_version_label.config(font=("Terminal"), background="gray8", foreground="springgreen")

        # App's clock
        self.time_text = StringVar()
        self.time_text.set(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        self.time_label = Label(self, text=self.time_text)
        self.time_label.pack(side=RIGHT, anchor=SE, fill=Y)
        self.time_label.config(textvariable=self.time_text, font=("Terminal"), background="gray8", foreground="springgreen")
        self.get_time()

    def get_time(self):
        """Update the date/time of the clock in the app"""

        self.time_text.set(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        self.time_label.after(1000, self.get_time)