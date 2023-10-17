# future home of tkinter
import pickle
import tkinter as tk
from tkinter import filedialog
from . import main
# save and load gui state


def save_state():
    state = {
        "base_xml_path": base_xml_entry.get(),
        "reference_xml_path": reference_xml_entry.get(),
        "reference_name": reference_name_entry.get(),
        "output_dir_path": output_dir_entry.get(),
        "output_name": output_name_entry.get()
    }

    with open("app_state.pkl", "wb") as f:
        pickle.dump(state, f)


def load_state():
    try:
        with open("app_state.pkl", "rb") as f:
            state = pickle.load(f)
            base_xml_entry.insert(0, state["base_xml_path"])
            reference_xml_entry.insert(0, state["reference_xml_path"])
            reference_name_entry.insert(0, state["reference_name"])
            output_dir_entry.insert(0, state["output_dir_path"])
            output_name_entry.insert(0, state["output_name"])
    except FileNotFoundError:
        pass


def browse_file(entry):
    file_path = filedialog.askopenfilename()
    entry.delete(0, tk.END)
    entry.insert(0, file_path)


def browse_directory(entry):
    dir_path = filedialog.askdirectory()
    entry.delete(0, tk.END)
    entry.insert(0, dir_path)


root = tk.Tk()

root.title("XML Processing")

# Create and pack labels and entry fields


tk.Label(root, text="Base XML Path:").pack()
base_xml_entry = tk.Entry(root)
base_xml_entry.pack()
tk.Button(root, text="Browse",
          command=lambda: browse_file(base_xml_entry)).pack()

tk.Label(root, text="Reference XML Path:").pack()
reference_xml_entry = tk.Entry(root)
reference_xml_entry.pack()
tk.Button(root, text="Browse", command=lambda: browse_file(
    reference_xml_entry)).pack()

tk.Label(root, text="Reference Name:").pack()
reference_name_entry = tk.Entry(root)
reference_name_entry.pack()

tk.Label(root, text="Output Directory Path:").pack()
output_dir_entry = tk.Entry(root)
output_dir_entry.pack()
tk.Button(root, text="Browse", command=lambda: browse_directory(
    output_dir_entry)).pack()

# Adding the "Output Name" section
tk.Label(root, text="Output Name:").pack()
output_name_entry = tk.Entry(root)
output_name_entry.pack()


# Create and pack the "Generate XML" button
generate_button = tk.Button(root, text="Generate XML", command=main.generate_xml)
generate_button.pack()

load_state()
root.protocol("WM_DELETE_WINDOW", lambda: [save_state(), root.quit()])

# Run the GUI
root.mainloop()
