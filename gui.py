# File for GUI stuff
import tkinter as tk
import threading
import os
from PIL import Image, ImageTk
import time

# All GUI-related variables:
gui_state = -1  # -1 = not started, 0 = started, 1 = first hint, 2 = second hint, 3 = third hint, 4 = fourth hint, 5 = fifth hint, 6 = you win
timer_start_time = None

# All GUI elements:
root = None # GUI Window
text_pins = None # Displays pin values
text_title = None # Displays if blocks are placed or not
zeus_image = None # Image of zeus
text_pressSpace = None # Displays "Press space to continue" message
text_timer = None # Displays the timer
text_pressSpaceForHint = None # Displays "Press space for hint" message
text_hintCounter = None # Displays the hint counter
image_hint_label = None # Image of hint

def gui_init(img_zeus_path):
    # Init the tkiner window (for GUI). Use ESC to quit and F11 to toggle fullscreen.
    def start_gui():
        global root, text_pins, text_title, zeus_image, text_pressSpace, text_timer, text_pressSpaceForHint, text_hintCounter, hint_image_label
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

        hint_image = Image.open("hint-1.png")
        resized_hint_image = hint_image.resize((329, 605))  # Set desired width and height
        image_hint = ImageTk.PhotoImage(resized_hint_image)
        # Hint image
        hint_image_label = tk.Label(root, image=image_hint, bg="white")
        hint_image_label.image = image_hint

        text_title = tk.Label(root, text="Olympian Trials: The Puzzle of Zeus", font=("Helvetica", 32), bg="white", fg="green")
        text_title.pack(expand=True, fill=tk.BOTH)
        text_pressSpace = tk.Label(root, text="Press space to continue", font=("Helvetica", 16), bg="white", fg="black")
        text_pressSpace.pack(expand=True, fill=tk.BOTH)
        text_pins = tk.Label(root, text="", font=("Helvetica", 10), bg="white", fg="black")
        text_pins.pack(expand=True, fill=tk.BOTH)

        text_timer = tk.Label(root, text="timer", font=("Helvetica", 30), bg="white", fg="black")
        text_pressSpaceForHint = tk.Label(root, text="Press space for hint!", font=("Helvetica", 32), bg="white", fg="black")
        text_hintCounter = tk.Label(root, text="(0/5 hints used)", font=("Helvetica", 24), bg="white", fg="black")
        root.mainloop()
    gui_thread = threading.Thread(target=start_gui)
    gui_thread.start()
    return

def gui_space():
    global root, text_pressSpace, text_title, zeus_image, gui_state, text_timer, timer_start_time, gui_state, text_pressSpaceForHint, text_hintCounter, image_hint, hint_image_label
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
        text_pressSpaceForHint.pack(expand=True, fill=tk.BOTH)
        text_hintCounter.pack(expand=True, fill=tk.BOTH)

    elif(gui_state == 0):
        # 0 to 1: Transition to first hint
        root.after(0, lambda: text_hintCounter.config(text="(1/5 hints used)"))
        hint_image_label.pack(expand=True, fill=tk.BOTH)
        print("First hint!")
    elif(gui_state == 1):
        # 1 to 2: Transition to second hint
        root.after(0, lambda: text_hintCounter.config(text="(2/5 hints used)"))
        hint_image = Image.open("hint-2.png")
        resized_hint_image = hint_image.resize((329, 605))  # Set desired width and height
        image_hint = ImageTk.PhotoImage(resized_hint_image)
        root.after(0, lambda: hint_image_label.config(image=image_hint))
        print("Second hint!")
    elif(gui_state == 2):
        # 2 to 3: Transition to third hint
        root.after(0, lambda: text_hintCounter.config(text="(3/5 hints used)"))
        hint_image = Image.open("hint-3.png")
        resized_hint_image = hint_image.resize((329, 605))
        image_hint = ImageTk.PhotoImage(resized_hint_image)
        root.after(0, lambda: hint_image_label.config(image=image_hint))
        print("Third hint!")
    elif(gui_state == 3):
        # 3 to 4: Transition to fourth hint
        root.after(0, lambda: text_hintCounter.config(text="(4/5 hints used)"))
        hint_image = Image.open("hint-4.png")
        resized_hint_image = hint_image.resize((329, 605))
        image_hint = ImageTk.PhotoImage(resized_hint_image)
        root.after(0, lambda: hint_image_label.config(image=image_hint))
        print("Fourth hint!")
    elif(gui_state == 4):
        # 4 to 5: Transition to fifth hint
        root.after(0, lambda: text_hintCounter.config(text="(5/5 hints used)"))
        hint_image = Image.open("hint-5.png")
        resized_hint_image = hint_image.resize((329, 605))
        image_hint = ImageTk.PhotoImage(resized_hint_image)
        root.after(0, lambda: hint_image_label.config(image=image_hint))
        print("Fifth hint!")
        
    if(gui_state != 5):
        gui_state = gui_state + 1
    return

def gui_you_win():
    global root, gui_state, text_timer, text_pins

    if root and (gui_state != -1):
        # Cancel any pending `after` callbacks
        root.after_cancel(gui_update_timer)
        root.after_cancel(gui_update_pins)

        # Destroy all widgets in the root window
        for widget in root.winfo_children():
            widget.destroy()

        # Display the "You Win" message
        you_win_label = tk.Label(root, text="You Win!", font=("Helvetica", 48), bg="white", fg="green")
        you_win_label.pack(expand=True, fill=tk.BOTH)
        gui_state = 6 # Increment the state to indicate the game is over

    return

def gui_update_pins(pins):
    global gui_state
    if gui_state == 6:
        return
    global root, text_pins
    if root and text_pins and (gui_state != 6):
        root.after(0, lambda: text_pins.config(text=f"Pins: {pins}"))
    return

def gui_update_timer():
    global gui_state
    if gui_state == 6:
        return
    global root, text_timer, timer_start_time
    if gui_state != -1:
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