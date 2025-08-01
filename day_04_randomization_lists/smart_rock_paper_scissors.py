import sys
import random

ROCK = r"""
      _______
  ---'   ____)
        (_____)
        (_____)
        (____)
  ---.__(___)"""
PAPER = r"""
      _______
  ---'   ____)____
            ______)
            _______)
           _______)
  ---.__________)"""
SCISSORS = r"""
      _______
  ---'   ____)____
            ______)
         __________)
        (____)
  ---.__(___)"""
GAME_MAP = {0: ROCK, 1: PAPER, 2: SCISSORS}
user_score = 0
computer_score = 0

# TODO: Implement "smart" version of Rock-Paper-Scissors game.
#  Which is impossible for the user to win.

def play_game() -> None:
    global user_score
    global computer_score

    user_choice = input("\nType 0 for Rock, 1 for Paper or "
                        "2 for Scissors, -1 to quit the game.\n"
                        "Your Choice: ").strip()
    computer_choice = random.choice([0, 1, 2])

    try:
        user_choice = int(user_choice)
    except ValueError:
        print("Invalid input.")
        return

    if user_choice == -1:
        print("Good bye!")
        sys.exit(0)

    if user_choice not in [0, 1, 2]:
        print("Invalid option.")
        return

    print(GAME_MAP[user_choice])
    print("\nComputer chose:", computer_choice, end="")
    print(GAME_MAP[computer_choice])

    if computer_choice == user_choice:
        print("TIE!")
    elif (user_choice == 0 and computer_choice == 2) or \
            (user_choice == 1 and computer_choice == 0) or \
            (user_choice == 2 and computer_choice == 1):
        print("You Win!")
        user_score += 1
    else:
        print("You Lose!")
        computer_score += 1
    print(f"SCORE: USER - {user_score} || COMPUTER - {computer_score}")

def main():
    try:
        print("Welcome to the Rock-Paper-Scissors game!")
        while True:
            play_game()
    except KeyboardInterrupt:
        print("\nQuitting the game...")

if __name__ == "__main__":
    main()
