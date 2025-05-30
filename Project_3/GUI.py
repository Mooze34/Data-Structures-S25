# MXA 220164
# Mustafa Alawad
# CS 3345.009
# Project 3



import tkinter as tk  # Tkinter is used for the GUI (Native to python, no need to install)
from tkinter import ttk, messagebox # To display the path route 
from Maze import (
    generate_maze,  # Creates a random maze
    solve_maze,     # Finds path from start to end
    path_to_directions,  # Converts path coordinates to human-readable directions
    WALL_N, WALL_S, WALL_E, WALL_W  # Constants for wall positions
)

CELL_SIZE = 20  # Size of each maze cell in pixels - bigger = easier to see

class MazeApp(tk.Tk):
    def __init__(self):
        super().__init__()  # Initialize the parent class (basic tk stuff)
        self.title("Maze Solver")  # Window title

        # Set up the control panel
        frm = ttk.Frame(self)
        frm.pack(padx=10, pady=10)  # Add some padding so it looks decent

        # Input fields for maze dimensions
        ttk.Label(frm, text="Width:").grid(row=0, column=0)
        self.w_var = tk.IntVar(value="")  # Variable to store width
        ttk.Entry(frm, textvariable=self.w_var, width=5).grid(row=0, column=1)

        ttk.Label(frm, text="Height:").grid(row=0, column=2)
        self.h_var = tk.IntVar(value="")  # Variable to store height
        ttk.Entry(frm, textvariable=self.h_var, width=5).grid(row=0, column=3)

        # Buttons for generating and solving
        ttk.Button(frm, text="Generate Maze", command=self.on_generate)\
            .grid(row=0, column=6, padx=5)
        ttk.Button(frm, text="Solve Path", command=self.on_solve)\
            .grid(row=0, column=7)

        # Canvas = the drawing area for our maze
        self.canvas = tk.Canvas(self, bg="white")
        self.canvas.pack(padx=10, pady=10)

        # Initialize empty maze and path
        self.maze = []  # Will hold maze data
        self.path = []  # Will hold solution path
        self.path_color = "orange"  # Color for the solution (obviously orange)

    def on_generate(self):
        # Grab dimensions from input fields
        w, h = self.w_var.get(), self.h_var.get()
        if w <= 0 or h <= 0:
            return messagebox.showerror("Error", "Dimensions must be > 0")  # No zero/negative mazes
        self.maze = generate_maze(w, h)  # Create a new random maze
        self.path = []  # Clear any existing path
        # Resize canvas to fit the maze
        self.canvas.config(width=w*CELL_SIZE, height=h*CELL_SIZE)
        self.draw_maze()  # Draw the new maze

    def on_solve(self):
        if not self.maze:  # Can't solve what doesn't exist
            return
        self.path = solve_maze(self.maze)  # Find the solution path
        self.path_color = "orange"  # Set path color
        self.draw_maze()  # Redraw maze with solution
        dirs = path_to_directions(self.path)  # Convert coordinates to directions
        messagebox.showinfo("Path Directions", dirs)  # Show directions in popup

    def draw_maze(self):
        self.canvas.delete("all")  # Clear the canvas
        if not self.maze:
            return  # Nothing to draw

        h, w = len(self.maze), len(self.maze[0])  # Get maze dimensions
        # Draw all walls for each cell
        for y in range(h):
            for x in range(w):
                x1, y1 = x*CELL_SIZE,   y*CELL_SIZE  # Top-left corner
                x2, y2 = x1+CELL_SIZE,  y1+CELL_SIZE  # Bottom-right corner
                cell = self.maze[y][x]  # Current cell's wall config
                # Draw each wall if it exists
                if cell & WALL_N:  # North wall
                    self.canvas.create_line(x1, y1, x2, y1, fill="black")
                if cell & WALL_S:  # South wall
                    self.canvas.create_line(x1, y2, x2, y2, fill="black")
                if cell & WALL_W:  # West wall
                    self.canvas.create_line(x1, y1, x1, y2, fill="black")
                if cell & WALL_E:  # East wall
                    self.canvas.create_line(x2, y1, x2, y2, fill="black")

        # Draw solution path (if exists)
        for (x, y) in self.path:
            x1, y1 = x*CELL_SIZE+2, y*CELL_SIZE+2  # Add offset to stay inside walls
            self.canvas.create_rectangle(
                x1, y1,
                x1+CELL_SIZE-4, y1+CELL_SIZE-4,  # -4 to make it smaller than cell
                fill=self.path_color, outline=self.path_color  # Orange boxes show the path
            )

if __name__ == '__main__':
    app = MazeApp()  # Create the app
    app.mainloop()  # Start it running - this is the event loop