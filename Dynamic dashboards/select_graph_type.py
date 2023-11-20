import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from axis_and_graph import AxisGraphFrame

class GraphTypeFrame(ttk.Frame):
    def __init__(self, master, data):  # Include 'data' as an argument
        super().__init__(master)
        self.data = data  # Store the received data

        ttk.Label(self, text="Select Graph Type").pack()
        self.graph_type_var = tk.StringVar()
        self.graph_type_var.set("Line Graph")
        self.graph_type_dropdown = ttk.Combobox(
            self,
            textvariable=self.graph_type_var,
            values=["Line Graph", "Bar Graph", "Histogram", "Boxplot", "Scatterplot", "3D Scatter", "Surface Plot", "Wireframe"]
        )
        self.graph_type_dropdown.pack()
        self.graph_type_button = ttk.Button(self, text="Next", command=self.select_graph_type)
        self.graph_type_button.pack()

    def select_graph_type(self):
        selected_graph = self.graph_type_var.get()

        if selected_graph in ["Line Graph", "Bar Graph","Scatterplot"]:
            self.master.main_frame = AxisGraphFrame(self.master, data=self.data,graph_type=selected_graph, has_x_axis=True, has_y_axis=True,has_z_axis=False)
        elif selected_graph in ["Histogram","Boxplot"]:
            self.master.main_frame = AxisGraphFrame(self.master,data=self.data, graph_type=selected_graph, has_x_axis=True, has_y_axis=False,has_z_axis=False)
        elif selected_graph in ["3D Scatter", "Surface Plot", "Wireframe"]:
            self.master.main_frame = AxisGraphFrame(self.master,data=self.data, graph_type=selected_graph, has_x_axis=True, has_y_axis=True,has_z_axis=True)
        self.pack_forget()
        self.master.main_frame.pack()

def main():
    root = tk.Tk()
    root.title("Graph Selection")
    root.configure(bg="#202020")
    root.geometry("900x300")
    graph_type_frame = GraphTypeFrame(root)
    graph_type_frame.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
