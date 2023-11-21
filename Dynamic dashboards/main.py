import tkinter as tk
from tkinter import ttk
from upload_frame import UploadFrame

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Dynamic Dashboards")

        self.upload_frame = UploadFrame(self)
        self.upload_frame.pack(pady=20)

    def run(self):
        self.mainloop()

if __name__ == "__main__":
    app = MainApp()
    app.run()
