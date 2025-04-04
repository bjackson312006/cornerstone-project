# File for GUI stuff
import tkinter as tk
from tkinter import font
import threading
import os
from PIL import Image, ImageTk
import time
import pygame
import sys
import csv
from datetime import datetime

# All GUI-related variables:
gui_state = -2  # -1 = not started, 0 = started, 1 = first hint, 2 = second hint, 3 = third hint, 4 = fourth hint, 5 = fifth hint, 6 = you win
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
text_restartForTheNextPlayer = None # Displays "Press space to restart for the next player" message
image_olympianTrials = None # Image of Olympian Trials
image_zeus2 = None # Image of Zeus 2
image_titlescreen_showing = None
image_titlescreen_notshowing = None # Image of title screen not showing
is_title_showing = True
image_titlescreen_label = None
image_instructions_label = None
image_pressSpaceForHint_label = None
image_ps0 = None # Image of press space for hint 0
image_ps1 = None # Image of press space for hint 1
image_ps2 = None # Image of press space for hint 2
image_ps3 = None # Image of press space for hint 3
image_ps4 = None # Image of press space for hint 4
image_ps5 = None # Image of press space for hint 5
image_youwin_label = None # Image of you win
image_youwin = None # Image of you win

def gui_init():
    # Init the tkiner window (for GUI). Use ESC to quit and F11 to toggle fullscreen.
    def start_gui():
        global root, text_pins, text_title, zeus_image, text_pressSpace, text_timer, text_pressSpaceForHint, text_hintCounter, hint_image_label, text_restartForTheNextPlayer, image_olympianTrials, image_titlescreen, is_title_showing, image_titlescreen_label, image_titlescreen_notshowing, image_titlescreen_showing, image_instructions_label, image_pressSpaceForHint_label, image_ps0, image_ps1, image_ps2, image_ps3, image_ps4, image_ps5, image_youwin, image_youwin_label
        root = tk.Tk()
        root.attributes('-fullscreen', True)
        root.bind("<Escape>", lambda e: gui_quit())
        root.bind("<space>", lambda e: gui_space())
        root.bind("<F11>", lambda e: root.attributes('-fullscreen', not root.attributes('-fullscreen')))
        root.bind("<Control-space>", lambda e: restart_script())


        gui_state = -2 # default state

        image_titlescreen_showing = ImageTk.PhotoImage(Image.open("title_screen_showing.png"))
        image_titlescreen_notshowing = ImageTk.PhotoImage(Image.open("title_screen_notshowing.png"))
        image_titlescreen_label = tk.Label(root, image=image_titlescreen_showing, bg="white")
        image_titlescreen_label.pack(expand=True, fill=tk.BOTH)
        is_title_showing = True
        toggle_title_image()

        image_instructions = ImageTk.PhotoImage(Image.open("instructions.png"))
        image_instructions_label = tk.Label(root, image=image_instructions, bg="white")

        image_ps0 = ImageTk.PhotoImage(Image.open("ps_0.png"))
        image_ps1 = ImageTk.PhotoImage(Image.open("ps_1.png"))
        image_ps2 = ImageTk.PhotoImage(Image.open("ps_2.png"))
        image_ps3 = ImageTk.PhotoImage(Image.open("ps_3.png"))
        image_ps4 = ImageTk.PhotoImage(Image.open("ps_4.png"))
        image_ps5 = ImageTk.PhotoImage(Image.open("ps_5.png"))

        image_pressSpaceForHint_label = tk.Label(root, image=image_ps0, bg="white")

        # Pre-load the "You Win" image
        image_youwin = ImageTk.PhotoImage(Image.open("YouWin.png"))
        image_youwin_label = tk.Label(root, image=image_youwin, bg="white")
        image_youwin_label.place(x=0, y=0, relwidth=1, relheight=1)
        image_youwin_label.place_forget()  # Hide it initially



        hint_image = Image.open("hint-0.png")
        resized_hint_image = hint_image.resize((329, 605))  # Set desired width and height
        image_hint = ImageTk.PhotoImage(resized_hint_image)
        # Hint image
        hint_image_label = tk.Label(root, image=image_hint, bg="white")
        hint_image_label.image = image_hint

        #text_pins = tk.Label(root, text="", font=("Helvetica", 10), bg="white", fg="black")
        #text_pins.pack(expand=True, fill=tk.BOTH)

        text_timer = tk.Label(root, text="timer", font=("Helvetica", 60, "bold"), bg="white", fg="black")
        text_pressSpaceForHint = tk.Label(root, text="Press space for hint!", font=("Helvetica", 32), bg="white", fg="black")
        text_hintCounter = tk.Label(root, text="(0/5 hints used)", font=("Helvetica", 24), bg="white", fg="black")
        root.mainloop()
    gui_thread = threading.Thread(target=start_gui)
    gui_thread.start()
    return

def toggle_title_image():
    global image_titlescreen_label, root, is_title_showing, image_titlescreen_showing, image_titlescreen_notshowing, gui_state
    if gui_state != -2 and gui_state != -1:
        return
    if is_title_showing:
        image_titlescreen_label.config(image=image_titlescreen_notshowing)
        is_title_showing = False
    else:
        image_titlescreen_label.config(image=image_titlescreen_showing)
        is_title_showing = True
    root.after(500, toggle_title_image)


