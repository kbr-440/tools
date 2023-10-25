import os
import tkinter as tk
from tkinter import filedialog, ttk, simpledialog, font
from recoverytool import core
from recoverytool import errors


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        # Fonts and Styles
        self.main_font = font.Font(family='Arial', size=12)
        self.error_font = font.Font(family='Arial', size=10, weight='bold')

        # Styles for ttk widgets
        self.style = ttk.Style()
        self.style.configure("TLabel", font=self.main_font)
        self.style.configure("TButton", font=self.main_font)

        # Main Window Configuration
        self.title("Recovery Tool")
        self.geometry("600x450")
        self.configure(bg='#2e2e2e')  # Dark background color
        self.create_widgets()

    def create_widgets(self):
        # Frame for selecting the image
        image_frame = ttk.Frame(self)
        image_frame.grid(row=0, column=0, padx=20, pady=20, sticky='w')

        # Disk Image Widgets
        ttk.Label(image_frame, text="Select Disk Image:").grid(row=0, column=0, padx=5, pady=5)
        self.browse_button = ttk.Button(image_frame, text="Browse", command=self.browse_disk_image)
        self.browse_button.grid(row=0, column=1, padx=5, pady=5)
        self.file_label = ttk.Label(image_frame, text="No file selected", wraplength=300)
        self.file_label.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        # Frame for output directory
        output_frame = ttk.Frame(self)
        output_frame.grid(row=1, column=0, padx=20, pady=20, sticky='w')

        # Output Directory Widgets
        ttk.Label(output_frame, text="Output Directory:").grid(row=0, column=0, padx=5, pady=5)
        self.output_dir_button = ttk.Button(output_frame, text="Choose", command=self.choose_output_dir)
        self.output_dir_button.grid(row=0, column=1, padx=5, pady=5)
        self.selected_output_dir_label = ttk.Label(output_frame, text="Default: ./recovered")
        self.selected_output_dir_label.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        # Options and Recovery Button
        self.recover_all_var = tk.IntVar()
        self.recover_all_checkbutton = tk.Checkbutton(self, text="Recover all files", variable=self.recover_all_var,
                                                      bg='#2e2e2e', fg='white')
        self.recover_all_checkbutton.grid(row=2, column=0, padx=20, pady=10, sticky='w')
        self.recover_button = ttk.Button(self, text="Recover", command=self.recover_files)
        self.recover_button.grid(row=2, column=0, padx=20, pady=10, sticky='e')

        # Error message display
        self.error_text = tk.Text(self, height=3, width=50, wrap=tk.WORD, fg='red', bg='#2e2e2e', borderwidth=0)
        self.error_text.grid(row=3, column=0, padx=20, pady=10, sticky='w')
        self.error_text.config(state=tk.DISABLED)

        # Applying Fonts
        for child in self.winfo_children():
            widget_type = child.winfo_class()
            if widget_type in ("Label", "Checkbutton", "Text", "Button"):
                child.configure(font=self.main_font)
            elif isinstance(child, tk.Text):
                child.configure(font=self.error_font)


    def browse_disk_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image_path = file_path
            self.file_label.config(text=os.path.basename(file_path))
            self.error_label.config(text="")  # Clear any previous errors

    def choose_output_dir(self):
        dir_path = filedialog.askdirectory()
        if dir_path:
            self.output_dir = dir_path
            self.selected_output_dir_label.config(text=dir_path)

    def clear_error_text(self):
        self.error_text.config(state=tk.NORMAL)  # Enable editing
        self.error_text.delete("1.0", tk.END)  # Clear text
        self.error_text.config(state=tk.DISABLED)  # Disable editing

    def set_error_text(self, message):
        self.error_text.config(state=tk.NORMAL)  # Enable editing
        self.error_text.insert(tk.END, message)  # Insert message
        self.error_text.config(state=tk.DISABLED)  # Disable editing

    def recover_files(self):
        # Clear the error text at the start
        self.clear_error_text()

        if hasattr(self, 'image_path'):
            # Determine which files to recover based on user's choice:
            files_to_recover = core.DiskRecoveryTool(self.image_path).scan_files(recover_all=self.recover_all_var.get())

            # Optional: You can check the length of `files_to_recover` and display some messages.
            if not files_to_recover:
                self.set_error_text("No files found for recovery.")
                return

            output_path = getattr(self, 'output_dir', './recovered')

            # Create an instance of your recovery tool
            recovery_tool = core.DiskRecoveryTool(self.image_path, output_path)

            # Recover each file
            for file_entry in files_to_recover:
                recovery_tool.recover_file(file_entry)

            self.set_error_text("Files recovered successfully!")
        else:
            self.set_error_text("Please select a disk image before attempting recovery.")


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
