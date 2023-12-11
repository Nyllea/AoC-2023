import numpy as np

input_file_path = "Day11/input.txt"

galaxy_symbol = '#'

f = open(input_file_path, "r")
lines = f.read().splitlines()

line_len = len(lines[0])
line_nbr = len(lines)

# Lists containing the rows and colums without any galaxy (ie that need to be expanded)
columns_expanded = [i for i in range(line_len)]
rows_expanded = [i for i in range(line_nbr)]

# List containing the coordinates of all the galaxies
galaxies = []

# We go through the file line by line and add the galaxies to 'galaxies' while actualizing the expanded rows/columns
current_row = 0
for line in lines:
    current_column = 0
    for char in line:
        if char == galaxy_symbol:
            galaxies += [np.array([current_row, current_column])]

            columns_expanded = [col for col in columns_expanded if col != current_column]
            rows_expanded = [row for row in rows_expanded if row != current_row]

        current_column += 1
    current_row += 1


# We can now determine the distance between each pair of galaxies
nbr_galaxies = len(galaxies)
sum_distances = 0
for galaxy_id in range(nbr_galaxies):
    current_galaxy = galaxies[galaxy_id]

    # For each galaxy, we look at all the galaxies with a lower index (to avoid repeating pairs)
    for other_galaxy in galaxies[galaxy_id + 1:]:
        # We can then calculate the distance between these galaxies
        distance_vector = other_galaxy - current_galaxy
        distance = abs(distance_vector[0]) + abs(distance_vector[1])

        # Finally, for each expanded rows and columns the shortest path passes through, we add one to the distance
        for expanded_row_id in rows_expanded:
            if expanded_row_id > current_galaxy[0] and expanded_row_id < other_galaxy[0]:
                distance += 1
        
        for expanded_col_id in columns_expanded:
            if (expanded_col_id > current_galaxy[1] and expanded_col_id < other_galaxy[1]) or (expanded_col_id < current_galaxy[1] and expanded_col_id > other_galaxy[1]):
                distance += 1

        sum_distances += distance

print(sum_distances)