# File to run the program. Handles serial communication with the Arduino, as well as detecting when blocks are placed or removed (with debouncing).
# Even though this file runs the program, main.py is the main file that decides what happens when the blocks are placed/removed.

import serial
from main import PORT, A0_THRESHOLD, A1_THRESHOLD, A2_THRESHOLD, A3_THRESHOLD, DETECT_DEBOUNCE_TIME, blocks_placed, blocks_removed, INITIAL_DELAY, loop, setup
import time

ser = serial.Serial(PORT, 9600, timeout=1) # Set up serial connection
start_time = time.perf_counter() # Start time for serial connection

# Initial values for the pins. Set them to max (1023 because 10-bit ADCs) to avoid jankiness during the first few seconds of the program.
pins = {
    "A0": 1023,
    "A1": 1023,
    "A2": 1023,
    "A3": 1023
}

setup() # Call setup function

# Function to parse line and extract id and data
def parse(line):
    try:
        id, data = line.split(':')
        id = id.strip()
        data = data.strip()
        return id, data
    except ValueError:
        return None, None

# Function to read data from serial and update pin values
def receive(ser):
    if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').rstrip()
                id, data = parse(line)
                if id in pins and data is not None:
                    pins[id] = int(data)
    return pins

def get_status(pins):
    # If any of the pins are above their threshold, not all blocks are placed. So, return false.
    if pins["A0"] > A0_THRESHOLD: return False
    if pins["A1"] > A1_THRESHOLD: return False
    if pins["A2"] > A2_THRESHOLD: return False
    if pins["A3"] > A3_THRESHOLD: return False
    
    # If all pins are below their threshold, all blocks are placed. So, return true.
    return True

# Function to handle triggers with debouncing
def handle_detect(pins):
    elapsed_time = time.perf_counter() - start_time
    # Static variables to store the previous status and debounce state
    if not hasattr(handle_detect, "previous_status"):
        handle_detect.previous_status = None
    if not hasattr(handle_detect, "debounce"):
        handle_detect.debounce = False

    # Get the current status
    current_status = get_status(pins)

    # Check if the status has changed and debounce is not active
    if current_status != handle_detect.previous_status and not handle_detect.debounce:
        handle_detect.debounce = True  # Activate debounce
        if current_status and elapsed_time > INITIAL_DELAY:
            blocks_placed()
        elif not current_status and elapsed_time > INITIAL_DELAY:
            blocks_removed()
        handle_detect.previous_status = current_status

        # Reset debounce after a short delay
        import threading
        def reset_debounce():
            handle_detect.debounce = False
        threading.Timer(DETECT_DEBOUNCE_TIME, reset_debounce).start()

# Infinite loop until program is exited
def program_loop():
    try:
        while True:
            pins = receive(ser)
            handle_detect(pins)
            loop(pins)
    except KeyboardInterrupt:
        print("Exiting program.")
    finally:
        ser.close()

# Start the loop
program_loop()