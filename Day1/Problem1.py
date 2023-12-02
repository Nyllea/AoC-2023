import re

input_file_path = "Day1\input.txt"

f = open(input_file_path, "r")
lines = f.read().splitlines()

sum = 0
for line in lines:
    # All the numbers in the line
    numbers = re.sub("[^0-9]","",line)

    # First number of the line
    n1 = re.search("^[0-9]", numbers).group()

    # Last number of the line
    n2 = re.search("[0-9]$", numbers).group()
    
    sum += int(n1 + n2)

print(sum)