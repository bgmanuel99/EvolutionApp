import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

class SoundEffects():

    """This class loads the sounds of the application to be used by the frames and objects"""

    # Initialize pygame mixer object in order to be able to play sounds and music in the application
    pygame.mixer.init()

    button_click = pygame.mixer.Sound(os.getcwd().replace("\\", "/") + "/assets/sounds/interface_click.mp3")
    error_click = pygame.mixer.Sound(os.getcwd().replace("\\", "/") + "/assets/sounds/error_click.mp3")
    checkbutton_click = pygame.mixer.Sound(os.getcwd().replace("\\", "/") + "/assets/sounds/checkbox_click.mp3")