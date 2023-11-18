import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt

# Global variables
data = None
x_column = None
y_column = None
legend_column = None
graph_type = None
page_stack = []

# Function to load data from Excel or CSV file
def load_data():
    global data
    file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx *.xls"), ("CSV Files", "*.csv")])
    if file_path:
        try:
            if file_path.endswith('.csv'):
                data = pd.read_csv(file_path)
            else:
                data = pd.read_excel(file_path)
            messagebox.showinfo("Success", "Data loaded successfully!")
            show_graph_options()
        except Exception as e:
            messagebox.showerror("Error", f"Error loading data: {str(e)}")

# Function to show graph type selection page
def show_graph_options():
    upload_frame.pack_forget()
    page_stack.append(upload_frame)
    graph_type_frame.pack()
    
# Function to select graph type
def select_graph_type():
    global graph_type
    graph_type = graph_type_var.get()
    if graph_type == "Histogram":
        show_legend_input()
    else:
        show_axis_options()

# Function to show axis selection page
def show_axis_options():
    graph_type_frame.pack_forget()
    page_stack.append(graph_type_frame)
    axis_frame.pack()

# Function to show legend input page
def show_legend_input():
    graph_type_frame.pack_forget()
    page_stack.append(graph_type_frame)
    legend_frame.pack()

# Function to set X and Y axes
def set_axes():
    global x_column, y_column
    x_column = x_column_entry.get()
    y_column = y_column_entry.get()
    analyze_data()

# Function to set legend and create the graph
def set_legend_and_analyze():
    global legend_column
    legend_column = legend_column_entry.get()
    analyze_data()

# Function to create and display the graph
def analyze_data():
    if graph_type == "Bar Graph":
        create_bar_graph()
    elif graph_type == "Line Graph":
        create_line_graph()
    elif graph_type == "Histogram":
        create_histogram()

# Function to create a bar graph
def create_bar_graph():
    plt.figure(figsize=(8, 6))
    plt.title("Bar Graph")
    plt.xlabel(x_column)
    plt.ylabel(y_column)
    plt.bar(data[x_column], data[y_column])
    plt.show()

# Function to create a line graph
def create_line_graph():
    plt.figure(figsize=(8, 6))
    plt.title("Line Graph")
    plt.xlabel(x_column)
    plt.ylabel(y_column)
    plt.plot(data[x_column], data[y_column])
    plt.show()

# Function to create a histogram
def create_histogram():
    plt.figure(figsize=(8, 6))
    plt.title("Histogram")
    plt.hist(data[legend_column], bins=10, edgecolor='k')
    plt.show()

# Create the main application window
root = tk.Tk()
root.title("Dynamic Dashboards")  # Set title bar text to "Dynamic Dashboards"

# Set the font for the entire application to "Century Schoolbook"
font = ("Century Schoolbook", 12)
root.option_add("*TButton*Font", font)
root.option_add("*TLabel*Font", font)
root.option_add("*TEntry*Font", font)
root.option_add("*TCombobox*Font", font)

# Create the frame for uploading data (Excel or CSV)
upload_frame = ttk.Frame(root)
ttk.Label(upload_frame, text="Upload Data File (Excel or CSV)").pack()
upload_button = ttk.Button(upload_frame, text="Upload", command=load_data)
upload_button.pack()
upload_frame.pack(pady=20)

# Create the frame for selecting graph type
graph_type_frame = ttk.Frame(root)
ttk.Label(graph_type_frame, text="Select Graph Type").pack()
graph_type_var = tk.StringVar()
graph_type_var.set("Bar Graph")
graph_type_dropdown = ttk.Combobox(graph_type_frame, textvariable=graph_type_var, values=["Bar Graph", "Line Graph", "Histogram"])
graph_type_dropdown.pack()
graph_type_button = ttk.Button(graph_type_frame, text="Next", command=select_graph_type)
graph_type_button.pack()

# Create the frame for selecting X and Y axes
axis_frame = ttk.Frame(root)
ttk.Label(axis_frame, text="Select X and Y Axes").pack()
ttk.Label(axis_frame, text="X-Axis").pack()
x_column_entry = ttk.Entry(axis_frame)
x_column_entry.pack()
ttk.Label(axis_frame, text="Y-Axis").pack()
y_column_entry = ttk.Entry(axis_frame)
y_column_entry.pack()
axis_button = ttk.Button(axis_frame, text="Analyze", command=set_axes)
axis_button.pack()

# Create the frame for entering the legend column name
legend_frame = ttk.Frame(root)
ttk.Label(legend_frame, text="Enter Legend Column Name").pack()
legend_column_entry = ttk.Entry(legend_frame)
legend_column_entry.pack()
legend_button = ttk.Button(legend_frame, text="Analyze", command=set_legend_and_analyze)
legend_button.pack()

# Center the main window on the screen
window_width = 800
window_height = 600
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

root.mainloop()
