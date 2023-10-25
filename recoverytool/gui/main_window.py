import os
import tkinter as tk
from tkinter import filedialog, ttk
from recoverytool import core
from recoverytool import errors


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

        # Error message label
        self.error_text = tk.Text(self, height=3, width=40, wrap=tk.WORD, fg='red', bg='light gray', borderwidth=0)
        self.error_text.grid(row=2, column=1, pady=10, padx=20, sticky='w')
        self.error_text.config(state=tk.DISABLED)  # Disable editing

        self.recover_button = ttk.Button(self, text="Recover", command=self.recover_files)
        self.recover_button.grid(row=3, column=0, pady=20, padx=20, sticky='w')

        # Create an error_label widget
        self.error_label = ttk.Label(self, text="", background='light gray', foreground='red')
        self.error_label.grid(row=3, column=1, pady=10, padx=20, sticky='w')

    def browse_disk_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image_path = file_path
            self.file_label.config(text=os.path.basename(file_path))
            self.error_label.config(text="")  # Clear any previous errors

    def clear_error_text(self):
        self.error_text.config(state=tk.NORMAL)  # Enable editing
        self.error_text.delete("1.0", tk.END)  # Clear text
        self.error_text.config(state=tk.DISABLED)  # Disable editing

    def set_error_text(self, message):
        self.error_text.config(state=tk.NORMAL)  # Enable editing
        self.error_text.insert(tk.END, message)  # Insert message
        self.error_text.config(state=tk.DISABLED)  # Disable editing

    def recover_files(self):
        if hasattr(self, 'image_path'):
            try:
                result = core.scan_disk_for_deleted_files(self.image_path)
                core.carve_files_from_disk(self.image_path, "output_directory")
                self.set_error_text("Files recovered successfully!")
            except errors.DiskRecoveryError as e:  # Catch any error derived from DiskRecoveryError
                self.set_error_text(str(e))
        else:
            self.set_error_text("Please select a disk image before attempting recovery.")


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
