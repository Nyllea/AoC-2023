input_file_path = "Day4/input.txt"

f = open(input_file_path, "r")
lines = f.read().splitlines()

points = 0
for line in lines:
    card = line.split(":")
    card_numbers = card[-1].split("|")

    # Get the list of numbers ans winning numbers
    winning_numbers = card_numbers[0].split(" ")
    numbers = card_numbers[-1].split(" ")

    # Calculate the number of numbers that are winning numbers
    number_of_match = 0
    for number in numbers:
        if number.isdigit() and number in winning_numbers:
            number_of_match += 1
    
    # Calculate the number of points from this card and add it to the total
    if number_of_match > 0:
        points += 2**(number_of_match-1)

print(points)