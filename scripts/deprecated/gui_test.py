import tkinter as tk
from encode_decode import decode

password = "test"

def on_button_click():
    entered_password = get_entry_value()
    if entered_password == password:
        label.config(text="Correct")
        decode()  # This will only be called when the password is correct
    else:
        label.config(text="Incorrect")

def get_entry_value():
    # Get the value from the Entry widget
    entry_value = entry_var.get()
    return entry_value

# Create the main window
window = tk.Tk()
window.title("Simple GUI")

# Create widgets
label = tk.Label(window, text="Enter a password:")
entry_var = tk.StringVar()
entry = tk.Entry(window, textvariable=entry_var)
button = tk.Button(window, text="Submit", command=on_button_click)

# Place widgets in the window
label.pack()
entry.pack()
button.pack()

# Start the main loop
window.mainloop()
