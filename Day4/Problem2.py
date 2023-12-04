input_file_path = "Day4/input.txt"

f = open(input_file_path, "r")
lines = f.read().splitlines()

# List containting the number of copies of each card we have
number_of_cards = [1 for _ in range(len(lines))]

for line in lines:
    card = line.split(":")
    card_id = int(card[0].split(" ")[-1])

    # This correspond to the number of the card as provided in the input, so 1 for the first card, 2 for the second and so on
    card_numbers = card[-1].split("|")

    # Get the list of numbers ans winning numbers
    winning_numbers = card_numbers[0].split(" ")
    numbers = card_numbers[-1].split(" ")

    # Calculate the number of numbers that are winning numbers
    number_of_match = 0
    for number in numbers:
        if number.isdigit() and number in winning_numbers:
            number_of_match += 1
    
    # For number_of_match cards following the current card, add one copy of that card for each copy of the current card
    # Which means adding the amount of copies of the current card to the amount of copies of these cards
    for i in range(number_of_match):
        number_of_cards[card_id+i] += number_of_cards[card_id-1]

# The result is the total amount of card we have, including the copies
total_card_amount = sum(number_of_cards)

print(total_card_amount)