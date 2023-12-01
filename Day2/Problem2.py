input_file_path = "Day2/test.txt"

f = open(input_file_path, "r")
lines = f.read().splitlines()

for line in lines:
    print(line)