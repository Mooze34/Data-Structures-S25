# MXA 220164
# Mustafa Alawad
# CS 3345.009
# Project 3


import random
from collections import deque

# Bitmasks for walls - each number represents a wall direction
WALL_N, WALL_S, WALL_E, WALL_W = 1, 2, 4, 8
# Maps each wall to its opposite direction (for when we carve passages)
OPPOSITE = {
    WALL_N: WALL_S,
    WALL_S: WALL_N,
    WALL_E: WALL_W,
    WALL_W: WALL_E
}
# Movement directions: (x change, y change, wall to remove, direction char)
DIRS = [
    (0, -1, WALL_N, 'S'),  # go south (y decreases)
    (0,  1, WALL_S, 'N'),  # go north (y increases)
    (1,  0, WALL_E, 'W'),  # go east (x increases)
    (-1, 0, WALL_W, 'E'),  # go west (x decreases)
]

def generate_maze(width, height):
    """
    Generate a perfect maze of size width x height using DFS.
    Returns a 2D list of bitmasks for wall presence in each cell.
    """
    # Start with all walls up (15 = all 4 walls)
    maze = [[WALL_N | WALL_S | WALL_E | WALL_W for _ in range(width)]
            for _ in range(height)]
    stack = [(0, 0)]  # Start at top-left corner
    visited = {(0, 0)}  # Keep track of cells we've already handled

    # DFS maze generation - keep going until we've visited all cells
    while stack:
        x, y = stack[-1]  # Get current position (top of stack)
        neighbors = []
        # Check all 4 directions for unvisited neighbors
        for dx, dy, wall, _ in DIRS:
            nx, ny = x + dx, y + dy
            if (0 <= nx < width and 0 <= ny < height
                    and (nx, ny) not in visited):
                neighbors.append((nx, ny, wall))
        
        if neighbors:
            # Pick random unvisited neighbor
            nx, ny, wall = random.choice(neighbors)
            # Knock down walls between current cell and chosen neighbor
            maze[y][x] ^= wall  # XOR to remove the wall bit
            maze[ny][nx] ^= OPPOSITE[wall]  # Remove opposite wall in neighbor
            visited.add((nx, ny))  # Mark neighbor as visited
            stack.append((nx, ny))  # Move to neighbor
        else:
            # No unvisited neighbors, backtrack
            stack.pop()
    return maze

def solve_maze(maze):
    """
    Find the shortest path from (0,0) to bottom-right using BFS.
    Returns a list of (x, y) coordinates.
    """
    height, width = len(maze), len(maze[0])
    start, goal = (0, 0), (width - 1, height - 1)
    q = deque([start])  # Queue for BFS
    parents = {start: None}  # Track path for reconstruction

    # BFS until we find the goal
    while q:
        x, y = q.popleft()
        if (x, y) == goal:
            break  # Found the exit, we're done!
        
        # Try all four directions
        for dx, dy, wall, _ in DIRS:
            nx, ny = x + dx, y + dy
            # If in bounds, no wall, and not visited yet
            if (0 <= nx < width and 0 <= ny < height
                    and not (maze[y][x] & wall)  # Bitwise check if wall exists
                    and (nx, ny) not in parents):
                q.append((nx, ny))
                parents[(nx, ny)] = (x, y)  # Remember how we got here

    # Reconstruct path from goal to start
    path = []
    node = goal
    while node:
        path.append(node)
        node = parents.get(node)

    return list(reversed(path))  # Return path from start to goal

def path_to_directions(path):
    """
    Convert a sequence of coordinates to compass directions (NSEW).
    Makes it easier to follow the solution.
    """
    dirs = []
    # Compare each pair of adjacent positions
    for (x1, y1), (x2, y2) in zip(path, path[1:]):
        if x2 == x1 + 1:
            dirs.append('E')  # Moving right
        elif x2 == x1 - 1:
            dirs.append('W')  # Moving left
        elif y2 == y1 + 1:
            dirs.append('S')  # Moving down
        elif y2 == y1 - 1:
            dirs.append('N')  # Moving up
    return ''.join(dirs)
