"""DAY 12. Number Guessing Game."""

import random

ART = r"""
    _                         ___  _                _                  _
  / _ \_   _  ___  ___ ___  /__   \ |__   ___    /\ \ \_   _ _ __ ___ | |__   ___ _ __ 
 / /_\/ | | |/ _ \/ __/ __|   / /\/ '_ \ / _ \  /  \/ / | | | '_ ' _ \| '_ \ / _ \ '__|
/ /_\\| |_| |  __/\__ \__ \  / /  | | | |  __/ / /\  /| |_| | | | | | | |_) |  __/ |   
\____/ \__,_|\___||___/___/  \/   |_| |_|\___| \_\ \/  \__,_|_| |_| |_|_.__/ \___|_|      
"""

def play_number_guessing_game():
    """Plays the Number Guessing Game."""
    print("\033[2J\033[H", end="")  # Clears the screen
    print(ART)
    print("Welcome to the Number Guessing Game!")

    key_number = random.randint(1, 100)
    game_level = input("Choose a game difficulty: 'easy' or 'hard': ")
    if game_level == "hard":
        attempts = 5
    else:
        attempts = 10
    print("I'm thinking of a number between 1 and 100.")
    while attempts > 0:
        guess = input("\nMake a guess: ").strip()
        if not guess.isdecimal():
            print("Invalid Input.")
        elif int(guess) == key_number:
            print("YOU WIN. The answer was:", key_number)
            break
        elif int(guess) > key_number:
            print("TOO HIGH.")
        else:
            print("TOO LOW.")
        attempts -= 1
        print(f"You have {attempts} remaining attempts the guess the number.")
    else:
        print("\nYOU LOSE. You've run out of guesses. "
              "The answer was:", key_number)


if __name__ == "__main__":
    start = True
    while True:
        if not start:
            play_again = input("\nPLAY AGAIN? [y/n]: ").strip().lower()
            if play_again in ["n", "no"]:
                break
        play_number_guessing_game()
        start = False
