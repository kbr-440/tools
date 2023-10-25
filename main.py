import tkinter as tk
from recoverytool.gui.main_window import MainWindow

def main():
    # Create the main application window
    root = tk.Tk()
    root.title("Recovery Tool")
    app = MainWindow(master=root)
    app.pack(expand=True, fill='both')  # To make the app fill the entire root window
    root.geometry('450x400')

    # Main event loop for the GUI
    root.mainloop()

if __name__ == "__main__":
    main()
