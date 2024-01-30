input_file_path = "Day14/input.txt"

rounded_rock = 'O'
cube_rock = '#'
empty_space = '.'

f = open(input_file_path, "r")
lines = f.read().splitlines()

nbr_columns = len(lines[0])
nbr_rows = len(lines)

def partial_column_load(first_boulder_row, last_boulder_row):
    first_boulder_weight = nbr_rows - first_boulder_row  - 1
    last_boulder_weight = nbr_rows - last_boulder_row
    nbr_of_boulders = last_boulder_row - first_boulder_row

    return (first_boulder_weight + last_boulder_weight) * nbr_of_boulders // 2

last_cube_rock = [-1 for _ in range(nbr_columns)]
nbr_rounded_rocks = [0 for _ in range(nbr_columns)]

current_line = 0
total_load = 0

for line in lines:
    for i in range(nbr_columns):
        element = line[i]
        if element == cube_rock:
            total_load += partial_column_load(last_cube_rock[i], last_cube_rock[i]+nbr_rounded_rocks[i])

            last_cube_rock[i] = current_line
            nbr_rounded_rocks[i] = 0
        elif element == rounded_rock:
            nbr_rounded_rocks[i] += 1
    
    current_line += 1

for i in range(nbr_columns):
    total_load += partial_column_load(last_cube_rock[i], last_cube_rock[i]+nbr_rounded_rocks[i])

print(total_load)