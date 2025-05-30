# Data Structures Projects – CS3345 Spring 2025

A collection of three Python projects from CS3345 at UT Dallas.

---

## Project 1: Splay Tree (CLI)

**Files:** `Proj_1.py`, `ExtraCredit.txt`  
Implements a bottom-up splay tree with:
- `insert(key)`, `delete(key)`, `search(key)`  
- Preorder print using `kRT` / `kL` / `kR`  
- ExtraCredit.txt contains one-pass (top-down) splay pseudocode  

---

## Project 2: Sorting & Benchmark (CLI)

**Files:** `sorting_algos.py`, `benchmark.py`  
- **Mergesort** (iterative)  
- **Quicksort** (median-of-three + cutoff = 15)  
- `benchmark.py` tests random vs. nearly-sorted arrays (sizes 1K/5K/10K) and prints timing results  

---

## Project 3: Maze Generator & Solver

**Files:** `Maze.py`, `Maze_wPen.py`, `GUI.py`  

- `Maze.py`  
  - DFS maze generator  
  - BFS solver → direction string (e.g. “SENW”)  

- `Maze_wPen.py`  
  - Dijkstra’s solver with wall-knock penalties  
  - ASCII output + penalty report  

- `GUI.py`  
  - Tkinter GUI to draw the maze  
  - “Solve” button highlights path and shows directions  

---

## How to Run

Make sure you have Python 3 and `tkinter` installed. `tkinter` is native to python. 
