input_file_path = "Day13/input.txt"

# Takes in a 2D list of 0 and 1 and returns the index of the mirror line that can fit in this pattern
# with as 2 integer, the first one correspond to horizontal lines and the second one to vertical lines,
# and 0 meaning no mirror line possible, i meaning a mirror line between the rows/columns of index i-1 and i
# ie with i rows/columns to the left/above it
def find_mirror_lines(pattern):
    nbr_rows = len(pattern)

    # Make sure the pattern is not empty
    if nbr_rows == 0:
        return 0,0
    
    nbr_columns = len(pattern[0])

    # Store all the possible horizontal and vertical lines
    possible_horizontal_lines = [i for i in range(1, nbr_columns)]
    possible_vertical_lines = [i for i in range(1, nbr_rows)]
    
    # Check, for each horizontal line, that it is a valid one
    # and remove it from possible_horizontal_lines if it is not
    for i in range(nbr_rows):
        new_horizontal_lines = []
        for current_horizontal_line in possible_horizontal_lines:
            # Determine the first column that needs to be checked so that the reflection is still inside the pattern
            min_column_to_check = max(0, 2*current_horizontal_line-nbr_columns)

            is_line_mirror = True
            for j in range(min_column_to_check, current_horizontal_line):
                if pattern[i][j] != pattern[i][2*current_horizontal_line-1-j]:
                    is_line_mirror = False
                    break

            # If the line is still valid as a mirror, add it to the actualized possible_horizontal_lines
            if is_line_mirror:
                new_horizontal_lines.append(current_horizontal_line)
        
        # Actualize the possible horizontal lines
        possible_horizontal_lines = new_horizontal_lines
    

    # Do exactly the same as before, with vertical lines
    
    # Check, for each vertical line, that it is a valid one
    # and remove it from possible_vertical_lines if it is not
    for j in range(nbr_columns):
        new_vertical_lines = []
        for current_vertical_line in possible_vertical_lines:
            # Determine the first row that needs to be checked so that the reflection is still inside the pattern
            min_row_to_check = max(0, 2*current_vertical_line-nbr_rows)

            is_line_mirror = True
            for i in range(min_row_to_check, current_vertical_line):
                if pattern[i][j] != pattern[2*current_vertical_line-1-i][j]:
                    is_line_mirror = False
                    break
                    
            # If the line is still valid as a mirror, add it to the actualized possible_vertical_lines
            if is_line_mirror:
                new_vertical_lines.append(current_vertical_line)

        # Actualize the possible vertical lines
        possible_vertical_lines = new_vertical_lines

    # Get the right horizontal/vertical line and return it
    # (if the input is well made, there should only be one value left in these lists)
    vertical_mirror = 0
    if len(possible_vertical_lines) > 0:
        vertical_mirror = possible_vertical_lines[0]
    
    horizontal_mirror = 0
    if len(possible_horizontal_lines) > 0:
        horizontal_mirror = possible_horizontal_lines[0]
    
    return horizontal_mirror, vertical_mirror

f = open(input_file_path, "r")
lines = f.read().splitlines()

# List of 0 and 1 representing the positions of the '#' (=1) and the '.' (=0) in the pattern
current_pattern = []
sum = 0

for line in lines:
    if line != "":
        current_pattern.append([0 if element == '.' else 1 for element in line])
    else:
        horizontal_line, vertical_line = find_mirror_lines(current_pattern)

        # The id of the line corresponds to the number of columns to it's left/number of rows above it
        sum += horizontal_line + vertical_line * 100

        current_pattern = []

# We find the mirror lines one last time, for the last pattern
horizontal_line, vertical_line = find_mirror_lines(current_pattern)
sum += horizontal_line + vertical_line * 100

print(sum)