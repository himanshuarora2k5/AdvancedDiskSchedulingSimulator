# Disk Scheduling Algorithm Simulator

A Python-based GUI application using Tkinter and Matplotlib to simulate and visualize different disk scheduling algorithms. Compare FCFS, SSTF, SCAN, and C-SCAN based on total head movement, average seek time, and throughput.

## Features

* **Implemented Algorithms:**
    * First-Come, First-Served (FCFS)
    * Shortest Seek Time First (SSTF)
    * SCAN (Elevator Algorithm)
    * C-SCAN (Circular SCAN)
* **Graphical User Interface (GUI):** Built with Tkinter for easy input and display.
* **CSV Import:** Load disk requests directly from a CSV file.
* **Results Comparison:** View a tabular comparison of total head movement, average seek time, and throughput for each algorithm.
* **Track Position Display:** See the sequence of track accesses for each algorithm.
* **Animated Visualization:** Visualize the disk head movement path for selected algorithms on an interactive Matplotlib plot.

## Requirements

* Python 3.6+
* The libraries listed in `requirements.txt`.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/himanshuarora2k5/AdvancedDiskSchedulingSimulator
    cd disk-scheduling-simulator
    ```

2.  **Install the required libraries:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  **Run the main GUI script:**
    ```bash
    python main.py
    ```

2.  **Enter Disk Requests:**
    * Enter the track numbers the disk head needs to visit, separated by commas (e.g., `98, 183, 37, 122, 14, 124, 65, 67`).
    * Alternatively, click the "Import CSV" button to load requests from a CSV file (the first row should contain comma-separated integers).
    * Ensure requests are non-negative and within the disk size range.

3.  **Enter Initial Head Position:**
    * Enter the starting track number for the disk head (e.g., `53`).
    * Ensure the position is non-negative and within the disk size range.

4.  **Enter Disk Size:**
    * Enter the total number of tracks on the disk (e.g., `200` for tracks 0 to 199).
    * Ensure the size is a positive integer.

5.  **Run Simulation:**
    * Click the "RUN SIMULATION & COMPARE" button.
    * The results (total movement, average seek time, throughput) and the sequence of track visits will appear in the respective text areas.

6.  **Visualize Movement:**
    * After running the simulation, check the boxes next to the algorithms you want to visualize. You can use "Select All" or "Clear Selection".
    * Click the "VISUALIZE SELECTED" button.
    * A new window will open displaying an animated plot of the disk head movement for the selected algorithms.

## File Structure

* `gui.py`: The main script containing the Tkinter GUI layout and logic. It connects the input, algorithms, and visualization.
* `algorithm_engine.py`: Contains the implementations of the FCFS, SSTF, SCAN, and C-SCAN algorithms.
* `visualization_module.py`: Handles the creation of Matplotlib plots and animation for the disk head movement.
* `input_module.py`: (Included in the code but not directly used by the GUI's main input fields; serves as a potential command-line input helper or reference).
* `requirements.txt`: Lists the necessary Python dependencies.
* `README.md`: This file, providing an overview and instructions.

## Screenshots

![image](https://github.com/user-attachments/assets/c21a4a59-df0b-408a-adaa-c33ce54bd2ab)
![image](https://github.com/user-attachments/assets/3a2b35c5-654a-46b4-85d1-13793e2c717e)
![image](https://github.com/user-attachments/assets/552c9551-d940-451e-ab57-d0ed549f874c)
![image](https://github.com/user-attachments/assets/0eeb8d00-2ec4-4434-92a2-68ae2bdcd335)

## License

*N/A*

## Acknowledgements

* Based on common disk scheduling algorithm concepts taught in operating systems courses.
* Uses the `sv_ttk` library for a modern Tkinter theme.
