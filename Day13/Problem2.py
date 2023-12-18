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

    # All the possible horizontal and vertical lines
    possible_horizontal_lines = []
    possible_vertical_lines = []
    
    # Check, for each horizontal line, that it would be valid for exactly one smudge
    # and add it to possible_horizontal_lines if it is
    for current_horizontal_line in range(1, nbr_columns):
        is_current_line_possible = True # True if the current line could be a mirror line with one smudge
        smudge_corrected = False # True if a smudge has been taken into consideration for this miror line

        for i in range(nbr_rows):
            # Determine the first column that needs to be checked so that the reflection is still inside the pattern
            min_column_to_check = max(0, 2*current_horizontal_line-nbr_columns)

            for j in range(min_column_to_check, current_horizontal_line):
                if pattern[i][j] != pattern[i][2*current_horizontal_line-1-j]:
                    # If a reflection don't match and a smudge has already been taken into account
                    # then the line is not a miror line
                    if smudge_corrected:
                        is_current_line_possible = False
                        break

                    # If a reflection don't match but no smudge has been taken into account,
                    # then take this mismatch as a smudge
                    else:
                        smudge_corrected = True

            # If the line needs at least 2 correction to be considered a miror line, then it is not one
            # We can stop verifying the rest of the positions
            if not is_current_line_possible:
                break
        
        # If exactly one smudge has been needed for this line to be a mirror line, then add it to possible_horizontal_lines
        if is_current_line_possible and smudge_corrected:
            possible_horizontal_lines.append(current_horizontal_line)


    # Do exactly the same as before, with vertical lines

    # Check, for each horizontal line, that it would be valid for exactly one smudge
    # and add it to possible_horizontal_lines if it is
    for current_vertical_line in range(1, nbr_rows):
        is_current_line_possible = True # True if the current line could be a mirror line with one smudge
        smudge_corrected = False # True if a smudge has been taken into consideration for this miror line

        for j in range(nbr_columns):
            # Determine the first row that needs to be checked so that the reflection is still inside the pattern
            min_row_to_check = max(0, 2*current_vertical_line-nbr_rows)

            for i in range(min_row_to_check, current_vertical_line):
                if pattern[i][j] != pattern[2*current_vertical_line-1-i][j]:
                    # If a reflection don't match and a smudge has already been taken into account
                    # then the line is not a miror line
                    if smudge_corrected:
                        is_current_line_possible = False
                        break

                    # If a reflection don't match but no smudge has been taken into account,
                    # then take this mismatch as a smudge
                    else:
                        smudge_corrected = True

            # If the line needs at least 2 correction to be considered a miror line, then it is not one
            # We can stop verifying the rest of the positions
            if not is_current_line_possible:
                break
        
        # If exactly one smudge has been needed for this line to be a mirror line, then add it to possible_vertical_lines
        if is_current_line_possible and smudge_corrected:
            possible_vertical_lines.append(current_vertical_line)
    

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