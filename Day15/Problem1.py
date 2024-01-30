input_file_path = "Day15/input.txt"

f = open(input_file_path, "r")
lines = f.read().splitlines()

# Uses the given algorithm to calculate the hash value of the given string
def hash_algo(char_string):
    current_value = 0
    for character in char_string:
        current_value = ((current_value + ord(character)) * 17) % 256
    return current_value

hash_sum = 0
for line in lines:
    init_sequence = line.split(',')
    for step in init_sequence:
        hash_sum += hash_algo(step)

print(hash_sum)
