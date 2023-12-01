import re

input_file_path = "Day1\input_1.txt"

f = open(input_file_path, "r")
lines = f.read().splitlines()

sum = 0
for line in lines:
    numbers = re.sub("[^0-9]","",line)
    n1 = re.search("^[0-9]", numbers).group()
    n2 = re.search("[0-9]$", numbers).group()
    #print(numbers, " - ", n1, ":", n2, " - ", n1+n2)
    sum += int(n1 + n2)

print(sum)