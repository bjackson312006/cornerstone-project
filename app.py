import serial
import tkinter as tk

# CONFIG
port = 'COM9'  # Port connected to Arduino.

# Initialize serial connection
ser = serial.Serial(port, 9600, timeout=1)

# Function to parse line and extract id and data
def parse(line):
    try:
        id, data = line.split(':')
        id = id.strip()
        return id, data
    except ValueError:
        return None, None

# Update function to read data from serial and update GUI labels
def update_labels():
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()
        id, data = parse(line)
        if id in labels:
            labels[id].config(text=f"{id}: {data}")
    root.after(100, update_labels)  # Schedule the next update

# Initialize GUI
root = tk.Tk()
root.title("Sensor Monitor")

# Create a dictionary to hold label references
labels = {
    'A0': tk.Label(root, text="A0: None"),
    'A1': tk.Label(root, text="A1: None"),
    'A2': tk.Label(root, text="A2: None"),
    'A3': tk.Label(root, text="A3: None"),
}

# Pack the labels into the window
for label in labels.values():
    label.pack()

try:
    update_labels()  # Start the update loop
    root.mainloop()  # Start the Tkinter main loop
except KeyboardInterrupt:
    print("Exiting program.")
finally:
    ser.close()  # Ensure the serial connection is closed