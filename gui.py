# File for GUI stuff
import tkinter as tk
import threading
import os

# All GUI elements:
root = None # GUI Window
text_pins = None # Displays pin values
text_blocksPlaced = None # Displays if blocks are placed or not
zeus_image = None # Image of zeus

def gui_init(img_zeus_path):
    # Init the tkiner window (for GUI). Use ESC to quit and F11 to toggle fullscreen.
    def start_gui():
        global root, text_pins, text_blocksPlaced, zeus_image
        root = tk.Tk()
        root.attributes('-fullscreen', True)
        root.bind("<Escape>", lambda e: gui_quit())
        root.bind("<F11>", lambda e: root.attributes('-fullscreen', not root.attributes('-fullscreen')))

        # Zeus image
        image = tk.PhotoImage(file=img_zeus_path)
        zeus_image = tk.Label(root, image=image, bg="black")
        zeus_image.image = image

        text_pins = tk.Label(root, text="", font=("Helvetica", 32), bg="black", fg="white")
        text_pins.pack(expand=True, fill=tk.BOTH)
        text_blocksPlaced = tk.Label(root, text="Program Started", font=("Helvetica", 32), bg="black", fg="white")
        text_blocksPlaced.pack(expand=True, fill=tk.BOTH)
        root.mainloop()
    gui_thread = threading.Thread(target=start_gui)
    gui_thread.start()
    return

def gui_update_pins(pins):
    global root, text_pins
    if root and text_pins:
        root.after(0, lambda: text_pins.config(text=f"Pins: {pins}"))
    return

def gui_update_blocksPlaced(msg, color="white"):
    global root, text_blocksPlaced
    if root and text_blocksPlaced:
        root.after(0, lambda: text_blocksPlaced.config(text=msg, fg=color))
    return

def gui_show_zeus():
    global root, zeus_image
    if root and zeus_image:
        root.after(0, lambda: zeus_image.pack(expand=True, fill=tk.BOTH))
    return

def gui_hide_zeus():
    global root, zeus_image
    if root and zeus_image:
        root.after(0, lambda: zeus_image.pack_forget())
    return

def gui_quit():
    global root
    if root:
        root.quit()
        root.destroy()
        
    os._exit(0)  # Force exit the program
    return