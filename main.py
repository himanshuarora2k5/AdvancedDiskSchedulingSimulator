# gui_disk_scheduler.py (Version 8 - Added Accessibility Options)

import tkinter as tk
from tkinter import ttk, messagebox, font, filedialog
from algorithm_engine import fcfs, sstf, scan, c_scan
import csv

from visualization_module import show_combined_disk_movement

import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('TkAgg')

import sv_ttk

class DiskSchedulerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Disk Scheduling Algorithm Simulator")
        self.root.geometry("1200x700")  # Further increased window width
        sv_ttk.set_theme("dark")  # Apply the Sun Valley dark theme

        self.all_results = None
        self.initial_head_pos = None
        self.disk_requests_list = None
        self.algo_vars = {}
        self.algo_checkbuttons = {}

        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="20 20 20 20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        header = ttk.Label(main_frame, text="DISK SCHEDULING SIMULATOR", font=("Segoe UI", 18, "bold"), anchor=tk.CENTER)
        header.pack(pady=(0, 20), fill=tk.X)

        # Left side (existing content)
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 20))

        # --- Input Frame ---
        input_outer_frame = ttk.Frame(left_frame)
        input_outer_frame.pack(fill=tk.X, pady=5)
        
        # Input frame for disk requests with import button
        input_frame = ttk.Frame(input_outer_frame)
        input_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Disk Requests row with import button
        disk_requests_frame = ttk.Frame(input_frame)
        disk_requests_frame.grid(row=0, column=0, columnspan=2, sticky=tk.EW, pady=5)
        
        ttk.Label(disk_requests_frame, text="Disk Requests:", font=("Segoe UI", 11)).pack(side=tk.LEFT, padx=(0, 5))
        self.requests_entry = ttk.Entry(disk_requests_frame, font=("Segoe UI", 11), width=50)
        self.requests_entry.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        self.requests_entry.insert(0, "98, 183, 37, 122, 14, 124, 65, 67")
        
        import_btn = ttk.Button(disk_requests_frame, text="Import CSV", command=self.import_csv)
        import_btn.pack(side=tk.LEFT, padx=5)

        ttk.Label(input_frame, text="Initial Head Pos:", font=("Segoe UI", 11)).grid(row=1, column=0, padx=(0, 5), pady=5, sticky=tk.W)
        self.head_entry = ttk.Entry(input_frame, font=("Segoe UI", 11), width=15)
        self.head_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        self.head_entry.insert(0, "53")

        buttons_frame = ttk.Frame(input_outer_frame)
        buttons_frame.pack(side=tk.RIGHT, padx=10)

        clear_data_button = ttk.Button(buttons_frame, text="Clear All Data", command=self.clear_input_fields)
        clear_data_button.pack(pady=5, fill=tk.X)

        run_button_frame = ttk.Frame(left_frame)
        run_button_frame.pack(pady=(15, 10), fill=tk.X)
        self.run_button = ttk.Button(run_button_frame, text="RUN SIMULATION & COMPARE", command=self.run_simulation, style="Accent.TButton")
        self.run_button.pack(expand=True, fill=tk.X)

        # --- Results Frame ---
        results_frame = ttk.LabelFrame(left_frame, text="Simulation Comparison Results")
        results_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Create the text widget with scrollbar
        self.result_text = tk.Text(results_frame, height=10, wrap=tk.WORD, 
                                 font=("Consolas", 16), bg="#1a1a1a", fg="white",
                                 insertbackground="white", selectbackground="#4ECDC4",
                                 padx=10, pady=10)
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=scrollbar.set)

        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.result_text.insert(tk.END, ">> Waiting for simulation...\n")
        self.result_text.config(state=tk.DISABLED)

        # Right side (Track Positions) with increased width
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(20, 0))

        # Configure weight for the frames
        main_frame.columnconfigure(0, weight=2)  # Left frame takes 2 parts
        main_frame.columnconfigure(1, weight=3)  # Right frame takes 3 parts

        # Track Positions Frame with increased width
        track_frame = ttk.LabelFrame(right_frame, text="Track Positions")
        track_frame.pack(fill=tk.BOTH, expand=True)

        # Create the track positions text widget with increased width
        self.track_text = tk.Text(track_frame, height=10, wrap=tk.WORD,
                                font=("Consolas", 12), bg="#1a1a1a", fg="white",
                                insertbackground="white", selectbackground="#4ECDC4",
                                padx=10, pady=10, width=60)  # Increased width from 45 to 60
        track_scrollbar = ttk.Scrollbar(track_frame, orient=tk.VERTICAL, command=self.track_text.yview)
        self.track_text.configure(yscrollcommand=track_scrollbar.set)

        self.track_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        track_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.track_text.insert(tk.END, ">> Track positions will appear here after simulation...\n")
        self.track_text.config(state=tk.DISABLED)

        # --- Visualization Selection Frame ---
        vis_select_outer_frame = ttk.Frame(left_frame)
        vis_select_outer_frame.pack(fill=tk.X, pady=5)

        vis_select_frame = ttk.LabelFrame(vis_select_outer_frame, text="Select Algorithms to Visualize")
        vis_select_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        vis_buttons_frame = ttk.Frame(vis_select_outer_frame)
        vis_buttons_frame.pack(side=tk.RIGHT, padx=10, fill=tk.Y)

        algorithms = ["FCFS", "SSTF", "SCAN", "C-SCAN"]
        num_cols = 4
        for i, algo in enumerate(algorithms):
            self.algo_vars[algo] = tk.IntVar()
            cb = ttk.Checkbutton(vis_select_frame, text=algo, variable=self.algo_vars[algo], state='disabled')
            col = i % num_cols
            row = i // num_cols
            cb.grid(row=row, column=col, padx=15, pady=5, sticky=tk.W)
            self.algo_checkbuttons[algo] = cb

        for i in range(num_cols):
            vis_select_frame.columnconfigure(i, weight=1)

        select_all_button = ttk.Button(vis_buttons_frame, text="Select All", command=self.select_all_algorithms)
        select_all_button.pack(pady=5, fill=tk.X)

        clear_selection_button = ttk.Button(vis_buttons_frame, text="Clear Selection", command=self.clear_all_algorithm_selections)
        clear_selection_button.pack(pady=5, fill=tk.X)

        vis_button_frame = ttk.Frame(left_frame)
        vis_button_frame.pack(pady=(10, 0), fill=tk.X)
        self.visualize_button = ttk.Button(vis_button_frame, text="VISUALIZE SELECTED", command=self.show_visualization, state='disabled', style="Accent.TButton")
        self.visualize_button.pack(expand=True, fill=tk.X)

    def clear_input_fields(self):
        """Clears the disk requests and initial head position input fields."""
        self.requests_entry.delete(0, tk.END)
        self.head_entry.delete(0, tk.END)

    def select_all_algorithms(self):
        """Selects all available disk scheduling algorithms for visualization."""
        for algo in self.algo_vars:
            if algo in self.all_results:  # Only select if results are available
                self.algo_vars[algo].set(1)

    def clear_all_algorithm_selections(self):
        """Clears the selection of all disk scheduling algorithms for visualization."""
        for algo in self.algo_vars:
            self.algo_vars[algo].set(0)

    def import_csv(self):
        try:
            file_path = filedialog.askopenfilename(
                title="Select CSV File",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )
            
            if not file_path:  # User cancelled the dialog
                return
                
            with open(file_path, 'r') as file:
                csv_reader = csv.reader(file)
                # Read the first row and join the values with commas
                for row in csv_reader:
                    # Filter out any empty strings and convert to integers to validate
                    values = [int(val.strip()) for val in row if val.strip()]
                    # Convert back to strings and join with commas
                    disk_requests = ", ".join(map(str, values))
                    self.requests_entry.delete(0, tk.END)
                    self.requests_entry.insert(0, disk_requests)
                    break  # Only read the first row
                    
        except ValueError as e:
            messagebox.showerror("Import Error", "Invalid data in CSV file. Please ensure all values are integers.")
        except Exception as e:
            messagebox.showerror("Import Error", f"Error reading CSV file:\n{str(e)}")

    def update_track_positions(self):
        """Update the track positions display with the current results."""
        if not self.all_results:
            return

        self.track_text.config(state=tk.NORMAL)
        self.track_text.delete(1.0, tk.END)

        # Configure text tags
        self.track_text.tag_configure("header", foreground="#4ECDC4", font=("Consolas", 12, "bold"))
        self.track_text.tag_configure("algo_name", foreground="#FF6B6B", font=("Consolas", 12, "bold"))
        self.track_text.tag_configure("positions", foreground="white", font=("Consolas", 12))
        self.track_text.tag_configure("separator", foreground="#444444", font=("Consolas", 12))

        self.track_text.insert(tk.END, "Track Positions by Algorithm:\n\n", "header")

        # Display track positions for each algorithm
        for algo_name, result in self.all_results.items():
            # Get the movement path including initial head position
            path = [self.initial_head_pos] + result.get("order", [])
            
            # Insert algorithm name
            self.track_text.insert(tk.END, f"{algo_name}:\n", "algo_name")
            
            # Format positions in rows of 5
            positions = [str(pos).rjust(4) for pos in path]
            for i in range(0, len(positions), 5):
                row = positions[i:i+5]
                self.track_text.insert(tk.END, " ".join(row) + "\n", "positions")
            
            # Use a shorter separator that won't wrap
            self.track_text.insert(tk.END, "\n" + "-"*25 + "\n\n", "separator")

        self.track_text.config(state=tk.DISABLED)

    def run_simulation(self):
        try:
            requests_str = self.requests_entry.get()
            if not requests_str: raise ValueError("Disk Requests cannot be empty.")
            self.disk_requests_list = [int(x.strip()) for x in requests_str.split(',')]
            if not self.disk_requests_list: raise ValueError("No valid disk requests entered.")
            if any(r < 0 for r in self.disk_requests_list): raise ValueError("Disk Requests must be non-negative integers.")
            head_str = self.head_entry.get()
            if not head_str: raise ValueError("Initial Head Position cannot be empty.")
            self.initial_head_pos = int(head_str)
            if self.initial_head_pos < 0: raise ValueError("Initial Head Position must be non-negative.")

            self.all_results = {
                "FCFS": fcfs(self.disk_requests_list, self.initial_head_pos),
                "SSTF": sstf(self.disk_requests_list, self.initial_head_pos),
                "SCAN": scan(self.disk_requests_list, self.initial_head_pos),
                "C-SCAN": c_scan(self.disk_requests_list, self.initial_head_pos)
            }

            # Update both results displays
            self.update_results_display()  # Update main results
            self.update_track_positions()  # Update track positions

            self.visualize_button.config(state='normal')
            for algo, cb in self.algo_checkbuttons.items():
                if algo in self.all_results:
                    cb.config(state='normal')
                else:
                    cb.config(state='disabled')

        except ValueError as e:
            messagebox.showerror("Input Error", f"Invalid input:\n{e}\nPlease enter comma-separated non-negative integers for requests and a non-negative integer for the head position.")
            self.reset_visualization_options()
        except Exception as e:
            messagebox.showerror("Simulation Error", f"An unexpected error occurred during simulation:\n{e}")
            self.reset_visualization_options()

    def update_results_display(self):
        """Update the main results display."""
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)

        # Insert results with enhanced formatting
        self.result_text.insert(tk.END, ">> Simulation Comparison Complete:\n\n", "header")
        
        # Configure text tags with larger fonts and modern colors
        self.result_text.tag_configure("header_cyan", foreground="#4ECDC4", font=("Consolas", 16, "bold"))
        self.result_text.tag_configure("value_color", foreground="#FF6B6B", font=("Consolas", 16))
        self.result_text.tag_configure("separator", foreground="#444444", font=("Consolas", 16))
        
        # Calculate column widths
        algo_width = 12
        move_width = 16
        seek_width = 14
        thpt_width = 12
        
        # Create header with proper spacing
        header = (
            f"{'Algorithm':<{algo_width}} "
            f"{'Total Movement':<{move_width}} "
            f"{'Average Seek':<{seek_width}} "
            f"{'Throughput':<{thpt_width}}"
        )
        
        # Insert header with extra spacing for readability
        self.result_text.insert(tk.END, "\n")  # Extra space at top
        self.result_text.insert(tk.END, header + "\n", "header_cyan")
        
        # Create separator line
        separator = "-" * (algo_width + move_width + seek_width + thpt_width + 3)
        self.result_text.insert(tk.END, separator + "\n", "separator")

        # Sort algorithms by total movement
        sorted_results = sorted(self.all_results.items(), 
                             key=lambda x: x[1]['head Movement'])

        # Format and insert values with extra line spacing
        for algo_name, result in sorted_results:
            mov = str(result.get('head Movement', 'N/A'))
            seek = f"{result.get('average Seek', 0):.2f}"
            thpt = f"{result.get('throughput', 0):.4f}"
            
            # Format each row with proper spacing and left alignment
            row = (
                f"{algo_name:<{algo_width}} "
                f"{mov:<{move_width}} "
                f"{seek:<{seek_width}} "
                f"{thpt:<{thpt_width}}"
            )
            self.result_text.insert(tk.END, row + "\n", "value_color")
            self.result_text.insert(tk.END, "\n")  # Add extra line spacing between rows

        # Bottom separator
        self.result_text.insert(tk.END, separator + "\n", "separator")
        self.result_text.insert(tk.END, "\n")  # Extra space at bottom

        self.result_text.config(state=tk.DISABLED)

    def show_visualization(self):
        if not self.all_results:
            messagebox.showwarning("No Data", "Please run the simulation first.")
            return

        selected_algos = [algo for algo, var in self.algo_vars.items() if var.get() == 1]

        if not selected_algos:
            messagebox.showwarning("No Selection", "Please select at least one algorithm to visualize using the checkboxes.")
            return

        results_to_plot = {}
        for algo_name in selected_algos:
            if algo_name in self.all_results:
                if 'order' in self.all_results[algo_name]:
                    results_to_plot[algo_name] = self.all_results[algo_name]
                else:
                    print(f"Warning: Results for {algo_name} missing 'order' data, skipping.")
                    messagebox.showwarning("Missing Data", f"Plotting data ('order') missing for {algo_name}. Skipping.")
            else:
                print(f"Warning: Results for {algo_name} not found, skipping.")

        if not results_to_plot:
            messagebox.showerror("Error", "Could not find valid plot data for any selected algorithm.")
            return

        try:
            print(f"Creating plot for: {', '.join(results_to_plot.keys())}")
            plt.style.use('dark_background')
            fig, ax = plt.subplots(figsize=(12, 7))
            # Use self.root to get the background color
            bg_color_hex = self.root.cget("bg")
            r, g, b = self.root.winfo_rgb(bg_color_hex)
            fig.patch.set_facecolor((r / 65535.0, g / 65535.0, b / 65535.0))
            ax.set_facecolor((r / 65535.0, g / 65535.0, b / 65535.0))

            # Get the animation object
            ani = show_combined_disk_movement(results_to_plot, self.initial_head_pos, ax)

            fig.tight_layout(pad=1.5)
            plt.show()
            print("plt.show() finished.")

        except Exception as e:
            messagebox.showerror("Visualization Error", f"An error occurred while generating the combined plot:\n{e}")

    def reset_visualization_options(self):
        self.visualize_button.config(state='disabled')
        for algo, cb in self.algo_checkbuttons.items():
            cb.config(state='disabled')
            if algo in self.algo_vars:
                self.algo_vars[algo].set(0)
        self.all_results = None
        self.initial_head_pos = None
        self.disk_requests_list = None

if __name__ == "__main__":
    root = tk.Tk()
    app = DiskSchedulerGUI(root)
    root.mainloop()

