input_file_path = "Day10/input.txt"

starting_symbol = 'S'
ground_symbol = '.'

f = open(input_file_path, "r")
lines = f.read().splitlines()

line_len = len(lines[0])
line_nbr = len(lines)
direction_dict = {'|':(-line_len, line_len), '-':(-1,1), 'L':(-line_len,1), 'J':(-line_len,-1), '7':(-1,line_len), 'F':(line_len,1)}

# Dictionary of all the cells containing a pipe, with the format: cell_nbr, (dir1, dir2)
# with cell_nbr the linear index of the cell in the terrain, 
# dir is a relative direction: -1 for left, 1 for right, -line_len for up and line_len for down
cells = dict()
current_cell_nbr = 0
starting_cell_nbr = -1
for line in lines:
    for char in line:
        if char == starting_symbol:
            starting_cell_nbr = current_cell_nbr
        elif char != ground_symbol:
            cells[current_cell_nbr] = direction_dict[char]
        
        current_cell_nbr += 1

# Determine the directions connected to the starting cell
connected_cells_directions = []
for dir in [-line_len, -1, line_len, 1]:
    if starting_cell_nbr+dir in cells:
        adjacent_cell = cells[starting_cell_nbr+dir]
        if adjacent_cell[0] == -dir or adjacent_cell[1] == -dir:
            connected_cells_directions.append(dir)

# Add that direction to the dictionnary 'cells' representing all the pipes
number_pipes_on_start = len(connected_cells_directions)
if number_pipes_on_start != 2:
    print("Error ! There is ", number_pipes_on_start, " pipes connected to the starting cell")
    exit()
else:
    cells[starting_cell_nbr] = tuple(connected_cells_directions)

# Using Breadth-first search, starting from the starting cell S
# The two branches of the search will meet at the farthest point from S
# So we need to stop when the same cell is met twice
all_cells_met = [starting_cell_nbr] # List of all the cells met
new_cells_met = [starting_cell_nbr] # List of all the cells met in the search but not yet searched
cell_met_twice = False
current_distance = 0 # Distance from the start
farthest_cell = -1 # Linear index of the farthest cell met

while not cell_met_twice:
    current_cells = new_cells_met
    new_cells_met = []
    current_distance += 1

    # For each cell met but not yet searched
    for current_cell in current_cells:
        current_cell_directions = cells[current_cell]

        all_adjacent_cells_met = True # True if all the cells next to the current_cell have already been met
        
        # For each directions the current cell points to
        for current_direction in current_cell_directions:
            adjacent_cell = current_cell + current_direction
            
            # If the adjacent cell is not on the same line or on the same column as the current cell
            # That means the current cell is at the border of the map and point outside of it
            if not (adjacent_cell%line_len == current_cell % line_len or adjacent_cell//line_len == current_cell//line_len):
                print("The cell ", current_cell, " points to the outside of the map")
                continue

            if adjacent_cell not in cells:
                print("The cell ", current_cell, " points to the ground cell ", adjacent_cell)
                continue

            if adjacent_cell not in all_cells_met:
                all_cells_met += [adjacent_cell]
                new_cells_met += [adjacent_cell]
                all_adjacent_cells_met = False
        
        if all_adjacent_cells_met:
            cell_met_twice = True
            farthest_cell = adjacent_cell
            break

print("Farthest cell is ", farthest_cell," = (", farthest_cell//line_len + 1, ", ", farthest_cell%line_len + 1, ") at a distance of ", current_distance, " from the start")
