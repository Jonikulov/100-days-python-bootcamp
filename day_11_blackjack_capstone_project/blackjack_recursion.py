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

def play_blackjack(new_game=True, player_cards=None, bot_cards=None):
    """Plays Blackjack game, recursively."""

    def print_cards_scores(player_final=True, bot_final=True):
        pl_msg1 = "cards"
        pl_msg2 = "current"
        bot_msg = f"first card: {bot_cards[0]}"
        if player_final:
            pl_msg1 = "final hand"
            pl_msg2 = "final"
        if bot_final:
            bot_msg = f"final hand: {bot_cards}, final score: {bot_score}"
        print(f"\nYour {pl_msg1}: {player_cards}, "
              f"{pl_msg2} score: {player_score}")
        print(f"Computer's {bot_msg}")

    if new_game:
        play_game = input(
            "\nDo you want to play a game of Blackjack? [y/n]: "
        ).strip().lower()
        if play_game in ["n", "no"]:
            return None

        print("\033[2J\033[H", end="")  # Clears the screen
        print(BLACKJACK_ART, end="")
        player_cards = random.choices(CARDS, k=2)
        bot_cards = random.choices(CARDS, k=2)
        player_score = sum(player_cards)
        bot_score = sum(bot_cards)
        if player_score == 22:
            player_cards = [11, 1]
            player_score = 12
        if bot_score == 22:
            bot_cards = [11, 1]
            bot_score = 12

        print_cards_scores(False, False)
        is_blackjack = False
        if bot_score == 21:
            print_cards_scores()
            print("YOU LOSE. Computer has Blackjack.")
            is_blackjack = True
        elif player_score == 21:
            print_cards_scores()
            print("YOU WIN with Blackjack!")
            is_blackjack = True
        if is_blackjack:
            return play_blackjack()

    get_card = input("Type 'y' to get another card, type 'n' to pass: ")
    player_score = sum(player_cards)
    bot_score = sum(bot_cards)
    if get_card == "y":
        card = random.choice(CARDS)
        if (card == 11) and (card + player_score > 21):
            card = 1
        player_cards.append(card)
        player_score += card
        if player_score > 21:
            if 11 in player_cards and player_score - 10 <= 21:
                player_cards[player_cards.index(11)] = 1
                player_score -= 10
            else:
                print_cards_scores()
                print("YOU LOSE. You went over.")
                return play_blackjack()
        print_cards_scores(False, False)
        return play_blackjack(False, player_cards, bot_cards)

    # Computer must hit until score 17
    while bot_score < 17:
        card = random.choice(CARDS)
        if (card == 11) and (card + bot_score > 21):
            card = 1
        bot_cards.append(card)
        bot_score += card

    print_cards_scores()
    if bot_score > 21:
        print("YOU WIN! Computer went over.")
    elif player_score == bot_score:
        print("TIE!")
    elif player_score > bot_score:
        print("YOU WIN!")
    else:
        print("YOU LOSE.")
    return play_blackjack()


if __name__ == "__main__":
    play_blackjack()
