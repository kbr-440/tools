import os
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from recoverytool import core

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Recovery Tool")
        self.geometry("500x400")  # Set a default size
        self.configure(bg='light gray')  # Set the background color of the main window
        self.create_widgets()

    def create_widgets(self):
        self.label = ttk.Label(self, text="Select Disk Image", background='light gray')
        self.label.grid(row=0, column=0, pady=20, padx=20, sticky='w')

        self.browse_button = ttk.Button(self, text="Browse", command=self.browse_disk_image)
        self.browse_button.grid(row=1, column=0, pady=20, padx=20, sticky='w')

        # Display selected file name
        self.file_label = ttk.Label(self, text="No file selected", background='light gray')
        self.file_label.grid(row=1, column=1, pady=20, padx=20, sticky='w')

        self.recover_button = ttk.Button(self, text="Recover", command=self.recover_files)
        self.recover_button.grid(row=2, column=0, pady=20, padx=20, sticky='w')

    def browse_disk_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image_path = file_path
            self.file_label.config(text=os.path.basename(file_path))

    def recover_files(self):
        if hasattr(self, 'image_path'):
            try:
                deleted_files = core.scan_disk_for_deleted_files(self.image_path)
                core.carve_files_from_disk(self.image_path, "output_directory")
                messagebox.showinfo("Success", "Files recovered successfully!")
            except Exception as e:
                messagebox.showerror("Recovery Error", f"An error occurred: {str(e)}")
        else:
            messagebox.showerror("Error", "Please select a disk image before attempting recovery.")

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
