import file_printer
import file_reader

import tkinter as tk
from tkinter import filedialog


def open_file_dialog():
    # Create the file dialog
    file_path = filedialog.askopenfilename(title="Select a File", filetypes=[("CSV files", "*.csv")])

    # Display the selected file path
    if file_path:
        label.config(text=f"Selected File: {file_path}")
        selected_file.set(file_path)
    else:
        label.config(text="No file selected")
        selected_file.set("")


def process_selected_file():
    # Get the selected file path from the variable
    file_path = selected_file.get()

    # Process the selected file path (replace this with your own logic)
    if file_path:
        spells = file_reader.read_spells(file_path)
        file_printer.print_file(file_path, spells)
        root.destroy()
    else:
        print("No file selected")


# Create the main window
root = tk.Tk()
root.title("Spell Card Converter")

# Create a button to open the file dialog
button_open_dialog = tk.Button(root, text="Choose csv to convert", command=open_file_dialog)
button_open_dialog.pack(pady=10)

# Create a label to display the selected file path
label = tk.Label(root, text="No file selected", font=("Helvetica", 12))
label.pack()

# Variable to store the selected file path
selected_file = tk.StringVar()

# Create a button to process the selected file path
button_process_file = tk.Button(root, text="Convert Selected File", command=process_selected_file)
button_process_file.pack(pady=10)

# Run the main loop
root.mainloop()


