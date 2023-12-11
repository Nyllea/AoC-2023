input_file_path = "Day10/input.txt"

starting_symbol = 'S'
ground_symbol = '.'

f = open(input_file_path, "r")
lines = f.read().splitlines()

line_len = len(lines[0])
line_nbr = len(lines)
direction_dict = {'|':(-line_len, line_len), '-':(-1,1), 'L':(-line_len,1), 'J':(-line_len,-1), '7':(line_len,-1), 'F':(line_len,1)}

# Useful function to quicly visualize a map of pipes, and some specific points on it
def print_loop(loop_dict, special_pos_ids=[]):
    for i in range(line_nbr):
        line_str = ""
        for j in range(line_len):
            pos = i * line_len + j
            if pos in special_pos_ids:
                line_str += '+'
            elif pos in loop_dict:
                line_str += 'O'
            else:
                line_str += '.'
        print(line_str)


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
    cells[starting_cell_nbr] = connected_cells_directions

# Remove all cells not in the main loop as well as the cells '-'
# To do so, we go through all the elements connected to the starting cell,
# followinf the loop, and add them to main_loop if they are not '-'
main_loop = dict()
current_cell = starting_cell_nbr
previous_cell = -1
back_to_start = False
while not back_to_start:
    current_cell_directions = cells[current_cell]
    
    if current_cell_directions != direction_dict['-']:
        main_loop[current_cell] = current_cell_directions

    for current_direction in current_cell_directions:
        adjacent_cell = current_cell + current_direction
        
        # If the adjacent cell is not on the same line or on the same column as the current cell
        if not (adjacent_cell%line_len == current_cell % line_len or adjacent_cell//line_len == current_cell//line_len):
            continue

        if adjacent_cell not in cells:
            print("The cell ", current_cell, " points to the ground cell ", adjacent_cell)
            continue

        if adjacent_cell != previous_cell:
            previous_cell = current_cell
            current_cell = adjacent_cell
            break
    
    back_to_start = current_cell == starting_cell_nbr

# Sort the main loop by cell number to ensure that we will go through it 
# line by line in the next loop
sorted_main_loop = dict(sorted(main_loop.items()))

# We can now determine the amount of tiles inside the main loop
in_the_loop = False # True if the distance between the previous and the current cell is inside the main loop
tiles_in_loop = 0 # Number of tiles inside the main loop
previous_cell = next(iter(sorted_main_loop)) # linear index of the cell previously met in the main loop
previous_cell_dir = sorted_main_loop[previous_cell] # The corresponding directions

# Go through the cells of the main loop (that are not '-') line by line, from left to right
for cell_nbr, cell_dir in sorted_main_loop.items():
    # If we're not on the same line, then the tiles between the previous and current cells are not in the loop
    if cell_nbr//line_len != previous_cell//line_len:
        in_the_loop = False
        
    # If the previous cell is on the same line as the current one
    else:
        # If the positions between the two cells is not a line of '-'
        if cell_dir == direction_dict['|'] or previous_cell_dir == direction_dict['|'] or cell_dir[1] > previous_cell_dir[1]:
            dist_from_previous_cell = cell_nbr - previous_cell - 1

            if dist_from_previous_cell > 0 and in_the_loop:
                tiles_in_loop += dist_from_previous_cell
        
        # If we are in a situation with L7 or FJ, then we alternate between inside and outside the loop
        elif cell_dir != direction_dict['|'] and cell_dir[0] == -previous_cell_dir[0]:
            in_the_loop = not in_the_loop

    # If the current cell is a '|', then we alternate between inside and outside the loop
    if cell_dir == direction_dict['|']:
        in_the_loop = not in_the_loop

    previous_cell = cell_nbr
    previous_cell_dir = cell_dir

print(tiles_in_loop)