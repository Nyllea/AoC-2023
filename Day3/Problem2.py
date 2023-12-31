input_file_path = "Day3/input.txt"

f = open(input_file_path, "r")
lines = f.read().splitlines()

vert_size = len(lines)

sum = 0
for i in range(vert_size):
    horiz_size = len(lines[i])
    for j in range(horiz_size):
        char = lines[i][j]

        if char == '*':
            adjacent_numbers = [] 
            visited_number_start = [] # A list of the coordinates of the beginning of all the numbers already taken into account (to avoid duplicates)
            for vert_offset in [-1, 0, 1]:
                for horiz_offset in [-1, 0, 1]:
                    new_i = i + vert_offset
                    new_j = j + horiz_offset

                    if new_i < vert_size and new_j < horiz_size:
                        valid_char = lines[new_i][new_j]

                        # If the character around the symbol at (i,j) is a digit
                        if valid_char.isdigit():
                            full_number = ''

                            # Look for the beginning of the number and add the digits to full_number as we find them
                            number_index = new_j
                            current_char = valid_char
                            while current_char.isdigit():
                                full_number = current_char + full_number

                                number_index -= 1
                                if number_index < 0:
                                    break
                                current_char = lines[new_i][number_index]
                            
                            # Check if that number has already been seen before around that symbol and if not, add it to visited_number_start
                            number_start_coord = (number_index + 1, new_i)
                            if number_start_coord in visited_number_start:
                                break
                            else:
                                visited_number_start += [number_start_coord]

                            # Look for the end of the number and add the digits to full_number as we find them
                            number_index = new_j + 1
                            if number_index < horiz_size:
                                current_char = lines[new_i][number_index]
                                while current_char.isdigit():
                                    full_number = full_number + current_char

                                    number_index += 1
                                    if number_index >= horiz_size:
                                        break
                                    current_char = lines[new_i][number_index]

                            full_number = int(full_number)
                            adjacent_numbers += [full_number]
            
            # If there are exactly two numbers adjacent to the '*' character
            if len(adjacent_numbers) == 2:
                gear_ratio = adjacent_numbers[0] * adjacent_numbers[1]
                sum += gear_ratio

print(sum)
