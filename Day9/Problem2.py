input_file_path = "Day9/input.txt"

f = open(input_file_path, "r")
lines = f.read().splitlines()

sum = 0
for line in lines:
    sequence = line.split(" ")
    sequence = [int(elem) for elem in sequence]

    # List where the first line is the input sequence and all the others are the sequences of differences of the previous line
    # We keep creating these sequences of differences until all the values are 0
    differences = [sequence]
    while not all(elem == 0 for elem in differences[-1]):
        current_differences = differences[-1]
        differences.append([current_differences[i+1] - current_differences[i] for i in range(len(current_differences)-1)])
    
    # We add a 0 at the beginning of the last sequence of differences and extrapolate the values backward, 
    # going up in the lines of differences by substracting the last value of the next line from the last value of the current one
    differences[-1].insert(0,0)
    for i in range(len(differences)-2, -1, -1):
        differences[i].insert(0,differences[i][0] - differences[i+1][0])
    
    sum += differences[0][0]

print(sum)    
