# MXA 220164 
# Mustafa Alawad 
# CS 3345 Project 2 


import math  # Import math for gcd (needed in the algo)

def find_collinear_points(points):
    # Sort the list of points lexicographically (by x, then y)
    points = sorted(points)
    n = len(points)
    # Use a set to store unique groups of collinear points
    collinear_groups = set()

    # Iterate over all points as the "origin"
    for i in range(n):
        origin = points[i]
        slopes = {}  # Dictionary to map each normalized slope to points sharing that slope with origin
        # Compare the origin with every other point
        for j in range(n):
            if i == j:
                continue  # Skip comparing the origin to itself
            # Calculate differences in x and y coordinates
            dx = points[j][0] - origin[0]
            dy = points[j][1] - origin[1]
            
            # For vertical lines, set slope to (1, 0)
            if dx == 0:
                slope = (1, 0)
            # For horizontal lines, set slope to (0, 1)
            elif dy == 0:
                slope = (0, 1)
            else:
                # Compute the greatest common divisor for dx and dy
                g = math.gcd(dx, dy)
                # Normalize the differences
                ndx = dx // g
                ndy = dy // g
                # Ensure the normalized slope has a positive denominator
                if ndx < 0:
                    ndx, ndy = -ndx, -ndy
                # Use a tuple (ndy, ndx) to represent the normalized slope
                slope = (ndy, ndx)
            # Append the point to the list of points sharing this slope with origin
            slopes.setdefault(slope, []).append(points[j])
        
        # For each unique slope, check if enough points are collinear with the origin
        for slope, same_slope_points in slopes.items():
            # Group is valid if there are at least 3 points with the same slope (plus the origin makes 4)
            if len(same_slope_points) >= 3:
                # Create a sorted tuple representing the group of collinear points
                group = tuple(sorted([origin] + same_slope_points))
                # Only add the group if the origin is the smallest point to avoid duplicates
                if group[0] == origin:
                    collinear_groups.add(group)
    # Return the sorted list of unique collinear groups that have at least 4 points
    return sorted(collinear_groups)

if __name__ == '__main__':
    # Example list of points; you can modify this or read from a file as required.
    sample_points = [
        (10000, 0), (0, 10000), (3000, 7000), (7000, 3000),
        (20000, 21000), (3000, 4000), (14000, 15000), (6000, 7000),
        (1, 2), (2, 4), (3, 6), (4, 8),
        (10, 10), (20, 20), (30, 30), (40, 40)
    ]
    
    # Find collinear point groups among the sample points
    groups = find_collinear_points(sample_points)
    
    # Print out the results
    if groups:
        print("Collinear groups (4 or more points):")
        for group in groups:
            print(group)
    else:
        print("No collinear groups found.")