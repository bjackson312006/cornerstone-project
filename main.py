# Main file for stuff. To start the program: python3 run.py
from gui import gui_init, gui_update_pins, gui_you_win, gui_update_timer, gui_state
import pygame
# CONFIG
PORT = 'COM9'  # Port connected to Arduino.
A0_THRESHOLD = 50
A1_THRESHOLD = 50
A2_THRESHOLD = 50
A3_THRESHOLD = 50
DETECT_DEBOUNCE_TIME = 0.5  # (seconds) Time to wait before checking if blocks are placed again.
INITIAL_DELAY = 5  # (seconds) Time to wait before checking if blocks are placed for the first time. Makes it less janky

# Stuff to happen at startup
def setup():
    gui_init()
    return

# Stuff to happen every time the loop runs.
# "pins" is a dictionary that contains pins["A0"], pins["A1"], pins["A2"]", and pins["A3"], whose values are updated continuously.
def loop(pins):
    gui_update_pins(pins)
    #print("Pins: ", pins)
    gui_update_timer()
    return

# Stuff to happen when the blocks are placed
def blocks_placed():
    print("Blocks are placed!")
    gui_you_win()
    # Play sound when blocks are placed
    pygame.mixer.init()
    pygame.mixer.music.load("bolt.mp3")
    pygame.mixer.music.play()
    # Wait for the sound to finish playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)  # Wait for the sound to finish playing
        
    return

# Stuff to happen when the blocks are removed
def blocks_removed():
    print("Blocks are removed!")
    return