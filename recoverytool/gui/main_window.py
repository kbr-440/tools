import os
import tkinter as tk
from tkinter import filedialog, ttk, font
from recoverytool import core
from recoverytool import errors

class MainWindow(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.configure(bg='#2e2e2e')  # Dark background color

        # Fonts and Styles
        self.title_font = font.Font(family='Arial', size=16, weight='bold')
        self.main_font = font.Font(family='Arial', size=12)
        self.error_font = font.Font(family='Arial', size=10, weight='bold')

        # Styles for ttk widgets
        self.style = ttk.Style()
        self.style.configure("TLabel", font=self.main_font, background='#2e2e2e', foreground='white')
        self.style.configure("TButton", font=self.main_font)
        self.style.configure("TFrame", background='#2e2e2e')

        self.center_window()  # Center the window
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self, text="Recovery Tool", font=self.title_font, foreground='#00BFFF').grid(row=0, column=0, pady=(0, 20))

        # Disk Image Selection
        image_frame = ttk.Frame(self)
        image_frame.grid(row=1, column=0, padx=10, pady=10, sticky='w')

        ttk.Label(image_frame, text="Select Disk Image:").grid(row=0, column=0, padx=10, pady=5)
        self.browse_button = ttk.Button(image_frame, text="Browse", command=self.browse_disk_image)
        self.browse_button.grid(row=0, column=1, padx=10, pady=5)
        self.file_label = ttk.Label(image_frame, text="No file selected", wraplength=400)
        self.file_label.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

        # Output Directory Selection
        output_frame = ttk.Frame(self)
        output_frame.grid(row=2, column=0, padx=10, pady=10, sticky='w')

        ttk.Label(output_frame, text="Output Directory:").grid(row=0, column=0, padx=10, pady=5)
        self.output_dir_button = ttk.Button(output_frame, text="Choose", command=self.choose_output_dir)
        self.output_dir_button.grid(row=0, column=1, padx=10, pady=5)
        self.selected_output_dir_label = ttk.Label(output_frame, text="Default: ./recovered")
        self.selected_output_dir_label.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

        # Recovery Options
        self.recover_all_var = tk.IntVar()
        self.recover_all_checkbutton = ttk.Checkbutton(self, text="Recover all files", variable=self.recover_all_var)

        self.recover_all_checkbutton.grid(row=3, column=0, padx=10, pady=10, sticky='w')
        self.recover_button = ttk.Button(self, text="Recover", command=self.recover_files)
        self.recover_button.grid(row=3, column=0, padx=10, pady=10, sticky='e')

        # Error message display
        self.error_label = ttk.Label(self, text="", foreground='red', wraplength=500)
        self.error_label.grid(row=4, column=0, padx=10, pady=10, sticky='w')

    def center_window(self):
        # Center the window on the screen
        window_width = self.master.winfo_reqwidth()
        window_height = self.master.winfo_reqheight()
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        x_cordinate = int((screen_width / 2) - (window_width / 2))
        y_cordinate = int((screen_height / 2) - (window_height / 2))

        self.master.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

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
        self.error_label.config(text="")

    def set_error_text(self, message):
        self.error_label.config(text=message)

    def recover_files(self):
        self.clear_error_text()

        if hasattr(self, 'image_path'):
            recovery_tool = core.DiskRecoveryTool(self.image_path)
            files_to_recover = recovery_tool.scan_files(recover_all=self.recover_all_var.get())

            if not files_to_recover:
                self.set_error_text("No files found for recovery.")
                return

            output_path = getattr(self, 'output_dir', './recovered')
            recovery_tool.set_output_path(output_path)

            for file_entry in files_to_recover:
                recovery_tool.recover_file(file_entry)

            self.set_error_text("Files recovered successfully!")
        else:
            self.set_error_text("Please select a disk image before attempting recovery.")

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
