import json
import os
import tkinter as tk
from tkinter import messagebox

# Path to the JSON file where data will be saved
data_file = 'notebooks_data.json'

# Initialize the notebooks data structure if it doesn't exist
if not os.path.exists(data_file):
    with open(data_file, 'w') as f:
        json.dump({"notebooks": []}, f, indent=4)

# Function to load data from the JSON file
def load_data():
    with open(data_file, 'r') as f:
        return json.load(f)

# Function to save data back to the JSON file
def save_data(data):
    with open(data_file, 'w') as f:
        json.dump(data, f, indent=4)

# Function to create a new notebook
def create_notebook(name):
    data = load_data()
    notebook = {"name": name, "text": "", "sub_notes": []}
    data['notebooks'].append(notebook)
    save_data(data)

# Function to create a new sub-note
def create_subnote(notebook_name, subnote_name, text):
    data = load_data()
    for notebook in data['notebooks']:
        if notebook['name'] == notebook_name:
            subnote = {"name": subnote_name, "text": text}
            notebook['sub_notes'].append(subnote)
            save_data(data)
            return
    raise ValueError(f'Notebook "{notebook_name}" not found.')

# Function to delete a notebook
def delete_notebook(notebook_name):
    data = load_data()
    for notebook in data['notebooks']:
        if notebook['name'] == notebook_name:
            data['notebooks'].remove(notebook)
            save_data(data)
            return
    raise ValueError(f'Notebook "{notebook_name}" not found.')

# Function to delete a sub-note
def delete_subnote(notebook_name, subnote_name):
    data = load_data()
    for notebook in data['notebooks']:
        if notebook['name'] == notebook_name:
            for subnote in notebook['sub_notes']:
                if subnote['name'] == subnote_name:
                    notebook['sub_notes'].remove(subnote)
                    save_data(data)
                    return
    raise ValueError(f'Sub-note "{subnote_name}" not found in notebook "{notebook_name}".')

# Function to load notebooks and display in the listbox
def load_notebooks():
    data = load_data()
    notebooks = [notebook['name'] for notebook in data['notebooks']]
    return notebooks

# Function to load sub-notes and display in the listbox
def load_subnotes(notebook_name):
    data = load_data()
    for notebook in data['notebooks']:
        if notebook['name'] == notebook_name:
            return [subnote['name'] for subnote in notebook['sub_notes']]
    return []

# Function to update the notebook listbox
def update_notebooks_list():
    notebooks = load_notebooks()
    notebook_listbox.delete(0, tk.END)
    for notebook in notebooks:
        notebook_listbox.insert(tk.END, notebook)

# Function to update the sub-note listbox
def update_subnotes_list(notebook_name):
    subnotes = load_subnotes(notebook_name)
    subnote_listbox.delete(0, tk.END)
    for subnote in subnotes:
        subnote_listbox.insert(tk.END, subnote)

# Function to handle creating a new notebook from the UI
def add_notebook():
    notebook_name = notebook_entry.get()
    if notebook_name:
        create_notebook(notebook_name)
        notebook_entry.delete(0, tk.END)
        update_notebooks_list()
    else:
        messagebox.showwarning("Input Error", "Please enter a notebook name.")

# Function to handle adding a sub-note from the UI
def add_subnote():
    notebook_name = notebook_listbox.get(tk.ACTIVE)
    subnote_name = subnote_entry.get()
    text = subnote_text.get("1.0", tk.END).strip()
    if notebook_name and subnote_name and text:
        try:
            create_subnote(notebook_name, subnote_name, text)
            subnote_entry.delete(0, tk.END)
            subnote_text.delete("1.0", tk.END)
            update_subnotes_list(notebook_name)
        except ValueError as e:
            messagebox.showerror("Error", str(e))
    else:
        messagebox.showwarning("Input Error", "Please fill in all fields.")

# Function to handle deleting a selected notebook
def delete_notebook_ui():
    notebook_name = notebook_listbox.get(tk.ACTIVE)
    if notebook_name:
        try:
            delete_notebook(notebook_name)
            update_notebooks_list()
            subnote_listbox.delete(0, tk.END)
        except ValueError as e:
            messagebox.showerror("Error", str(e))
    else:
        messagebox.showwarning("Selection Error", "Please select a notebook to delete.")

