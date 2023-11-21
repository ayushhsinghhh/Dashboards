import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import matplotlib.pyplot as plt
import statistics

class AxisGraphFrame(ttk.Frame):
    def __init__(self, master, data, graph_type, has_x_axis=True, has_y_axis=True, has_z_axis=True):
        super().__init__(master)
        self.graph_type = graph_type
        self.has_x_axis = has_x_axis
        self.has_y_axis = has_y_axis
        self.has_z_axis = has_z_axis
        self.data = data  # Store the data frame
        master.geometry("400x400")  # Set the width and height as required
        
        ttk.Label(self, text="Select Axes for Graph").pack()

        ttk.Label(self, text="Select Graph Color").pack()
        colors = ["red", "green", "blue", "yellow", "orange", "purple",
                  "cyan", "magenta", "lime", "pink", "teal", "brown", "black"]
        self.selected_color = tk.StringVar()
        self.color_dropdown = ttk.Combobox(self, textvariable=self.selected_color, values=colors)
        self.color_dropdown.pack()

        self.alpha_frame = ttk.Frame(self)  # Frame to contain the alpha dropdown
        self.alpha_dropdown = None
        
        
        #legend checkbox
        self.display_legend_var = tk.BooleanVar()
        self.display_legend_var.set(False)
        self.legend_checkbox = ttk.Checkbutton(self, text="Display Legend", variable=self.display_legend_var, command=self.toggle_legend)
        self.legend_checkbox.pack()
        
        
        self.x_column_var = tk.StringVar()
        self.y_column_var = tk.StringVar()
        self.z_column_var = tk.StringVar()

        ttk.Label(self, text="X-Axis").pack()
        self.x_column_dropdown = ttk.Combobox(self, textvariable=self.x_column_var)
        self.x_column_dropdown.pack()

        self.add_grid_var = tk.BooleanVar()
        self.add_grid_var.set(False)
        self.add_grid_checkbox = ttk.Checkbutton(self, text="Add Grid", variable=self.add_grid_var, command=self.toggle_alpha_dropdown)
        self.add_grid_checkbox.pack()
        
        self.mean_display_frame = ttk.Frame(self)  # Frame to contain the mean display widgets
        self.mean_display_button = None
        self.mean_column_dropdown = None
        self.mean_line_style_frame = None
        self.mean_line_style_dropdown = None

        # Create a button for mean display on Bar Graph or Line Chart
        if self.graph_type in ["Bar Graph", "Line Graph"]:
            self.mean_display_button = ttk.Checkbutton(self, text="Display Mean", command=self.toggle_mean_display)
            self.mean_display_button.pack()

        if self.has_y_axis:
            ttk.Label(self, text="Y-Axis").pack()
            self.y_column_dropdown = ttk.Combobox(self, textvariable=self.y_column_var)
            self.y_column_dropdown.pack()
        
        if self.has_z_axis:
            ttk.Label(self, text="Z-Axis").pack()
            self.z_column_dropdown = ttk.Combobox(self, textvariable=self.z_column_var)
            self.z_column_dropdown.pack()

        ttk.Button(self, text="Create Graph", command=self.create_graph).pack()

        self.populate_column_names()
    
    
    def toggle_legend(self):
        pass  # Placeholder for the function to toggle legend display
    
    
    def toggle_mean_display(self):
        if self.mean_display_button is not None:
            if self.mean_display_button.instate(['selected']):
                ttk.Label(self.mean_display_frame, text="Select Column for Mean").pack()
                columns = self.data.columns.tolist()
                self.mean_column_var = tk.StringVar()
                self.mean_column_dropdown = ttk.Combobox(self.mean_display_frame, textvariable=self.mean_column_var, values=columns)
                self.mean_column_dropdown.pack()
                
                ttk.Label(self.mean_display_frame, text="Select Mean Line Style").pack()
                line_styles = ['-', '--', '-.', ':']  # Different line styles
                self.selected_line_style = tk.StringVar()
                self.mean_line_style_dropdown = ttk.Combobox(self.mean_display_frame, textvariable=self.selected_line_style, values=line_styles)
                self.mean_line_style_dropdown.pack()
                
                self.mean_display_frame.pack()
            else:
                if self.mean_column_dropdown is not None:
                    self.mean_display_frame.pack_forget()

    def toggle_alpha_dropdown(self):
        if self.add_grid_var.get():  # Display the alpha dropdown if checkbox is checked
            if self.alpha_dropdown is None:  # Create the alpha dropdown if it doesn't exist
                ttk.Label(self.alpha_frame, text="Select Grid Alpha").pack()
                alpha_values = ["0.1", "0.2", "0.3", "0.4", "0.5", "0.6", "0.7", "0.8", "0.9", "1.0"]
                self.selected_alpha = tk.StringVar()
                self.alpha_dropdown = ttk.Combobox(self.alpha_frame, textvariable=self.selected_alpha, values=alpha_values)
                self.alpha_dropdown.pack()
                self.alpha_frame.pack()
        else:  # Hide the alpha dropdown if checkbox is unchecked
            if self.alpha_dropdown is not None:
                self.alpha_frame.pack_forget()
    
    def populate_column_names(self):
        columns = self.data.columns.tolist()

        self.x_column_dropdown['values'] = columns
        if self.has_y_axis:
            self.y_column_dropdown['values'] = columns
        if self.has_z_axis:
            self.z_column_dropdown['values'] = columns
            
    def create_graph(self):
        x_column = self.x_column_var.get()
        y_column = self.y_column_var.get() if self.has_y_axis else None
        z_column = self.z_column_var.get() if self.has_z_axis else None
        
        selected_color = self.selected_color.get()
        
        try:
            if self.graph_type == "3D Scatter" or self.graph_type == "Surface Plot" or self.graph_type == "Wireframe":
                plt.switch_backend('TkAgg')  # Explicitly set backend to TkAgg
            plt.figure(figsize=(8, 6))

            if self.graph_type == "Line Graph":
                if y_column:
                    if self.mean_display_button is not None and self.mean_display_button.instate(['selected']):
                        mean_column = self.mean_column_var.get()
                        if mean_column:
                            selected_line_style = self.selected_line_style.get()  # Get the selected linestyle
                            mean_val = statistics.mean(self.data[mean_column])
                            plt.axhline(mean_val, color='r', linestyle=selected_line_style, label=f'Mean of {mean_column}')
                        else:
                            messagebox.showerror("Error", "Please select a column for displaying the mean.")
                    if self.display_legend_var.get():  # Check if the legend checkbox is selected
                        plt.plot(self.data[x_column], self.data[y_column], color=selected_color, label=f'{y_column}')
                        plt.legend()  # Display legend
                        plt.title("Line Graph")
                    else:
                        plt.plot(self.data[x_column], self.data[y_column], color=selected_color)
                        plt.title("Line Graph")
            elif self.graph_type == "Bar Graph":
                if y_column:
                    if self.mean_display_button is not None and self.mean_display_button.instate(['selected']):
                        mean_column = self.mean_column_var.get()
                        if mean_column:
                            selected_line_style = self.selected_line_style.get()
                            mean_val = statistics.mean(self.data[mean_column])
                            plt.axhline(mean_val, color='r', linestyle=selected_line_style, label=f'Mean of {mean_column}')
                        else:
                            messagebox.showerror("Error", "Please select a column for displaying the mean.")
                    if self.display_legend_var.get():
                        plt.bar(self.data[x_column], self.data[y_column], color=selected_color, label=f'{y_column}')
                        plt.legend()
                        plt.title("Bar Graph")
                    else:
                        plt.bar(self.data[x_column], self.data[y_column], color=selected_color)
                        plt.title("Bar Graph")
                else:
                    messagebox.showerror("Error", "Please select Y-Axis for Bar Graph.")
            elif self.graph_type == "Histogram":
                if self.display_legend_var.get():
                    plt.hist(self.data[x_column], color=selected_color, label=f'{x_column}')
                    plt.legend()
                    plt.title("Histogram")
                else:
                    plt.hist(self.data[x_column], color=selected_color)
                    plt.title("Histogram")                    
            elif self.graph_type == "Boxplot":
                plt.boxplot(self.data[x_column])
                plt.title("Boxplot")
            elif self.graph_type == "Scatterplot":
                if y_column:
                    plt.scatter(self.data[x_column], self.data[y_column], color=selected_color)
                    plt.title("Scatterplot")
                else:
                    messagebox.showerror("Error", "Please select Y-Axis for Scatterplot.")
            elif self.graph_type == "3D Scatter":
                if y_column and z_column:
                    fig = plt.figure()
                    ax = fig.add_subplot(111, projection='3d')
                    ax.scatter(self.data[x_column], self.data[y_column], self.data[z_column])
                    ax.set_title("3D Scatter")
                    ax.set_xlabel(x_column)
                    ax.set_ylabel(y_column)
                    ax.set_zlabel(z_column)
                else:
                    messagebox.showerror("Error", "Please select Y and Z-Axis for 3D Scatter.")
            elif self.graph_type == "Surface Plot":
                if y_column and z_column:
                    # Reshape data for surface plot
                    X = self.data[x_column].values.reshape(-1, 1)
                    Y = self.data[y_column].values.reshape(-1, 1)
                    Z = self.data[z_column].values.reshape(-1, 1)
                    
                    fig = plt.figure()
                    ax = fig.add_subplot(111, projection='3d')
                    ax.plot_trisurf(X.flatten(), Y.flatten(), Z.flatten(), cmap='viridis')
                    ax.set_title("Surface Plot")
                    ax.set_xlabel(x_column)
                    ax.set_ylabel(y_column)
                    ax.set_zlabel(z_column)
                else:
                    messagebox.showerror("Error", "Please select X, Y, and Z-Axis for Surface Plot.")
            elif self.graph_type == "Wireframe":
                if y_column and z_column:
                    # Reshape data for wireframe plot
                    X = self.data[x_column].values.reshape(-1, 1)
                    Y = self.data[y_column].values.reshape(-1, 1)
                    Z = self.data[z_column].values.reshape(-1, 1)
                    
                    fig = plt.figure()
                    ax = fig.add_subplot(111, projection='3d')
                    ax.plot_wireframe(X, Y, Z)
                    ax.set_title("Wireframe")
                    ax.set_xlabel(x_column)
                    ax.set_ylabel(y_column)
                    ax.set_zlabel(z_column)
                else:
                    messagebox.showerror("Error", "Please select X, Y, and Z-Axis for Wireframe.")
            
            if self.add_grid_var.get():  # Check if the checkbox is selected
                if self.alpha_dropdown is not None:  # Check if alpha dropdown exists
                    selected_alpha_value = float(self.selected_alpha.get())
                    plt.grid(True, alpha=selected_alpha_value)
            
            plt.xlabel(x_column)
            if y_column:
                plt.ylabel(y_column)
            plt.show()

        except Exception as e:
            messagebox.showerror("Error", f"Error creating graph: {str(e)}")