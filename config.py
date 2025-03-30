# CONFIG
PORT = 'COM9'  # Port connected to Arduino.
A0_THRESHOLD = 50
A1_THRESHOLD = 50
A2_THRESHOLD = 50
A3_THRESHOLD = 50
DETECT_DEBOUNCE_TIME = 0.5  # (seconds) Time to wait before checking if blocks are placed again.
INITIAL_DELAY = 5  # (seconds) Time to wait before checking if blocks are placed for the first time. Makes it less janky

# Stuff to happen when the blocks are placed
def blocks_placed():
    print("Blocks placed!")

# Stuff to happen when the blocks are removed
def blocks_removed():
    print("Blocks removed!")

# Stuff to happen every time the loop runs
def act(pins):
    # thing