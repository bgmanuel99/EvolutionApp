from tkinter import *
from typing import List
from tkinter import font as TkFont
from tkinter.ttk import Progressbar
from components.models.gradients import GradientFrame
from components.interfaces.observer import Observer
from components.interfaces.publisher import Publisher
from components.audio.soundEffects import SoundEffects

class InitialFrame(Frame, Publisher):

    """
    This frame will serve as an introduction for the application.
    After the user presses the frame, the application will load to be used
    """

    def __init__(self, root):

        Frame.__init__(self, root, width=1214, height=752)
        self.config(background="gray8")
        self.propagate(False)

        self._observers: List[Observer] = []

        self.bind_all("<Key>", self.load_app)

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
        main_text.bind("<Enter>", lambda event: main_text.config(cursor="hand2"))
        main_text.bind("<Button-1>", self.load_app)
        main_text.tag_configure("springgreen", foreground="springgreen")
        main_text.tag_configure("center", justify="center")
        main_text.insert("end", "\n\nEVOLUTION", "springgreen")
        main_text.tag_add("center", "1.0", "end")
        main_text.config(state="disabled")

        self.load_progress_value = IntVar()
        self.load_progress_value.set(0)
        self.load_progress_bar = Progressbar(self, variable=self.load_progress_value)
        self.load_progress_bar.place(x=440, y=400, width=300, height=30)
        self.load_progress_bar.config(maximum=100)
        self.load_progress_bar.bind("<Enter>", self.load_progress_bar.config(cursor="hand2"))
        self.load_progress_bar.bind("<Button-1>", self.load_app)

        self.load_progress_label_variable = StringVar()
        self.load_progress_label_variable.set("0 %")
        self.load_progress_label = Label(self, textvariable=self.load_progress_label_variable, anchor="w")
        self.load_progress_label.place(x=750, y=400, width=100, height=30)
        self.load_progress_label.config(background="gray8", foreground="white", font=("Terminal", 12))
        self.load_progress_label.bind("<Enter>", self.load_progress_label.config(cursor="hand2"))
        self.load_progress_label.bind("<Button-1>", self.load_app)

        self.load_information_label_variable = StringVar()
        self.load_information_label_variable.set("Loading")
        self.load_information_label = Label(self, textvariable=self.load_information_label_variable, anchor="w")
        self.load_information_label.place(x=470, y=450, width=300, height=20)
        self.load_information_label.config(background="gray8", foreground="white", font=("Terminal", 11))
        self.load_information_label.bind("<Enter>", self.load_information_label.config(cursor="hand2"))
        self.load_information_label.bind("<Button-1>", self.load_app)

        # Variable that let the user start the application
        self.start_app = False

        # Variable for the time the click label shall be in each color
        self.spark_time = 10

        # Other variables to control the color of the click label
        self.back_and_force_number = -1
        self.continue_sparking = True

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

    def load_app(self, event):
        """This method interacts as a proxy to call to the notify method"""

        SoundEffects.button_click.play(loops=0)

        if self.start_app:
            self.unbind_all("<Key>")
            self.continue_sparking = False
            self.notify()

    def set_progress_bar(self, percentage):
        """This method will change the value of the progress bar"""

        self.load_progress_value.set(percentage)
        self.load_progress_label_variable.set(str(percentage) + " %")

    def set_progress_information(self, message):
        """This method will change the information label for the user to know what information is been load in the application"""

        self.load_information_label_variable.set("Loading " + str(message))

    def show_click_message(self):
        """This method will show a label which informs the user it can click the initial frame or press any key to start the application"""

        self.click_label_color = "gray100"
        self.click_label = Label(self, text="CLICK or PRESS any KEY to START the application", anchor="w")
        self.click_label.place(x=320, y=580, width=580, height=30)
        self.click_label.config(background="gray8", foreground=self.click_label_color, font=("Terminal", 12))
        self.click_label.bind("<Enter>", self.click_label.config(cursor="hand2"))
        self.click_label.bind("<Button-1>", self.load_app)
        self.spark_click_message()

        self.start_app = True

    def spark_click_message(self):
        """This method makes the click label spark from all tones of white"""

        if self.continue_sparking:
            click_label_color_number = int(self.click_label_color[4:])

            if click_label_color_number == 100:
                self.back_and_force_number = -1
            elif click_label_color_number == 15:
                self.back_and_force_number = 1

            if click_label_color_number >= 90:
                self.spark_time = 50
            elif click_label_color_number >= 80:
                self.spark_time = 45
            elif click_label_color_number >= 80:
                self.spark_time = 40
            elif click_label_color_number >= 70:
                self.spark_time = 35
            elif click_label_color_number >= 60:
                self.spark_time = 30
            elif click_label_color_number >= 50:
                self.spark_time = 25
            elif click_label_color_number >= 40:
                self.spark_time = 20
            elif click_label_color_number >= 30:
                self.spark_time = 15
            elif click_label_color_number >= 15:
                self.spark_time = 10

            self.click_label_color = "gray" + str(click_label_color_number + self.back_and_force_number)

            self.click_label.config(foreground=self.click_label_color)

            self.after(self.spark_time, self.spark_click_message)