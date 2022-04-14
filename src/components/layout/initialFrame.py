from tkinter import *
from typing import List
from tkinter import font as TkFont
from tkinter.ttk import Progressbar
from components.models.gradients import GradientFrame
from components.interfaces.observer import Observer
from components.interfaces.publisher import Publisher

class InitialFrame(Frame, Observer, Publisher):

    """
    This frame will serve as an introduction for the application.
    After the user presses the frame, the application will load to be used
    """

    def __init__(self, root):

        Frame.__init__(self, root, width=1214, height=752)
        self.config(background="gray8")
        self.propagate(False)

        self._observers: List[Observer] = []

        top_border_gradient = GradientFrame(self, color1="purple", color2="dark turquoise")
        top_border_gradient.place(x=0, y=0, width=1214, height=251)
        top_border_gradient.config(bd=0, highlightthickness=0, relief='ridge')

        middle_border_gradient = GradientFrame(self, color1="SeaGreen1", color2="green yellow")
        middle_border_gradient.place(x=0, y=251, width=1214, height=250)
        middle_border_gradient.config(bd=0, highlightthickness=0, relief='ridge')

        bottom_border_gradient = GradientFrame(self, color1="goldenrod1", color2="brown")
        bottom_border_gradient.place(x=0, y=501, width=1214, height=251)
        bottom_border_gradient.config(bd=0, highlightthickness=0, relief='ridge')

        main_text_font = TkFont.Font(family="Arial", size=80)

        main_text = Text(self)
        main_text.place(x=4, y=4, width=1206, height=744)
        main_text.config(
            font=main_text_font, 
            wrap=WORD, 
            background="gray8", 
            foreground="springgreen", 
            insertbackground="gray70", 
            relief=FLAT
        )
        main_text.bind("<Button-1>", self.pre_notify)
        main_text.tag_configure("springgreen", foreground="springgreen")
        main_text.tag_configure("center", justify="center")
        main_text.insert("end", "\n\nEVOLUTION", "springgreen")
        main_text.tag_add("center", "1.0", "end")
        main_text.config(state="disabled")

        self.load_progress_label_variable = StringVar()
        self.load_progress_label_variable.set("0 %")
        self.load_progress_label = Label(self, textvariable=self.load_progress_label_variable, anchor="w")
        self.load_progress_label.place(x=750, y=400, width=100, height=30)
        self.load_progress_label.config(background="gray8", foreground="white", font=("Terminal", 12))

        self.load_progress_value = IntVar()
        self.load_progress_value.set(0)
        self.load_progress_bar = Progressbar(self, variable=self.load_progress_value)
        self.load_progress_bar.place(x=440, y=400, width=300, height=30)
        self.load_progress_bar.config(maximum=100)

    def update(self, *args) -> None:
        """Receive the update from the publisher"""

        if args[0] == "load_widgets":
            pass

    def subscribe(self, observer: Observer) -> None:
        """Subscribes an observer to the publisher"""

        self._observers.append(observer)

    def unsubscribe(self, observer: Observer) -> None:
        """Unsubscribes an observer from the publisher"""

        self._observers.remove(observer)

    def notify(self) -> None:
        """Notify all observer about an event"""

        for observers in self._observers:
            observers.update("load_app")

    def pre_notify(self, event):
        """This method interacts as a proxy to call to the notify method"""

        self.notify()

    def set_progress_bar(self, percentage):
        """This method will change the value of the progress bar"""

        self.load_progress_value.set(percentage)
        self.load_progress_label_variable.set(str(percentage) + " %")