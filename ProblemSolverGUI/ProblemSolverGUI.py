import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np

class KnapsackSolver:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Knapsack Problem Solver")
        self.root.geometry("800x600")
        
        # Variables
        self.items = []
        self.capacity = tk.IntVar(value=10)
        self.solution = []
        self.selected_items = []
        self.total_value = 0
        
        self.create_ui()
        
    def create_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Input section
        input_frame = ttk.LabelFrame(main_frame, text="Problem Input", padding="10")
        input_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Capacity input
        ttk.Label(input_frame, text="Knapsack Capacity:").grid(row=0, column=0, sticky=tk.W)
        capacity_entry = ttk.Entry(input_frame, textvariable=self.capacity, width=10)
        capacity_entry.grid(row=0, column=1, sticky=tk.W, padx=(5, 0))
        
        # Items input frame
        items_frame = ttk.Frame(input_frame)
        items_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        ttk.Label(items_frame, text="Items (name, weight, value):").grid(row=0, column=0, sticky=tk.W)
        
        # Item entries
        self.item_entries = []
        for i in range(5):
            name_var = tk.StringVar(value=f"Item {i+1}")
            weight_var = tk.IntVar(value=i+1)
            value_var = tk.IntVar(value=(i+1)*2)
            
            name_entry = ttk.Entry(items_frame, textvariable=name_var, width=10)
            weight_entry = ttk.Entry(items_frame, textvariable=weight_var, width=5)
            value_entry = ttk.Entry(items_frame, textvariable=value_var, width=5)
            
            name_entry.grid(row=i+1, column=0, padx=(0, 5), pady=2)
            weight_entry.grid(row=i+1, column=1, padx=(0, 5), pady=2)
            value_entry.grid(row=i+1, column=2, pady=2)
            
            self.item_entries.append((name_var, weight_var, value_var))
        
        # Buttons
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=2, column=0, columnspan=3, pady=(10, 0))
        
        ttk.Button(button_frame, text="Solve", command=self.solve).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Clear", command=self.clear).pack(side=tk.LEFT)
        
        # Results section
        results_frame = ttk.LabelFrame(main_frame, text="Solution", padding="10")
        results_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Solution info
        info_frame = ttk.Frame(results_frame)
        info_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.solution_label = ttk.Label(info_frame, text="Total Value: 0")
        self.solution_label.grid(row=0, column=0, sticky=tk.W)
        
        self.items_label = ttk.Label(info_frame, text="Selected Items: None")
        self.items_label.grid(row=1, column=0, sticky=tk.W)
        
        # Grid display
        grid_frame = ttk.Frame(results_frame)
        grid_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create a canvas with scrollbar for the grid
        self.canvas = tk.Canvas(grid_frame, width=700, height=300, bg="white")
        scrollbar = ttk.Scrollbar(grid_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Configure grid weights for resizing
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(1, weight=1)
        
    def solve(self):
        try:
            # Get items from entries
            self.items = []
            for name_var, weight_var, value_var in self.item_entries:
                name = name_var.get()
                weight = weight_var.get()
                value = value_var.get()
                
                if name and weight > 0 and value >= 0:
                    self.items.append((name, weight, value))
            
            if not self.items:
                messagebox.showerror("Error", "Please enter at least one valid item.")
                return
                
            capacity = self.capacity.get()
            if capacity <= 0:
                messagebox.showerror("Error", "Capacity must be positive.")
                return
                
            # Solve knapsack problem
            self.solution, self.selected_items, self.total_value = self.knapsack_dp(self.items, capacity)
            
            # Update UI
            self.solution_label.config(text=f"Total Value: {self.total_value}")
            self.items_label.config(text=f"Selected Items: {', '.join([item[0] for item in self.selected_items])}")
            
            # Display the grid
            self.display_grid()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for weights and values.")
    
    def knapsack_dp(self, items, capacity):
        n = len(items)
        # Create a DP table with dimensions (n+1) x (capacity+1)
        dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]
        
        # Fill the DP table
        for i in range(1, n + 1):
            name, weight, value = items[i-1]
            for w in range(1, capacity + 1):
                if weight <= w:
                    dp[i][w] = max(dp[i-1][w], dp[i-1][w - weight] + value)
                else:
                    dp[i][w] = dp[i-1][w]
        
        # Backtrack to find selected items
        selected_items = []
        w = capacity
        for i in range(n, 0, -1):
            if dp[i][w] != dp[i-1][w]:
                name, weight, value = items[i-1]
                selected_items.append(items[i-1])
                w -= weight
        
        return dp, selected_items, dp[n][capacity]
    
    def display_grid(self):
        # Clear previous grid
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        if not self.solution:
            return
            
        n = len(self.items)
        capacity = self.capacity.get()
        
        # Create header row
        header_frame = ttk.Frame(self.scrollable_frame)
        header_frame.grid(row=0, column=0, columnspan=capacity+2, sticky=(tk.W, tk.E))
        
        ttk.Label(header_frame, text="Items/Capacity", width=12, borderwidth=1, 
                 relief="solid", background="lightblue").grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        for w in range(capacity + 1):
            ttk.Label(header_frame, text=str(w), width=5, borderwidth=1, 
                     relief="solid", background="lightblue").grid(row=0, column=w+1, sticky=(tk.W, tk.E))
        
        # Create data rows
        for i in range(n + 1):
            row_frame = ttk.Frame(self.scrollable_frame)
            row_frame.grid(row=i+1, column=0, columnspan=capacity+2, sticky=(tk.W, tk.E))
            
            # Row header
            if i == 0:
                label_text = "No items"
            else:
                name, weight, value = self.items[i-1]
                label_text = f"{name}\n(w:{weight}, v:{value})"
                
            ttk.Label(row_frame, text=label_text, width=12, borderwidth=1, 
                     relief="solid", background="lightblue").grid(row=0, column=0, sticky=(tk.W, tk.E))
            
            # Data cells
            for w in range(capacity + 1):
                cell_value = self.solution[i][w]
                # Highlight selected cells
                bg_color = "lightgreen" if self.is_selected_cell(i, w) else "white"
                ttk.Label(row_frame, text=str(cell_value), width=5, borderwidth=1, 
                         relief="solid", background=bg_color).grid(row=0, column=w+1, sticky=(tk.W, tk.E))
    
    def is_selected_cell(self, i, w):
        # Check if this cell is part of the optimal solution path
        if i == 0 or w == 0:
            return False
            
        if self.solution[i][w] != self.solution[i-1][w]:
            return True
            
        return False
    
    def clear(self):
        self.capacity.set(10)
        for i, (name_var, weight_var, value_var) in enumerate(self.item_entries):
            name_var.set(f"Item {i+1}")
            weight_var.set(i+1)
            value_var.set((i+1)*2)
        
        self.solution = []
        self.selected_items = []
        self.total_value = 0
        
        self.solution_label.config(text="Total Value: 0")
        self.items_label.config(text="Selected Items: None")
        
        # Clear grid
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = KnapsackSolver()
    app.run()