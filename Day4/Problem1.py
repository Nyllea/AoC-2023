input_file_path = "Day4/input.txt"

f = open(input_file_path, "r")
lines = f.read().splitlines()

points = 0
for line in lines:
    card = line.split(":")
    card_numbers = card[-1].split("|")
    winning_numbers = card_numbers[0].split(" ")
    numbers = card_numbers[-1].split(" ")

    number_of_match = 0
    for number in numbers:
        if number.isdigit() and number in winning_numbers:
            number_of_match += 1
    
    if number_of_match > 0:
        points += 2**(number_of_match-1)

print(points)