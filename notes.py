import tkinter as tk
from tkinter import messagebox, simpledialog
import os
import json

# Define colors for light and dark mode
LIGHT_MODE = {
    'bg': 'white',
    'fg': 'black',
    'button_bg': 'lightgray',
    'button_fg': 'black'
}

DARK_MODE = {
    'bg': '#2E2E2E',
    'fg': 'white',
    'button_bg': '#444444',
    'button_fg': 'white'
}

CONFIG_FILE = "config.json"  # Configuration file for saving settings


class SimpleNoteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Note-Taking App")
        self.root.geometry("800x600")

        # Initialize theme and notes data
        self.notes_data = {}
        self.notes_file = "notes.json"

        # Load theme from config or use default
        self.current_mode = self.load_theme()

        # UI Components
        self.setup_ui()

        # Load notes after UI is initialized
        self.load_notes()

        # Start autosave
        self.autosave()

    def setup_ui(self):
        """Setup the user interface."""
        # Frames for layout
        self.notes_frame = tk.Frame(self.root, width=200, bg=self.current_mode['bg'])
        self.notes_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.editor_frame = tk.Frame(self.root, bg=self.current_mode['bg'])
        self.editor_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

        # Notes listbox
        self.notes_listbox = tk.Listbox(self.notes_frame, bg=self.current_mode['bg'], fg=self.current_mode['fg'])
        self.notes_listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.notes_listbox.bind("<<ListboxSelect>>", self.load_selected_note)

        # Buttons for note management
        self.add_note_button = tk.Button(self.notes_frame, text="Add Note", command=self.add_note,
                                         bg=self.current_mode['button_bg'], fg=self.current_mode['button_fg'])
        self.add_note_button.pack(side=tk.TOP, fill=tk.X, padx=5, pady=2)

        self.rename_note_button = tk.Button(self.notes_frame, text="Rename Note", command=self.rename_note,
                                            bg=self.current_mode['button_bg'], fg=self.current_mode['button_fg'])
        self.rename_note_button.pack(side=tk.TOP, fill=tk.X, padx=5, pady=2)

        self.delete_note_button = tk.Button(self.notes_frame, text="Delete Note", command=self.delete_note,
                                            bg=self.current_mode['button_bg'], fg=self.current_mode['button_fg'])
        self.delete_note_button.pack(side=tk.TOP, fill=tk.X, padx=5, pady=2)

        # Dark Mode Toggle Button
        self.toggle_dark_mode_button = tk.Button(self.root, text="Toggle Dark Mode", command=self.toggle_dark_mode,
                                                 bg=self.current_mode['button_bg'], fg=self.current_mode['button_fg'])
        self.toggle_dark_mode_button.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)

        # Text editor
        self.text_editor = tk.Text(self.editor_frame, wrap=tk.WORD, bg=self.current_mode['bg'], fg=self.current_mode['fg'])
        self.text_editor.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)
        self.text_editor.bind("<KeyRelease>", self.mark_dirty)

        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = tk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor="w",
                                   bg=self.current_mode['bg'], fg=self.current_mode['fg'])
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def load_notes(self):
        """Load notes from a JSON file if it exists."""
        if os.path.exists(self.notes_file):
            with open(self.notes_file, "r") as file:
                self.notes_data = json.load(file)
        else:
            self.notes_data = {}
        self.refresh_notes_list()

    def save_notes(self):
        """Save notes to a JSON file."""
        with open(self.notes_file, "w") as file:
            json.dump(self.notes_data, file, indent=4)

    def refresh_notes_list(self):
        """Refresh the notes listbox."""
        self.notes_listbox.delete(0, tk.END)
        for note_name in self.notes_data:
            self.notes_listbox.insert(tk.END, note_name)

    def add_note(self):
        """Add a new note."""
        note_name = simpledialog.askstring("New Note", "Enter the name for the new note:")
        if not note_name:
            messagebox.showerror("Error", "Note name cannot be empty.")
            return
        if note_name in self.notes_data:
            messagebox.showerror("Error", "A note with this name already exists.")
            return
        self.notes_data[note_name] = ""
        self.refresh_notes_list()
        self.notes_listbox.select_set(tk.END)
        self.load_selected_note()

    def rename_note(self):
        """Rename the selected note."""
        selected_index = self.notes_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "Please select a note to rename.")
            return
        old_name = self.notes_listbox.get(selected_index)
        new_name = simpledialog.askstring("Rename Note", f"Enter a new name for '{old_name}':")
        if not new_name:
            messagebox.showerror("Error", "Note name cannot be empty.")
            return
        if new_name in self.notes_data:
            messagebox.showerror("Error", "A note with this name already exists.")
            return
        # Update the note name in the data
        self.notes_data[new_name] = self.notes_data.pop(old_name)
        self.refresh_notes_list()
        self.notes_listbox.select_set(selected_index)
        self.status_var.set(f"Renamed '{old_name}' to '{new_name}'.")

    def delete_note(self):
        """Delete the selected note."""
        selected_index = self.notes_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "Please select a note to delete.")
            return
        note_name = self.notes_listbox.get(selected_index)
        del self.notes_data[note_name]
        self.refresh_notes_list()
        self.text_editor.delete("1.0", tk.END)

    def load_selected_note(self, event=None):
        """Load the selected note into the editor."""
        selected_index = self.notes_listbox.curselection()
        if not selected_index:
            return
        note_name = self.notes_listbox.get(selected_index)
        self.text_editor.delete("1.0", tk.END)
        self.text_editor.insert(tk.END, self.notes_data[note_name])

    def mark_dirty(self, event=None):
        """Mark the current note as dirty (modified)."""
        selected_index = self.notes_listbox.curselection()
        if selected_index:
            note_name = self.notes_listbox.get(selected_index)
            self.notes_data[note_name] = self.text_editor.get("1.0", tk.END)
            self.status_var.set("Unsaved changes")

    def toggle_dark_mode(self):
        """Toggle between light and dark mode."""
        self.current_mode = DARK_MODE if self.current_mode == LIGHT_MODE else LIGHT_MODE
        self.save_theme()  # Save the selected theme
        self.apply_theme()

    def apply_theme(self):
        """Apply the selected theme (light or dark)."""
        self.root.config(bg=self.current_mode['bg'])
        self.notes_frame.config(bg=self.current_mode['bg'])
        self.editor_frame.config(bg=self.current_mode['bg'])
        self.notes_listbox.config(bg=self.current_mode['bg'], fg=self.current_mode['fg'])
        self.text_editor.config(bg=self.current_mode['bg'], fg=self.current_mode['fg'])
        self.status_bar.config(bg=self.current_mode['bg'], fg=self.current_mode['fg'])
        self.add_note_button.config(bg=self.current_mode['button_bg'], fg=self.current_mode['button_fg'])
        self.rename_note_button.config(bg=self.current_mode['button_bg'], fg=self.current_mode['button_fg'])
        self.delete_note_button.config(bg=self.current_mode['button_bg'], fg=self.current_mode['button_fg'])
        self.toggle_dark_mode_button.config(bg=self.current_mode['button_bg'], fg=self.current_mode['button_fg'])

    def load_theme(self):
        """Load the theme preference from the config file."""
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as file:
                config = json.load(file)
                return DARK_MODE if config.get("theme") == "dark" else LIGHT_MODE
        return LIGHT_MODE  # Default to light mode if no config exists

    def save_theme(self):
        """Save the current theme to the config file."""
        config = {"theme": "dark" if self.current_mode == DARK_MODE else "light"}
        with open(CONFIG_FILE, "w") as file:
            json.dump(config, file)

    def autosave(self):
        """Automatically save the notes every few seconds."""
        self.save_notes()
        self.root.after(5000, self.autosave)  # Autosave every 5 seconds


if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleNoteApp(root)
    root.mainloop()
