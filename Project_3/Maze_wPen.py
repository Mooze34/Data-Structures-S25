# MXA 220164
# Mustafa Alawad
# CS 3345.009
# Project 3

"""
run time analysis 
---------------------------
n, m dims → N = n * m
each cell = node, walls = edges (≤ 4 per node)
use Dijkstra’s algorithm with a binary heap:
  • heap ops (extract-min/decrease-key) cost O(log N)
  • ~N extracts + ~4N relaxations
  total time ≈ (N + 4N) * log N = O(N log N)
space usage: storing grid + heap = O(N)
"""

import random  # for generating random numbers and choices
import heapq   # lib for heap queue algorithms (priority queue) 

# Wall bitmasks - each bit represents a different wall direction
WALL_N, WALL_S, WALL_E, WALL_W = 1, 2, 4, 8
# Maps a wall to its opposite side - when we knock down a wall, gotta do both sides
OPPOSITE = {
    WALL_N: WALL_S,
    WALL_S: WALL_N,
    WALL_E: WALL_W,
    WALL_W: WALL_E
}
# Movement info: (dx, dy, which wall to check, letter for output)
DIRS = [
    (0, -1, WALL_N, 'N'),  # move north
    (0,  1, WALL_S, 'S'),  # move south
    (1,  0, WALL_E, 'E'),  # move east
    (-1, 0, WALL_W, 'W'),  # move west
]

def generate_maze(width, height):
    """
    Creates a random maze using depth-first search.
    Starts with all walls up, then carves passages by knocking down walls
    between adjacent cells, ensuring all cells are reachable.
    Returns a 2D grid representing the maze structure.
    """
    # Start with all walls up (15 = all 4 walls)
    maze = [[WALL_N | WALL_S | WALL_E | WALL_W for _ in range(width)]
            for _ in range(height)]
    stack = [(0, 0)]    # DFS stack starting at top-left
    visited = {(0, 0)}  # Track cells we've been to
    while stack:
        x, y = stack[-1]  # Peek at current cell
        neigh = []        # Find unvisited neighbors
        for dx, dy, wall, _ in DIRS:
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height and (nx, ny) not in visited:
                neigh.append((nx, ny, wall))
        if neigh:
            # Pick random neighbor, knock down the wall between them
            nx, ny, wall = random.choice(neigh)
            maze[y][x]    &= ~wall             # Remove wall in current cell
            maze[ny][nx]  &= ~OPPOSITE[wall]   # Remove opposite wall in neighbor
            visited.add((nx, ny))              # Mark as visited
            stack.append((nx, ny))             # Continue DFS from neighbor
        else:
            stack.pop()  # Backtrack if no unvisited neighbors
    return maze

def solve_maze_penalty(maze, penalty):
    """
    Solves the maze using Dijkstra's algorithm with a wall-breaking penalty.
    Finds the shortest path from top-left to bottom-right, where breaking
    a wall incurs the specified penalty cost. Returns both the path coordinates
    and a list of walls that were knocked down during traversal.
    """
    height, width = len(maze), len(maze[0])
    start, goal = (0, 0), (width-1, height-1)  # Start top-left, end bottom-right
    dist   = {start: 0}      # Cost to reach each cell
    parent = {start: None}   # For reconstructing path
    knocked= {}              # Track where we knocked down walls
    pq     = [(0, start)]    # Priority queue for Dijkstra's

    while pq:
        cost, (x, y) = heapq.heappop(pq)  # Get cheapest path so far
        if cost > dist[(x, y)]:           # Skip outdated entries
            continue
        if (x, y) == goal:                # Exit if we reached the goal
            break
        for dx, dy, wall, _ in DIRS:      # Try all four directions
            nx, ny = x + dx, y + dy
            if not (0 <= nx < width and 0 <= ny < height):
                continue                   # Skip out of bounds
            extra = penalty if (maze[y][x] & wall) else 0  # Apply penalty if wall exists
            new_cost = cost + extra
            if new_cost < dist.get((nx, ny), float('inf')):  # Found better path
                dist[(nx, ny)] = new_cost
                parent[(nx, ny)] = (x, y)
                knocked[(nx, ny)] = bool(maze[y][x] & wall)  # Remember if we knocked
                heapq.heappush(pq, (new_cost, (nx, ny)))

    # Trace path backwards from goal to start
    path, knocks = [], []
    node = goal
    while node:
        path.append(node)
        prev = parent.get(node)
        if prev and knocked.get(node):  # If we knocked a wall here
            dx, dy = node[0]-prev[0], node[1]-prev[1]
            for ddx, ddy, _, dchar in DIRS:
                if (dx, dy) == (ddx, ddy):
                    knocks.append((prev, dchar))  # Record which wall was knocked
                    break
        node = prev
    path.reverse()
    knocks.reverse()
    return path, knocks

def path_to_directions(path):
    """
    Converts a coordinate-based path to a string of direction characters.
    Takes a list of (x,y) coordinates and translates each step to N, E, S, or W
    based on the movement direction between consecutive points.
    """
    # Convert coordinate path to NESW string
    s = []
    for (x1,y1),(x2,y2) in zip(path, path[1:]):
        if x2==x1+1:   s.append('E')
        elif x2==x1-1: s.append('W')
        elif y2==y1+1: s.append('S')
        elif y2==y1-1: s.append('N')
    return ''.join(s)

def draw_maze_ascii(maze, path=None):
    """
    Renders the maze as ASCII art in the console.
    Displays walls as lines and borders, and optionally highlights
    the solution path with asterisks (*). Provides a visual representation
    of the maze structure and the found path.
    """
    # Convert maze to ASCII art with path marked by *
    height, width = len(maze), len(maze[0])
    path_set = set(path) if path else set()

    # Draw top border
    line = '+'
    for x in range(width):
        line += '---+' if (maze[0][x] & WALL_N) else '   +'
    print(line)

    for y in range(height):
        # Draw cell contents and vertical walls
        row = ''
        for x in range(width):
            row += '|' if (maze[y][x] & WALL_W) else ' '  # Left wall
            row += ' * ' if (x,y) in path_set else '   '  # Cell content
        row += '|'   # Right edge of maze
        print(row)

        # Draw horizontal walls below this row
        sep = '+'
        for x in range(width):
            sep += '---+' if (maze[y][x] & WALL_S) else '   +'
        print(sep)

def main():
    """
    Main program function that drives the maze generation and solving process.
    Gets user input for maze dimensions and penalty value, generates a random maze,
    solves it with the specified wall-breaking penalty, and displays the result
    with the optimal path and details about knocked-down walls.
    """
    # Get input, with lazy error handling
    try:
        w = int(input("Maze width: "))
        h = int(input("Maze height: "))
        p = int(input("Wall-knock penalty P (>0): "))
    except ValueError:
        print("Please enter three integers.")
        return

    maze = generate_maze(w, h)  # Make random maze
    path, knocks = solve_maze_penalty(maze, p)  # Solve it
    dirs = path_to_directions(path)  # Get directions

    # Print results
    print(f"\nHere's your maze with the optimal path (*) under penalty P = {p}\n")
    draw_maze_ascii(maze, path)

    print("Path directions:", dirs)
    print("Walls knocked down along path:")
    if knocks:
        for (x,y), d in knocks:
            print(f"  at ({x},{y}) knock to the {d}")
    else:
        print("  None  (the path uses only existing corridors)")
    
if __name__ == '__main__':
    main()
