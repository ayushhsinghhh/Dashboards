import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk  # Import Image and ImageTk from PIL
import pandas as pd
from select_graph_type import GraphTypeFrame  # Assuming 'select_graph_type' contains GraphTypeFrame

class UploadFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        style = ttk.Style()
        style.configure("Custom.TButton", font=("Century Schoolbook", 12),foreground="purple", width=20)  # Adjust font and width as needed
        
        # Create content
        ttk.Label(self, text="Upload Data File (Excel or CSV)", font=("Century Gothic", 18),background="#202020",foreground="white").pack()
        self.upload_button = ttk.Button(self, text="Upload", command=self.load_data, style="Custom.TButton")
        self.upload_button.pack()

        # Load and display an image
        image = Image.open("D:\\Coding\\Dynamic dashboards\\upload.png")  # Replace with your image path
        #image = image.resize((300, 200))  # Resize the image if needed
        photo = ImageTk.PhotoImage(image)
        self.image_label = ttk.Label(self, image=photo)
        self.image_label.image = photo  # Keep a reference to avoid garbage collection
        self.image_label.pack()

    def load_data(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx *.xls"), ("CSV Files", "*.csv")])
        if file_path:
            try:
                if file_path.endswith('.csv'):
                    data = pd.read_csv(file_path)
                else:
                    data = pd.read_excel(file_path)
                messagebox.showinfo("Success", "Data loaded successfully!")
                # Pass the data to GraphTypeFrame
                self.master.main_frame = GraphTypeFrame(self.master, data=data)
                self.pack_forget()
                self.master.main_frame.pack()
            except Exception as e:
                messagebox.showerror("Error", f"Error loading data: {str(e)}")

# Test the frame
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Upload Frame Test")
    root.configure(bg="#202020")  # Set your preferred hexadecimal color code

    # Adjust the size of the root window
    root.geometry("900x300")  # Set your preferred window size here

    upload_frame = UploadFrame(root)
    upload_frame.pack()
    root.mainloop()
