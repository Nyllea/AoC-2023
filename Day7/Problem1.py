input_file_path = "Day7/input.txt"

card_dict = {"A":14, 'K':13, 'Q':12, 'J':11, 'T':10}

# A class representing a card, allowing to compare them (operators < and !=)
class Card:
    def __init__(self, card_str):
        self.value_char = card_str
      
        if card_str.isdigit():
            self.value_num = int(card_str)
        else:
            self.value_num = card_dict[card_str]
    
    def __lt__(self, other):
        return self.value_num < other.value_num
    
    def __ne__(self, other):
        return self.value_num != other.value_num

# A class representing a hand of cards, allowing to compare them (operator <)
class Hand:
    # cards_str: the string corresponding to all the cards in the hand (in order)

    # bod_amount: the bid corresponding to this hand
    # hand_cards: ordered list of all the cards in hand
    # type_value: value of the type, the higher the value, the higher rank the type

    def __init__(self, hand_cards_str, bid_amount):
        self.cards_str = hand_cards_str
        self.bid_amount = bid_amount

        self.hand_cards = [Card(hand_cards_str[i]) for i in range(len(hand_cards_str))]

        # Dictionary with every card type in the hand as a key, and the number of this card in the hand as a value
        cards_amount_dict = dict()
        for card in self.hand_cards:
            if card.value_char in cards_amount_dict:
                cards_amount_dict[card.value_char] += 1
            else:
                cards_amount_dict[card.value_char] = 1
    
        # We attribute an arbitrary value to the type of the hand (self.type_value), the higher the value, the stronger the hand
        amount_card_type = len(cards_amount_dict)
        if amount_card_type == 1: # Five of a kind
            self.type_value = 6

        elif amount_card_type == 2: # Four of a kind or full house
            first_card = self.hand_cards[0]
            nbr_first_card = cards_amount_dict[first_card.value_char]

            if nbr_first_card == 4 or nbr_first_card == 1: # Four of a kind
                self.type_value = 5
            else: # Full house
                self.type_value = 4

        elif amount_card_type == 3: # Three of a kind or two pair
            max_card_amount = max(cards_amount_dict.values())
            if max_card_amount == 3: # Three of a kind
                self.type_value = 3
            else: # Two pair
                self.type_value = 2
        
        elif amount_card_type == 4: # One pair
            self.type_value = 1
        
        else: # High card
            self.type_value = 0

    # The operator <
    def __lt__(self, other):
        # First compare the types of the hands
        is_less_than = self.type_value < other.type_value

        # If the types are equal, compare the cards one by one, in order
        if self.type_value == other.type_value:
            for i in range(len(self.hand_cards)):
                if self.hand_cards[i] != other.hand_cards[i]:
                    is_less_than = self.hand_cards[i] < other.hand_cards[i]
                    break
        
        return is_less_than


f = open(input_file_path, "r")
lines = f.read().splitlines()

# Ordered list containing all the hands in the game, from weakest to strongest
all_hands = []

for line in lines:
    line_elements = line.split(" ")
    hand_cards_str = line_elements[0]
    bid_amount = int(line_elements[1])

    hand = Hand(hand_cards_str, bid_amount)

    # Insert the hand in the list all_hands while keeping it ordered
    hand_inserted = False
    for i in range(len(all_hands)):
        if hand < all_hands[i]:
            all_hands.insert(i, hand)
            hand_inserted = True
            break
    
    if not hand_inserted:
        all_hands.append(hand)

# Calculate the total winnings of the game
total_winnings = 0
for i in range(len(all_hands)):
    total_winnings += (i+1) * all_hands[i].bid_amount

print(total_winnings)
