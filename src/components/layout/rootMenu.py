import os
import csv
from tkinter import *
from tkinter import ttk
from typing import List
from components.models.gradients import GradientFrame
from components.interfaces.observer import Observer
from components.interfaces.publisher import Publisher
from components.audio.soundEffects import SoundEffects

class RootMenuBar(Menu, Publisher, Observer):

    """
    This is the root (main) menu bar of the application.
    It is also a publisher so it can notify its state and changes to other observers like the command terminal.
    """

    def __init__(self, root: Tk):
        Menu.__init__(self, root)

        self._observers: List[Observer] = []

        # This variable is created in order to know which command has been pressed in the menu before it is notify to the rest of the application frames
        self.pressed_command = ""

        # File menu commands
        self.file_menu = Menu(self, tearoff=0)
        self.file_menu.add_command(label="Volume", command=self.volume_popup)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=lambda: self.pre_notify("exit"))

        # Edit menu commands
        self.edit_menu = Menu(self, tearoff=0)
        self.edit_menu.add_command(label="Copy", command=lambda: self.pre_notify("copy"))
        self.edit_menu.add_command(label="Paste", command=lambda: self.pre_notify("paste"))

        # Run menu commands
        self.run_menu = Menu(self, tearoff=0)
        self.run_menu.add_command(label="Run", command=lambda: self.pre_notify("run"))
        self.run_menu.add_command(label="Stop", command=lambda: self.pre_notify("stop"))
        self.run_menu.add_command(label="Continue", command=lambda: self.pre_notify("continue"))
        self.run_menu.add_command(label="Restart", command=lambda: self.pre_notify("restart"))
        self.run_menu.add_separator()
        self.environment_submenu = Menu(self.run_menu, tearoff=0)
        self.environment_submenu.add_command(label="Polar", command=lambda: self.pre_notify("polar"))
        self.environment_submenu.add_command(label="Mediterranean", command=lambda: self.pre_notify("mediterranean"))
        self.environment_submenu.add_command(label="Desert", command=lambda: self.pre_notify("desert"))
        self.run_menu.add_cascade(label="Environments", menu=self.environment_submenu)

        # Terminal menu commands
        self.terminal_menu = Menu(self, tearoff=0)
        self.terminal_menu.add_command(label="Clear terminal", command=lambda: self.pre_notify("clear"))

        # Help menu commands
        self.help_menu = Menu(self, tearoff=0)
        self.help_menu.add_command(label="Help", command=self.help_popup)
        self.help_menu.add_separator()
        self.help_menu.add_command(label="About...", command=self.about_popup)

        # Colors for the help, about and volume popups
        self.help_gradient_colors = ["SpringGreen4", "OliveDrab1"]
        self.about_gradient_colors = ["SpringGreen4", "OliveDrab1"]
        self.volume_gradient_colors = ["SpringGreen4", "OliveDrab1"]
        
        # The gradients for the help, about and volume popups need to be initilized as None
        self.information_gradient = None
        self.search_gradient = None
        self.volume_gradient = None

        # Finally all the menu are added to the main menu of the application
        self.add_cascade(label="File", menu=self.file_menu)
        self.add_cascade(label="Edit", menu=self.edit_menu)
        self.add_cascade(label="Run", menu=self.run_menu)
        self.add_cascade(label="Terminal", menu=self.terminal_menu)
        self.add_cascade(label="Help", menu=self.help_menu)

    def subscribe(self, observer: Observer) -> None:
        """Subscribes an observer to the publisher"""

        self._observers.append(observer)

    def unsubscribe(self, observer: Observer) -> None:
        """Unsubscribes an observer from the publisher"""

        self._observers.remove(observer)

    def pre_notify(self, command):
        """
        This method is called before the notify method of the publisher to change an internal variable for the observers to know the command pressed on the menu
        """
        
        self.pressed_command = command
        self.notify()

    def notify(self) -> None:
        """Notify all observer about an event"""

        if self.pressed_command in ["exit", "copy", "paste", "run", "stop", "continue", "restart", "clear", "polar", "mediterranean", "desert"]:
            for observers in self._observers:
                observers.update(self.pressed_command)

    def update(self, *args) -> None:
        """Receive the update from the publisher"""

        if args[0] == "change_environment":
            if args[1] == "polar":
                self.help_gradient_colors = ["magenta4", "RoyalBlue2"]
                self.about_gradient_colors = ["magenta4", "RoyalBlue2"]
                self.volume_gradient_colors = ["magenta4", "RoyalBlue2"]
                if self.search_gradient: self.search_gradient.set_new_colors("magenta4", "RoyalBlue2")
                if self.information_gradient: self.information_gradient.set_new_colors("magenta4", "RoyalBlue2")
                if self.volume_gradient: self.volume_gradient.set_new_colors("magenta4", "RoyalBlue2")
            elif args[1] == "mediterranean":
                self.help_gradient_colors = ["SpringGreen4", "OliveDrab1"]
                self.about_gradient_colors = ["SpringGreen4", "OliveDrab1"]
                self.volume_gradient_colors = ["SpringGreen4", "OliveDrab1"]
                if self.search_gradient: self.search_gradient.set_new_colors("SpringGreen4", "OliveDrab1")
                if self.information_gradient: self.information_gradient.set_new_colors("SpringGreen4", "OliveDrab1")
                if self.volume_gradient: self.volume_gradient.set_new_colors("SpringGreen4", "OliveDrab1")
            elif args[1] == "desert":
                self.help_gradient_colors = ["brown", "goldenrod1"]
                self.about_gradient_colors = ["brown", "goldenrod1"]
                self.about_gradient_colors = ["brown", "goldenrod1"]
                if self.search_gradient: self.search_gradient.set_new_colors("brown", "goldenrod1")
                if self.information_gradient: self.information_gradient.set_new_colors("brown", "goldenrod1")
                if self.volume_gradient: self.volume_gradient.set_new_colors("brown", "goldenrod1")

    def about_popup(self):
        """This function, attached to the about button of the menu bar, will display general information about the application"""

        information_window = Toplevel(width=700, height=150)
        information_window.wm_title("Evolution App Information")
        information_window.resizable(0, 0)
        information_window.propagate(False)
        information_window.iconbitmap(os.getcwd().replace("\\", "/") + "/assets/icon/evolution.ico")

        self.information_gradient = GradientFrame(information_window, self.about_gradient_colors[0], self.about_gradient_colors[1])
        self.information_gradient.pack()
        self.information_gradient.config(bd=0, highlightthickness=0, relief='ridge')

        information_window.bind("<Destroy>", self.reinitialize_information_gradient)

        information_frame = Frame(self.information_gradient, width=700, height=150)
        information_frame.pack(fill=BOTH, padx=4, pady=4)
        information_frame.pack_propagate(0)
        information_frame.config(background="gray8")

        information_text = Text(information_frame)
        information_text.pack(expand=True, fill=BOTH)
        information_text.config(
            relief=FLAT, 
            font=("Terminal", 11), 
            wrap=WORD, 
            background="gray8", 
            insertbackground="gray70"
        )
        information_text.tag_configure("springgreen", foreground="springgreen")
        information_text.tag_configure("gray70", foreground="gray70")
        information_text.tag_configure("darkviolet", foreground="dark violet")
        information_text.tag_configure("center", justify="center")

        information_text.insert("end", "\n\nThis is the ", "gray70")
        information_text.insert("end", "Evolution app", "springgreen")
        information_text.insert("end", "!!\n", "gray70")
        information_text.insert("end", "This application use a ", "gray70")
        information_text.insert("end", "Genetic Algorithm ", "springgreen")
        information_text.insert("end", "to represent the darwinism theory of evolution by natural selection.\n", "gray70")
        information_text.insert("end", "This type of algorithms simbolizes a promising area of artificial intelligence and are inspired in the evolution theories.\n", "gray70")
        information_text.insert("end", "With the use of this algorithm a population will evolve during a finite number of epochs while it continues to adapt to it's\n", "gray70")
        information_text.insert("end", "environment, mutating each individual along with the evolution of the species as a whole.\n", "gray70")
        information_text.insert("end", "\nAuthor", "darkviolet")
        information_text.insert("end", ": An intelligent monkey\n", "gray70")
        information_text.insert("end", "Version", "darkviolet")
        information_text.insert("end", ": 1.0", "gray70")

        information_text.tag_add("center", "1.0", "end")
        information_text.config(state="disabled")

    def help_popup(self):
        """This function, attached to the help button of the menu bar, will display a dialog window in which a user can search for information of each panel on the application"""

        search_window = Toplevel(width=608, height=328)
        search_window.wm_title("Application Use Information")
        search_window.resizable(0, 0)
        search_window.propagate(False)
        search_window.iconbitmap(os.getcwd().replace("\\", "/") + "/assets/icon/evolution.ico")

        self.search_gradient = GradientFrame(search_window, self.help_gradient_colors[0], self.help_gradient_colors[1])
        self.search_gradient.pack()
        self.search_gradient.config(bd=0, highlightthickness=0, relief='ridge')

        search_window.bind("<Destroy>", self.reinitilize_search_gradient)

        search_frame = Frame(self.search_gradient, width=600, height=320)
        search_frame.pack(fill=BOTH, padx=4, pady=4)
        search_frame.pack_propagate(0)
        search_frame.config(background="gray8")

        self.search_text = Text(search_frame)
        self.search_text.place(x=0, y=0, width=600, height=300)
        self.search_text.config(
            relief=FLAT,
            font=("Terminal", 11),
            wrap=WORD,
            background="gray8",
            insertbackground="gray70"
        )
        self.search_text.tag_configure("springgreen", foreground="springgreen")
        self.search_text.tag_configure("gray70", foreground="gray70")
        self.search_text.tag_configure("OliveDrab1", foreground="OliveDrab1")
        self.search_text.tag_configure("darkviolet", foreground="dark violet")
        self.search_text.tag_configure("center", justify="center")
        self.display_information(os.getcwd().replace("\\", "/") + "/archive/mainmenuinformation.csv")

        search_label = Label(search_frame, text="Search for any information of the main menu:", anchor="w")
        search_label.place(x=0, y=300, width=230, height=20)
        search_label.config(background="gray8", foreground="white", font=("Terminal", 11))

        self.search_entry_variable = StringVar()
        self.search_entry_variable.set("")
        self.search_entry = Entry(search_frame, textvariable=self.search_entry_variable)
        self.search_entry.place(x=230, y=300, width=200, height=20)
        self.search_entry.config(
            background="gray8", 
            foreground="gray70", 
            font=("Terminal", 11), 
            justify=LEFT, 
            bd=0, 
            highlightthickness=1, 
            highlightbackground="dark violet", 
            highlightcolor="dark violet", 
            relief='ridge'
        )
        self.search_entry.bind("<Button-1>", self.search_entry_pressed)
        self.search_entry.bind("<FocusOut>", self.search_entry_focus_out)
        self.search_entry.bind("<Return>", lambda event: self.process_entry_data(entry=True))

        self.search_button_frame = Frame(search_frame)
        self.search_button_frame.place(x=430, y=300, width=85, height=20)
        self.search_button_frame.config(background="dark violet", bd=0)
        search_button = Button(self.search_button_frame, text="Search")
        search_button.place(x=1, y=1, width=83, height=18)
        search_button.config(
            background="gray8", 
            activebackground="gray8", 
            foreground="gray70", 
            activeforeground="springgreen", 
            font=("Terminal", 11), 
            bd=0, 
            relief="ridge"
        )
        search_button.bind("<Button-1>", lambda event: self.process_entry_data(entry=False))
        search_button.bind("<ButtonRelease>", self.search_button_release)

        self.search_main_menu_button_frame = Frame(search_frame)
        self.search_main_menu_button_frame.place(x=515, y=300, width=85, height=20)
        self.search_main_menu_button_frame.config(background="dark violet", bd=0)
        search_main_menu_button = Button(self.search_main_menu_button_frame, text="Menu")
        search_main_menu_button.place(x=1, y=1, width=83, height=18)
        search_main_menu_button.config(
            background="gray8", 
            activebackground="gray8", 
            foreground="gray70", 
            activeforeground="springgreen", 
            font=("Terminal", 11), 
            bd=0, 
            relief="ridge"
        )
        search_main_menu_button.bind("<Button-1>", self.search_main_menu_button_pressed)
        search_main_menu_button.bind("<ButtonRelease>", self.search_main_menu_button_release)

    def volume_popup(self):
        """This method creates the popup from which the user can change the volume of the application"""

        volume_window = Toplevel(width=250, height=250)
        volume_window.wm_title("Volume")
        volume_window.resizable(0, 0)
        volume_window.propagate(False)
        volume_window.iconbitmap(os.getcwd().replace("\\", "/") + "/assets/icon/evolution.ico")

        self.volume_gradient = GradientFrame(volume_window, self.volume_gradient_colors[0], self.volume_gradient_colors[1])
        self.volume_gradient.place(x=0, y=0, width=250, height=250)
        self.volume_gradient.config(bd=0, highlightthickness=0, relief='ridge')

        volume_window.bind("<Destroy>", self.reinitilize_volume_gradient)

        volume_frame = Frame(self.volume_gradient)
        volume_frame.place(x=4, y=4, width=242, height=242)
        volume_frame.pack_propagate(0)
        volume_frame.config(background="gray8")

        buttons_volume_label = Label(volume_frame, text="Environment volume", anchor="w")
        buttons_volume_label.place(x=75, y=20, width=100, height=20)
        buttons_volume_label.config(background="gray8", foreground="white", font=("Terminal", 11))

        self.buttons_volume_slider = ttk.Scale(volume_frame, from_=100, to=0, orient='vertical', command=self.set_buttons_volume)
        self.buttons_volume_slider.place(x=110, y=50, width=25, height=150)

        self.buttons_volume_value = Label(volume_window, text=str(int(round(self.buttons_volume_slider.get(), 0))) + " %")
        self.buttons_volume_value.place(x=113, y=210, width=30, height=20)
        self.buttons_volume_value.config(background="gray8", foreground="white", font=("Terminal", 11))
        
        self.buttons_volume_slider.set(100)

    def set_buttons_volume(self, event):
        """
        This method will be called whenever the value of the buttons volume slider is changed by the user.
        It will change the labels value on the volumes popup and notify the objects of the application to set the new volume value
        """

        self.buttons_volume_value.config(text=str(int(round(self.buttons_volume_slider.get(), 0))) + " %")

        SoundEffects.button_click.set_volume(int(round(self.buttons_volume_slider.get(), 0)) / 100)
        SoundEffects.error_click.set_volume(int(round(self.buttons_volume_slider.get(), 0)) / 100)
        SoundEffects.checkbutton_click.set_volume(int(round(self.buttons_volume_slider.get(), 0)) / 100)

    def reinitialize_information_gradient(self, event):
        """This method reinitilize the information gradient to None"""

        self.information_gradient = None

    def reinitilize_search_gradient(self, event):
        """This method reinitilize the search gradient to None"""

        self.search_gradient = None

    def reinitilize_volume_gradient(self, event):
        """This method reinitilize the volume gradient to None"""

        self.volume_gradient = None

    def search_entry_pressed(self, event):
        """This function will be called when the search entry of the help popup is being focused"""

        self.search_entry.config(highlightbackground="magenta3", highlightcolor="magenta3")

    def search_entry_focus_out(self, event):
        """This function will be called when the search entry of the help popup has no longer the focus"""

        self.search_entry.config(highlightbackground="dark violet", highlightcolor="dark violet")

    def process_entry_data(self, entry=False):
        """This function will be called when a user press the search button on the help popup"""

        if not entry:
            self.play_button_sound()
            self.search_button_frame.config(background="magenta3")

        if self.search_entry_variable.get() == "1" or self.search_entry_variable.get().lower() == "general information":
            self.delete_search_text()
            self.display_information(os.getcwd().replace("\\", "/") + "/archive/generalinformation.csv")
        elif self.search_entry_variable.get() == "2" or self.search_entry_variable.get().lower() == "menu bar":
            self.delete_search_text()
            self.display_information(os.getcwd().replace("\\", "/") + "/archive/menubarinformation.csv")
        elif self.search_entry_variable.get() == "3" or self.search_entry_variable.get().lower() == "top frame":
            self.delete_search_text()
            self.display_information(os.getcwd().replace("\\", "/") + "/archive/topframeinformation.csv")
        elif self.search_entry_variable.get() == "4" or self.search_entry_variable.get().lower() == "bottom frame":
            self.delete_search_text()
            self.display_information(os.getcwd().replace("\\", "/") + "/archive/bottomframeinformation.csv")
        elif self.search_entry_variable.get() == "5" or self.search_entry_variable.get().lower() == "election frame":
            self.delete_search_text()
            self.display_information(os.getcwd().replace("\\", "/") + "/archive/electionframeinformation.csv")
        elif self.search_entry_variable.get() == "6" or self.search_entry_variable.get().lower() == "evolution frame":
            self.delete_search_text()
            self.display_information(os.getcwd().replace("\\", "/") + "/archive/evolutionframeinformation.csv")
        elif self.search_entry_variable.get() == "7" or self.search_entry_variable.get().lower() == "information frame":
            self.delete_search_text()
            self.display_information(os.getcwd().replace("\\", "/") + "/archive/informationframeinformation.csv")
        elif self.search_entry_variable.get() == "8" or self.search_entry_variable.get().lower() == "environment frame":
            self.delete_search_text()
            self.display_information(os.getcwd().replace("\\", "/") + "/archive/environmentframeinformation.csv")

    def search_button_release(self, event):
        """This function will be called when a user release the search button on the help popup"""

        self.search_button_frame.config(background="dark violet")

    def search_main_menu_button_pressed(self, event):
        """This function will be called when a user press the main menu button on the help popup"""

        self.play_button_sound()

        self.search_main_menu_button_frame.config(background="magenta3")

        self.delete_search_text()
        self.display_information(os.getcwd().replace("\\", "/") + "/archive/mainmenuinformation.csv")

    def search_main_menu_button_release(self, event):
        """This function will be called when a user release the main menu button on the help popup"""

        self.search_main_menu_button_frame.config(background="dark violet")

    def delete_search_text(self):
        """This function will delete the information displayed in the search popup"""

        self.search_text.config(state="normal")
        self.search_text.delete("1.0", END)
        self.search_text.config(state="disabled")

    def new_line(self):
        """Inserts a new line in the terminal"""

        self.search_text.insert("end", "\n")

    def display_information(self, path):
        """This function will be called whenever the information of any frame need to be displayed in the help popup main text object"""

        self.search_text.config(state="normal")

        with open(path, newline="\n") as csvFile:
            reader = csv.reader(csvFile, delimiter=",")
            
            for position, message, color in reader:
                position = position.replace('"', '')
                message = message.replace('"', '')
                color = color.replace('"', '')
                if position == "center": 
                    self.search_text.tag_add(position, "1.0", "end")
                    continue
                split_message = message.split("\\n")
                count_before_breaks = True
                count_after_breaks = False
                before_breaks = 0
                after_breaks = 0
                actual_message = ""
                
                for word in split_message:
                    if word == "" and count_before_breaks: before_breaks += 1
                    elif word == "" and count_after_breaks: after_breaks += 1
                    else: 
                        actual_message = word
                        count_before_breaks = False
                        count_after_breaks = True
                
                for _ in range(before_breaks): self.new_line()
                self.search_text.insert(position, actual_message, color)
                for _ in range(after_breaks): self.new_line()

        self.search_text.config(state="disabled")

    def play_button_sound(self):
        """This method loads and plays the sound of a button been pressed for the search button in the help popup"""

        SoundEffects.button_click.play(loops=0)