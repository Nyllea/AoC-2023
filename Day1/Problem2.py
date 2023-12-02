import re

input_file_path = "Day1\input.txt"

# Association of the text and arabic numbers
numbers_assoc = [("one", "1"), ("two", "2"), ("three", "3"), ("four", "4"), ("five", "5"), ("six", "6"), ("seven", "7"), ("eight", "8"), ("nine", "9")]

# Creation of the regex expression to detect numbers in both text and arabic form
reg_exp = "("
for (str_val, num_val) in numbers_assoc:
    reg_exp += str_val + "|"
reg_exp += "[0-9])"

f = open(input_file_path, "r")
lines = f.read().splitlines()

sum = 0
for line in lines:
    # Search the line for any match, and repeating the process by removing characters one by one
    # This is used to detect cases like twone as two one, or oneight as one eight
    matches = []
    for i in range(len(line)):
        first_match = re.search(reg_exp, line[i:], re.IGNORECASE)
        if first_match != None:
            matches += [first_match.group()]

    # Concatenation of the first and last match, and conversion to arabic notation
    value = matches[0] + matches[-1]
    for (str_val, num_val) in numbers_assoc:
        value = re.sub(str_val, num_val, value, flags=re.IGNORECASE)

    sum += int(value)

print(sum)
