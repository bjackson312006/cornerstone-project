# Main file for stuff. To start the program: python3 run.py

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
    print("Program started!")
    return

# Stuff to happen every time the loop runs. "pins" is a dictionary that contains pins["A0"], pins["A1"], pins["A2"]", and pins["A3"], whose values are updated continuously.
def loop(pins):
    print("pins[A0]:", pins["A0"])
    return

# Stuff to happen when the blocks are placed
def blocks_placed():
    print("Blocks placed!")
    return

# Stuff to happen when the blocks are removed
def blocks_removed():
    print("Blocks removed!")
    return