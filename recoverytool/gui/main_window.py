import tkinter as tk
from tkinter import filedialog, messagebox
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
        if hasattr(self, 'image_path'):  # Check if 'image_path' attribute exists
            deleted_files = core.scan_disk_for_deleted_files(self.image_path)
        try:
            if hasattr(self, 'image_path'):
                deleted_files = core.scan_disk_for_deleted_files(self.image_pat) # Example for NTFS
                recovered_files = core.carve_files(deleted_files)
                core.save_recovered_files(recovered_files, "output_directory")  # Specify your output directory
        except Exception as e:
            # If there's an error, show it in a message box
            messagebox.showerror("Recovery Error", f"An error occurred: {str(e)}")
        else:
            # Handle the case where the image path has not been set.
            # Here, we'll display an error message in the GUI prompting the user to select an image.
            tk.messagebox.showerror("Error", "Please select a disk image before attempting recovery.")


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
