# visualization_module.py (Updated)

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import itertools # To cycle through colors
import numpy as np

# --- Original function (Modified: removed plt.show()) ---
def show_disk_movement(disk_data, start):
    """
    DEPRECATED for combined view, but kept for potential individual use.
    Draws a graph for a single algorithm's disk head movement.
    NOTE: This function no longer calls plt.show() itself.
    """
    movement_path = [start] + disk_data.get("order", []) # Use .get for safety
    if not movement_path or len(movement_path) <= 1 :
        print(f"Warning: No movement data to plot for algorithm.")
        # Optionally create an empty plot or just return
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.set_title("Disk Head Movement (No Data)")
        ax.set_xlabel("Steps")
        ax.set_ylabel("Tracks")
        return # Exit if no data

    x_axis = list(range(len(movement_path)))

    # Basic light theme plotting if called directly
    fig, ax = plt.subplots(figsize=(10, 5)) # Slightly wider figure
    ax.plot(x_axis, movement_path, marker='o', linestyle='-', color='blue')
    ax.set_title(f"Disk Head Movement (Individual)") # Add Algo name if passed
    ax.set_xlabel("Request Servicing Step")
    ax.set_ylabel("Track Number")
    ax.grid(True, linestyle='--', alpha=0.6)

    for idx, trk in enumerate(movement_path):
        ax.annotate(str(trk), (x_axis[idx], movement_path[idx]),
                    textcoords="offset points", xytext=(0, 8), ha='center', fontsize=9)

    stats_box = (
        f"Total Movement: {disk_data.get('head Movement', 'N/A')}\n"
        f"Avg Seek Time: {disk_data.get('average Seek', 0):.2f}\n"
        f"Throughput: {disk_data.get('throughput', 0):.4f} req/unit"
    )
    ax.text(0.98, 0.95, stats_box, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', horizontalalignment='right',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='wheat', alpha=0.7))

    # plt.show() # <--- REMOVED

# --- NEW Function for Combined Plotting with Dark Theme ---
def show_combined_disk_movement(results_dict, start_head, ax):
    """
    Draws animated disk head movement for multiple algorithms on the *provided* Axes object.
    """
    print("--- Entering show_combined_disk_movement (plotting on provided Axes) ---")
    print(f"Algorithms to plot: {list(results_dict.keys())}")

    # Updated color scheme for better differentiation
    color_cycle = itertools.cycle([
        '#FF6B6B',  # Bright red for FCFS
        '#4ECDC4',  # Turquoise for SSTF
        '#FFD93D',  # Bright yellow for SCAN
        '#A78BFA',  # Purple for C-SCAN
        '#118AB2',  # Blue (spare)
        '#EF476F'   # Pink (spare)
    ])
    
    max_steps = 0
    plot_count = 0
    lines = []
    points = []  # Store points for pulsing effect
    movement_paths = []

    # Prepare data for animation
    for algo_name, result in results_dict.items():
        print(f"Processing: {algo_name}")
        movement_path = [int(start_head)] + [int(x) for x in result.get("order", [])]
        if not movement_path or len(movement_path) <= 1:
            print(f"  Skipping {algo_name}: No movement data.")
            continue

        if algo_name == "C-SCAN":
            print(f"C-SCAN path: {movement_path}")

        x_axis = list(range(len(movement_path)))
        max_steps = max(max_steps, len(x_axis))
        current_color = next(color_cycle)
        movement_paths.append((x_axis, movement_path, algo_name, current_color))

    # Initialize empty lines and points
    for x_axis, movement_path, algo_name, color in movement_paths:
        line, = ax.plot([], [], marker='', linestyle='-',
                       linewidth=1.5, color=color, label=algo_name)
        # Add points with a larger size for pulsing effect
        point, = ax.plot([], [], marker='o', markersize=6, 
                        color=color, alpha=0.8)
        lines.append((line, x_axis, movement_path))
        points.append(point)
        plot_count += 1

    # Set consistent dark background
    ax.set_facecolor('#1a1a1a')  # Dark background color

    # Pre-calculate all positions for smoother animation
    interpolated_positions = []
    for x_axis, movement_path, algo_name, _ in movement_paths:
        positions = []
        
        # For C-SCAN, pre-process the path to ensure all points are included
        if algo_name == "C-SCAN":
            print(f"Processing C-SCAN path: {movement_path}")
            # Find the indices where we hit 199 and 0
            try:
                max_idx = movement_path.index(199)
                zero_idx = movement_path.index(0)
                print(f"C-SCAN indices - max: {max_idx}, zero: {zero_idx}")
                print(f"Points after zero: {movement_path[zero_idx:]}")
                
                # Process points up to 199
                for i in range(max_idx):
                    x1, x2 = x_axis[i], x_axis[i + 1]
                    y1, y2 = movement_path[i], movement_path[i + 1]
                    positions.append((x1, y1))
                
                # Add the point at 199
                positions.append((x_axis[max_idx], 199))
                
                # Add the jump to 0
                positions.append((x_axis[zero_idx], 0))
                
                # Process all remaining points after 0
                for i in range(zero_idx, len(movement_path)):
                    positions.append((x_axis[i], movement_path[i]))
                    if i < len(movement_path) - 1:
                        x1, x2 = x_axis[i], x_axis[i + 1]
                        y1, y2 = movement_path[i], movement_path[i + 1]
                        for t in np.linspace(0.1, 0.9, 3):  # Fewer interpolation points
                            x = x1 + (x2 - x1) * t
                            y = y1 + (y2 - y1) * t
                            positions.append((x, y))
                
            except ValueError as e:
                print(f"Error processing C-SCAN path: {e}")
                # Fallback to normal interpolation
                for i in range(len(x_axis) - 1):
                    x1, x2 = x_axis[i], x_axis[i + 1]
                    y1, y2 = movement_path[i], movement_path[i + 1]
                    positions.append((x1, y1))
                    for t in np.linspace(0.1, 0.9, 3):
                        x = x1 + (x2 - x1) * t
                        y = y1 + (y2 - y1) * t
                        positions.append((x, y))
                positions.append((x_axis[-1], movement_path[-1]))
        else:
            # Normal interpolation for other algorithms
            for i in range(len(x_axis) - 1):
                x1, x2 = x_axis[i], x_axis[i + 1]
                y1, y2 = movement_path[i], movement_path[i + 1]
                positions.append((x1, y1))
                for t in np.linspace(0.1, 0.9, 3):
                    x = x1 + (x2 - x1) * t
                    y = y1 + (y2 - y1) * t
                    positions.append((x, y))
            positions.append((x_axis[-1], movement_path[-1]))
                    
        interpolated_positions.append(positions)
        if algo_name == "C-SCAN":
            print(f"Final C-SCAN positions: {positions}")

    # Animation update function
    def update(frame):
        frames_per_algo = len(interpolated_positions[0]) if interpolated_positions else 0
        current_algo_index = frame // frames_per_algo
        current_step = frame % frames_per_algo
        
        # Reset all lines
        for line, _, _ in lines:
            line.set_data([], [])
        for point in points:
            point.set_data([], [])
            
        # Plot up to current algorithm
        animated_elements = []
        for i in range(len(lines)):  # Changed to always plot all algorithms
            line, x_axis, movement_path = lines[i]
            point = points[i]
            
            if i < current_algo_index:
                # Show complete path for previous algorithms
                line.set_data(x_axis, movement_path)
                # Show final point
                point.set_data([x_axis[-1]], [movement_path[-1]])
            elif i == current_algo_index:
                # Show partial path for current algorithm
                if current_step < len(interpolated_positions[i]):
                    # Get all positions up to current step
                    positions = interpolated_positions[i][:current_step + 1]
                    if positions:
                        x_coords = [p[0] for p in positions]
                        y_coords = [p[1] for p in positions]
                        line.set_data(x_coords, y_coords)
                        
                        # Show current position with subtle pulse
                        current_x, current_y = positions[-1]
                        pulse = 1 + 0.2 * np.sin(frame * 0.1)  # Reduced pulse effect
                        point.set_markersize(6 * pulse)
                        point.set_data([current_x], [current_y])
                else:
                    # If animation is complete for this algorithm, show full path
                    line.set_data(x_axis, movement_path)
                    point.set_data([x_axis[-1]], [movement_path[-1]])
            
            animated_elements.extend([line, point])

        # Subtle grid animation
        grid_alpha = 0.3 + 0.05 * np.sin(frame * 0.05)  # Reduced grid animation
        ax.grid(True, linestyle=':', linewidth=0.5, color='gray', alpha=grid_alpha)
        
        return animated_elements

    # Create animation with higher frame rate
    ani = animation.FuncAnimation(
        ax.figure, update, 
        frames=len(lines) * (len(interpolated_positions[0]) if interpolated_positions else 0),
        interval=25,  # Increased speed (40fps, changed from 50ms to 25ms)
        blit=True,
        repeat=False
    )

    # --- Styling with enhanced visual effects ---
    title = ax.set_title('Disk Head Movement Comparison', 
                        color='white', fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel('Request Servicing Step', color='white', fontsize=11)
    ax.set_ylabel('Track Number', color='white', fontsize=11)
    
    # Enhanced grid with consistent styling
    ax.grid(True, linestyle=':', linewidth=0.5, color='gray', alpha=0.3)
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    
    # Stylish spines
    for spine in ax.spines.values():
        spine.set_linewidth(1.2)
    ax.spines['top'].set_color('#444444')
    ax.spines['right'].set_color('#444444')
    ax.spines['left'].set_color('white')
    ax.spines['bottom'].set_color('white')

    # Set axis limits with padding
    if max_steps > 0:
        ax.set_xlim(left=-0.5, right=max_steps - 0.5)
        all_y_values = []
        for _, path, _, _ in movement_paths:
            all_y_values.extend(path)
            # For C-SCAN, explicitly include the full range (0 to 199)
            if any(p >= 199 for p in path):  # If this is C-SCAN path
                all_y_values.extend([0, 199])  # Include full range
        
        if all_y_values:
            y_min = 0  # Always start from 0
            y_max = 199  # Always go to max disk size
            padding = max(5, (y_max - y_min) * 0.1)
            ax.set_ylim(bottom=y_min, top=y_max + padding)

    # Enhanced legend with modern style
    if results_dict and plot_count > 0:
        legend = ax.legend(facecolor='#333333', edgecolor='gray', 
                          fontsize=9, labelcolor='white',
                          framealpha=0.8, borderpad=1,
                          handlelength=1.5)
        # Add hover effect to legend
        legend.set_zorder(1000)
        print("Legend created.")
    else:
        print("No legend created (no data or no plots).")

    print("--- Exiting show_combined_disk_movement ---")
    return ani
