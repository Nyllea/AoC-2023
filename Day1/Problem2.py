import re

input_file_path = "Day1\input.txt"
numbers_assoc = [("one", "1"), ("two", "2"), ("three", "3"), ("four", "4"), ("five", "5"), ("six", "6"), ("seven", "7"), ("eight", "8"), ("nine", "9")]


reg_exp = "("
for (str_val, num_val) in numbers_assoc:
    reg_exp += str_val + "|"
reg_exp += "[0-9])"

f = open(input_file_path, "r")
lines = f.read().splitlines()

sum = 0
for line in lines:
    matches = []
    for i in range(len(line)):
        first_match = re.search(reg_exp, line[i:], re.IGNORECASE)
        if first_match != None:
            matches += [first_match.group()]

    value = matches[0] + matches[-1]
    for (str_val, num_val) in numbers_assoc:
        value = re.sub(str_val, num_val, value, flags=re.IGNORECASE)
    
    #print(line, matches, matches[0], matches[-1], value)

    sum += int(value)

print(sum)
