input_file_path = "Day4/input.txt"

f = open(input_file_path, "r")
lines = f.read().splitlines()

number_of_cards = [1 for _ in range(len(lines))]
for line in lines:
    card = line.split(":")
    card_id = int(card[0].split(" ")[-1])
    card_numbers = card[-1].split("|")
    winning_numbers = card_numbers[0].split(" ")
    numbers = card_numbers[-1].split(" ")

    number_of_match = 0
    for number in numbers:
        if number.isdigit() and number in winning_numbers:
            number_of_match += 1
    
    for i in range(number_of_match):
        number_of_cards[card_id+i] += number_of_cards[card_id-1]

total_card_amount = sum(number_of_cards)
print(total_card_amount)