# File for GUI stuff
import tkinter as tk
import threading
import os
from PIL import Image, ImageTk
import time

gui_state = -1  # -1 = not started, 0 = started, 1 = first hint, 2 = second hint, 3 = third hint, 4 = fourth hint, 5 = fifth hint
timer_start_time = None

# All GUI elements:
root = None # GUI Window
text_pins = None # Displays pin values
text_title = None # Displays if blocks are placed or not
zeus_image = None # Image of zeus
text_pressSpace = None # Displays "Press space to continue" message
text_timer = None # Displays the timer

def gui_init(img_zeus_path):
    # Init the tkiner window (for GUI). Use ESC to quit and F11 to toggle fullscreen.
    def start_gui():
        global root, text_pins, text_title, zeus_image, text_pressSpace
        root = tk.Tk()
        root.attributes('-fullscreen', True)
        root.bind("<Escape>", lambda e: gui_quit())
        root.bind("<space>", lambda e: gui_space())
        root.bind("<F11>", lambda e: root.attributes('-fullscreen', not root.attributes('-fullscreen')))

        gui_state = -1 # default state

        # Resize the image using Pillow
        original_image = Image.open(img_zeus_path)
        resized_image = original_image.resize((800, 800))  # Set desired width and height
        image = ImageTk.PhotoImage(resized_image)
        # Zeus image
        zeus_image = tk.Label(root, image=image, bg="white")
        zeus_image.image = image  # Keep a reference to avoid garbage collection
        zeus_image.pack(expand=True, fill=tk.BOTH)

        text_title = tk.Label(root, text="Olympian Trials: The Puzzle of Zeus", font=("Helvetica", 32), bg="white", fg="green")
        text_title.pack(expand=True, fill=tk.BOTH)
        text_pressSpace = tk.Label(root, text="Press space to continue", font=("Helvetica", 16), bg="white", fg="black")
        text_pressSpace.pack(expand=True, fill=tk.BOTH)
        text_pins = tk.Label(root, text="", font=("Helvetica", 10), bg="white", fg="black")
        text_pins.pack(expand=True, fill=tk.BOTH)

        text_timer = tk.Label(root, text="timer", font=("Helvetica", 10), bg="white", fg="black")
        root.mainloop()
    gui_thread = threading.Thread(target=start_gui)
    gui_thread.start()
    return

def gui_space():
    global root, text_pressSpace, text_title, zeus_image, gui_state, text_timer
    if(gui_state == -1):
        # -1 to 0: Transition to game
        # Hide title screen stuff
        root.after(0, lambda: text_pressSpace.pack_forget())
        root.after(0, lambda: text_title.pack_forget())
        root.after(0, lambda: text_pins.pack_forget())
        root.after(0, lambda: zeus_image.pack_forget())
        # Show game stuff
        timer_start_time = time.time() # Start the timer
        root.after(0, lambda: text_timer.config(text="Time: 00:00"))  # Initialize the timer text
        text_timer.pack(expand=True, fill=tk.BOTH)

    elif(gui_state == 0):
        # 0 to 1: Transition to first hint
        gui_state = gui_state + 1
    return

def gui_update_pins(pins):
    global root, text_pins
    if root and text_pins:
        root.after(0, lambda: text_pins.config(text=f"Pins: {pins}"))
    return

def gui_update_timer():
    global root, text_timer, timer_start_time
    if root and text_timer:
        elapsed_time = time.time() - timer_start_time
        minutes, seconds = divmod(elapsed_time, 60)
        formatted_time = f"{int(minutes):02}:{int(seconds):02}"
        root.after(0, lambda: text_timer.config(text=f"Time: {formatted_time}"))
    return

def gui_update_blocksPlaced(msg, color="white"):
    global root, text_blocksPlaced
    if root and text_blocksPlaced:
        root.after(0, lambda: text_blocksPlaced.config(text=msg, fg=color))
    return

def gui_quit():
    global root
    if root:
        root.quit()
        root.destroy()
        
    os._exit(0)  # Force exit the program
    return