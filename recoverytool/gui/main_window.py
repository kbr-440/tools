# gui/main_window.py

import tkinter as tk
from tkinter import filedialog
from recoverytool import core


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Recovery Tool")

        # Create and place widgets
        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self, text="Select Disk Image")
        self.label.pack(pady=20)

        self.browse_button = tk.Button(self, text="Browse", command=self.browse_disk_image)
        self.browse_button.pack(pady=20)

        self.recover_button = tk.Button(self, text="Recover", command=self.recover_files)
        self.recover_button.pack(pady=20)

    def browse_disk_image(self):
        file_path = filedialog.askopenfilename()
        # Store file path and do additional stuff if necessary
        self.image_path = file_path

    def recover_files(self):
        if hasattr(self, 'image_path'):
            deleted_files = core.scan_disk_for_deleted_files(self.image_path, 'NTFS')  # Example for NTFS
            recovered_files = core.carve_files(deleted_files)
            core.save_recovered_files(recovered_files, "output_directory")  # Specify your output directory


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