def gui_space():
    global root, text_pressSpace, text_title, zeus_image, gui_state, text_timer, timer_start_time, gui_state, text_pressSpaceForHint, text_hintCounter, image_hint, hint_image_label, image_titlescreen_label, image_instructions_label,  image_pressSpaceForHint_label, image_ps0, image_ps1, image_ps2, image_ps3, image_ps4, image_ps5
    if(gui_state == -2):
        # -2 to -1: Transition to instructions
        # Hide title screen stuff
        root.after(0, lambda: (image_titlescreen_label.pack_forget(), toggle_title_image()))
        # Show instructions
        root.after(0, lambda: image_instructions_label.pack(expand=True, fill=tk.BOTH))
    elif(gui_state == -1):
        # -1 to 0: Transition to game start
        # Hide instructions
        root.after(0, lambda: image_instructions_label.pack_forget())
        # Show game stuff
        timer_start_time = time.time() # Start the timer
        root.after(0, lambda: text_timer.config(text="Time: 00:00"))  # Initialize the timer text
        image_pressSpaceForHint_label.place(x=0, y=0, relwidth=1, relheight=1)

        text_timer.place(relx=0.5, rely=0.1, anchor="center")  # Adjust relx, rely for positioning
        hint_image_label.place(relx=0.5, rely=0.5, anchor="center")  # Center the hint image


    elif(gui_state == 0):
        # 0 to 1: Transition to first hint
        hint_image = Image.open("hint-1.png")
        resized_hint_image = hint_image.resize((329, 605))  # Set desired width and height
        image_hint = ImageTk.PhotoImage(resized_hint_image)
        root.after(0, lambda: hint_image_label.config(image=image_hint))
        root.after(0, lambda: image_pressSpaceForHint_label.config(image=image_ps1))

    elif(gui_state == 1):
        # 1 to 2: Transition to second hint
        hint_image = Image.open("hint-2.png")
        resized_hint_image = hint_image.resize((329, 605))  # Set desired width and height
        image_hint = ImageTk.PhotoImage(resized_hint_image)
        root.after(0, lambda: hint_image_label.config(image=image_hint))
        root.after(0, lambda: image_pressSpaceForHint_label.config(image=image_ps2))
        print("Second hint!")
    elif(gui_state == 2):
        # 2 to 3: Transition to third hint
        hint_image = Image.open("hint-3.png")
        resized_hint_image = hint_image.resize((329, 605))
        image_hint = ImageTk.PhotoImage(resized_hint_image)
        root.after(0, lambda: hint_image_label.config(image=image_hint))
        root.after(0, lambda: image_pressSpaceForHint_label.config(image=image_ps3))
        print("Third hint!")
    elif(gui_state == 3):
        # 3 to 4: Transition to fourth hint
        hint_image = Image.open("hint-4.png")
        resized_hint_image = hint_image.resize((329, 605))
        image_hint = ImageTk.PhotoImage(resized_hint_image)
        root.after(0, lambda: hint_image_label.config(image=image_hint))
        root.after(0, lambda: image_pressSpaceForHint_label.config(image=image_ps4))
        print("Fourth hint!")
    elif(gui_state == 4):
        # 4 to 5: Transition to fifth hint
        hint_image = Image.open("hint-5.png")
        resized_hint_image = hint_image.resize((329, 605))
        image_hint = ImageTk.PhotoImage(resized_hint_image)
        root.after(0, lambda: hint_image_label.config(image=image_hint))
        root.after(0, lambda: image_pressSpaceForHint_label.config(image=image_ps5))
        print("Fifth hint!")
        
    if(gui_state != 5):
        gui_state = gui_state + 1
    return

def gui_you_win():
    global root, gui_state, text_timer, timer_start_time, image_youwin_label, image_youwin

    if root and (gui_state != -2) and (gui_state != -1) and (gui_state != 6):
        # Stop the timer updates
        root.after_cancel(gui_update_timer)

        # Calculate elapsed time
        elapsed_time = time.time() - timer_start_time
        minutes, seconds = divmod(elapsed_time, 60)
        formatted_time = f"{int(minutes):02}:{int(seconds):02}"

        image_youwin_label.place(x=0, y=0, relwidth=1, relheight=1)

        final_time_label = tk.Label(root, text=f"Final Time: {formatted_time}", font=("Helvetica", 100, "bold"), bg="white", fg="black")
        final_time_label.place(relx=0.5, rely=0.65, anchor="center")

        # Destroy all widgets in the root window
        for widget in root.winfo_children():
            if (widget != image_youwin_label) and (widget != final_time_label):  # Keep the "You Win" image label
                widget.destroy()

        # Log the time to a CSV file
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("time_list.csv", mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([current_datetime, formatted_time])

        gui_state = 6  # Set the state to indicate the game is over

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
    if gui_state != -2 and gui_state != -1:
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

def restart_script():
    global gui_state
    python = sys.executable
    os.execv(python, ['python'] + sys.argv)