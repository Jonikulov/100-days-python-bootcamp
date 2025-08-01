"""DAY 11. Blackjack Game."""

import random

BLACKJACK_ART = r"""
.------.            _     _            _    _            _    
|A_  _ |.          | |   | |          | |  (_)          | |   
|( \/ ).-----.     | |__ | | __ _  ___| | ___  __ _  ___| | __
| \  /|K /\  |     | '_ \| |/ _' |/ __| |/ / |/ _' |/ __| |/ /
|  \/ | /  \ |     | |_) | | (_| | (__|   <| | (_| | (__|   < 
'-----| \  / |     |_.__/|_|\__,_|\___|_|\_\ |\__,_|\___|_|\_\
      |  \/ K|                            _/ |                
      '------'                           |__/
"""
CARDS = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]

def deal_card() -> int:
    """Returns a random card from the deck"""
    return random.choice(CARDS)

def calculate_score(cards: list) -> int:
    """Take a list of cards and return the score calculated from the cards"""
    if sum(cards) == 21 and len(cards) == 2:
        return 0
    if sum(cards) > 21 and 11 in cards:
        cards[cards.index(11)] = 1
    return sum(cards)

def compare(u_score, c_score):
    if c_score == 0:
        return "YOU LOSE. Computer has Blackjack."
    elif u_score == 0:
        return "YOU WIN with Blackjack!"
    elif u_score > 21:
        return "YOU LOSE. You went over."
    elif c_score > 21:
        return "YOU WIN. Computer went over."
    elif u_score == c_score:
        return "TIE!"
    elif u_score > c_score:
        return "YOU WIN."
    else:
        return "YOU LOSE."

def play_blackjack():
    print(BLACKJACK_ART)
    user_cards = [deal_card() for _ in range(2)]
    computer_cards = [deal_card() for _ in range(2)]
    is_game_over = False
    user_score = calculate_score(user_cards)
    computer_score = calculate_score(computer_cards)

    while not is_game_over:
        print(f"\nYour cards: {user_cards}, current score: {user_score}")
        print(f"Computer's first card: {computer_cards[0]}")

        if computer_score == 0 or user_score == 0 or user_score > 21:
            is_game_over = True
        else:
            get_card = input("Type 'y' to get another card, "
                             "type 'n' to pass: ")
            if get_card == "y":
                user_cards.append(deal_card())
                user_score = calculate_score(user_cards)
            else:
                is_game_over = True

    # Computer's play
    while computer_score < 17 and computer_score != 0:
        computer_cards.append(deal_card())
        computer_score = calculate_score(computer_cards)

    print(f"\nYour final hand: {user_cards}, final score: {user_score}")
    print(f"Computer's final hand: {computer_cards}, "
          f"final score: {computer_score}")
    print(compare(user_score, computer_score))

while True:
    play_game = input("\nDo you want to play a game of Blackjack? [y/n]: ")
    if play_game in ["y", "yes"]:
        print("\033[2J\033[H", end="")  # Clears the screen
        play_blackjack()
    else:
        break
