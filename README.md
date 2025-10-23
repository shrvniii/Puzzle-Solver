Puzzle Solver — Backtracking vs Branch & Bound

Project Overview
This project demonstrates and compares two classical search and optimization algorithms — Backtracking and Branch & Bound — by applying them to solve a puzzle problem efficiently.
It visualizes how each algorithm explores possible solutions and compares their accuracy, execution time, and efficiency within a graphical interface.

Features
Solves a 6x6 puzzle using both algorithms.
Displays solution path, steps, and execution time for each method.
Provides a side-by-side comparison of performance metrics.
Uses an interactive Tkinter GUI for clarity and visualization.
Highlights algorithmic differences through live computation results.

Technologies Used
Language	Python 
Libraries 3
IDE	PyCharm
GUI	Tkinter
Algorithms	Backtracking, Branch and Bound
Concepts	Recursion, Heuristic Search, Time Comparison

Algorithms Used
1. Backtracking
Explores all possible states recursively.
Backtracks when a path leads to an invalid or suboptimal solution.
Ensures accuracy but may take longer for larger problem spaces.

2. Branch and Bound
Uses a bounding function to eliminate non-promising states early.
Employs a Priority Queue to expand the most promising nodes first.
Produces the same solution faster in most cases.

Performance Comparison
At the end of execution, the GUI displays:
Execution time for both algorithms
Success or failure messages
Comparison summary (which method solved it faster)
This allows users to visually understand how optimization techniques affect runtime and efficiency.

How to Run
Open in PyCharm
Navigate to your project folder and open the .py file.
Install Required Libraries

pip install tk


Run the Program
Press Run in PyCharm.
The Tkinter window will open.
View Output
The panel shows puzzle results and time taken by each algorithm.

Example Output
Backtracking: Solved in 2.13s
Branch & Bound: Solved in 0.47s
Faster Algorithm: Branch & Bound

