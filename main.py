import tkinter as tk
from tkinter import filedialog, messagebox
import os
import subprocess

def select_directory():
    global conversation_path, message_path  # Global variables to store file paths

    folder_selected = filedialog.askdirectory()
    if folder_selected:
        # Look for 'conversation.json' and 'message.json' in the selected directory and its subdirectories
        conversation_path = find_file(folder_selected, 'conversation.json')
        message_path = find_file(folder_selected, 'message.json')
        
        if not conversation_path:
            messagebox.showerror("Error", "conversation.json not found in the selected directory or its subdirectories.")
            return
        if not message_path:
            messagebox.showerror("Error", "message.json not found in the selected directory or its subdirectories.")
            return

def find_file(start_dir, file_name):
    for root, dirs, files in os.walk(start_dir):
        if file_name in files:
            return os.path.join(root, file_name)
    return None

def run_plot():
    if not (conversation_path and message_path):
        messagebox.showerror("Error", "No directory selected or paths not found.")
        return

    plot_type = plot_selection.get()
    if plot_type:
        if plot_type == "All Encompassing Plot":
            subprocess.run(['python', 'allEncompassingPlot.py', conversation_path, message_path])
        elif plot_type == "Average Likes Per Post":
            subprocess.run(['python', 'avgLikesPerPost.py', conversation_path, message_path])
        elif plot_type == "Specific Stats":
            subprocess.run(['python', 'specificStats.py', conversation_path, message_path])
        else:
            messagebox.showerror("Error", "u gotta select a plot. try again")
    else:
        messagebox.showerror("Error", "how abt u select a plot this time. u do ur job i'll do mine.")

def create_gui():
    global plot_selection, conversation_path, message_path
    
    # Initialize paths
    conversation_path = None
    message_path = None
    
    root = tk.Tk()
    root.title("ha made u look (and widen the window jeeeeeez im in your head)                               ok stop. you went too far")
    
    tk.Label(root, text="Select the Unzipped Export GroupMe Folder (should be a bunch of numbers or smtn)", padx=50, pady=10).pack(pady=10)
    
    tk.Button(root, text="Browse", command=select_directory, padx=50, pady=15).pack(pady=5)
    
    tk.Label(root, text="Select Plot Type", padx=50, pady=20).pack(pady=10)
    plot_selection = tk.StringVar(value="All Encompassing Plot")  # Default selection
    plot_options = ["All Encompassing Plot", "Average Likes Per Post", "Specific Stats"]
    for option in plot_options:
        tk.Radiobutton(root, text=option, variable=plot_selection, value=option, padx=10, pady=5).pack(anchor='w')
    
    tk.Button(root, text="Run Plot", command=run_plot, padx=10, pady=5).pack(pady=20)
    
    root.mainloop()

if __name__ == "__main__":
    create_gui()