# Function to handle deleting a selected sub-note
def delete_subnote_ui():
    notebook_name = notebook_listbox.get(tk.ACTIVE)
    subnote_name = subnote_listbox.get(tk.ACTIVE)
    if notebook_name and subnote_name:
        try:
            delete_subnote(notebook_name, subnote_name)
            update_subnotes_list(notebook_name)
        except ValueError as e:
            messagebox.showerror("Error", str(e))
    else:
        messagebox.showwarning("Selection Error", "Please select a sub-note to delete.")

# Function to edit the text of a notebook
def edit_notebook_text():
    notebook_name = notebook_listbox.get(tk.ACTIVE)
    new_text = notebook_text.get("1.0", tk.END).strip()
    if notebook_name and new_text:
        data = load_data()
        for notebook in data['notebooks']:
            if notebook['name'] == notebook_name:
                notebook['text'] = new_text
                save_data(data)
                notebook_text.delete("1.0", tk.END)
                messagebox.showinfo("Success", f"Notebook '{notebook_name}' updated.")
                return
        messagebox.showerror("Error", "Notebook not found.")
    else:
        messagebox.showwarning("Input Error", "Please select a notebook and enter text.")

# Function to edit the text of a sub-note
def edit_subnote_text():
    notebook_name = notebook_listbox.get(tk.ACTIVE)
    subnote_name = subnote_listbox.get(tk.ACTIVE)
    new_text = subnote_text.get("1.0", tk.END).strip()
    if notebook_name and subnote_name and new_text:
        data = load_data()
        for notebook in data['notebooks']:
            if notebook['name'] == notebook_name:
                for subnote in notebook['sub_notes']:
                    if subnote['name'] == subnote_name:
                        subnote['text'] = new_text
                        save_data(data)
                        subnote_text.delete("1.0", tk.END)
                        messagebox.showinfo("Success", f"Sub-note '{subnote_name}' updated.")
                        return
        messagebox.showerror("Error", "Sub-note not found.")
    else:
        messagebox.showwarning("Input Error", "Please select a sub-note and enter text.")

# Set up the Tkinter window
root = tk.Tk()
root.title("Note-taking App")

# Set up frames for layout
frame_notebook = tk.Frame(root)
frame_notebook.pack(padx=10, pady=10, fill='x')

frame_subnote = tk.Frame(root)
frame_subnote.pack(padx=10, pady=10, fill='x')

# Notebook management section
notebook_label = tk.Label(frame_notebook, text="Notebooks")
notebook_label.grid(row=0, column=0, sticky="w")

notebook_listbox = tk.Listbox(frame_notebook, height=5, width=30)
notebook_listbox.grid(row=1, column=0, padx=5)

notebook_entry = tk.Entry(frame_notebook, width=25)
notebook_entry.grid(row=2, column=0, padx=5)

add_notebook_button = tk.Button(frame_notebook, text="Add Notebook", command=add_notebook)
add_notebook_button.grid(row=3, column=0, pady=5)

delete_notebook_button = tk.Button(frame_notebook, text="Delete Notebook", command=delete_notebook_ui)
delete_notebook_button.grid(row=4, column=0, pady=5)

notebook_text = tk.Text(frame_notebook, height=4, width=30)
notebook_text.grid(row=5, column=0, padx=5)

edit_notebook_button = tk.Button(frame_notebook, text="Edit Notebook", command=edit_notebook_text)
edit_notebook_button.grid(row=6, column=0, pady=5)

# Sub-note management section
subnote_label = tk.Label(frame_subnote, text="Sub-notes")
subnote_label.grid(row=0, column=0, sticky="w")

subnote_listbox = tk.Listbox(frame_subnote, height=5, width=30)
subnote_listbox.grid(row=1, column=0, padx=5)

subnote_entry = tk.Entry(frame_subnote, width=25)
subnote_entry.grid(row=2, column=0, padx=5)

subnote_text = tk.Text(frame_subnote, height=4, width=30)
subnote_text.grid(row=3, column=0, padx=5)

add_subnote_button = tk.Button(frame_subnote, text="Add Sub-note", command=add_subnote)
add_subnote_button.grid(row=4, column=0, pady=5)

delete_subnote_button = tk.Button(frame_subnote, text="Delete Sub-note", command=delete_subnote_ui)
delete_subnote_button.grid(row=5, column=0, pady=5)

edit_subnote_button = tk.Button(frame_subnote, text="Edit Sub-note", command=edit_subnote_text)
edit_subnote_button.grid(row=6, column=0, pady=5)

# Initial population of the notebook listbox
update_notebooks_list()

root.mainloop()
