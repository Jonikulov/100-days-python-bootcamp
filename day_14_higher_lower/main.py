"""Day 14. Higher or Lower Game."""

import random
import art
import game_data

game_end = False
left_opponent = random.choice(game_data.data)
right_opponent = left_opponent
score = 0
while True:
    print("\033[2J\033[H", end="")  # Clears the screen
    print(art.logo)

    # Check whether the game ended
    if game_end:
        print("Sorry, that's wrong. Final score:", score)
        break
    if score > 0:
        print("That's right! Current score:", score)
        left_opponent = right_opponent

    # Choose a random opponent
    while left_opponent["name"] == right_opponent["name"]:
        right_opponent = random.choice(game_data.data)

    # Identify the correct answer
    answer = "A" if (left_opponent["follower_count"] >
                     right_opponent["follower_count"]) else "B"

    # Compare them and ask the user for response
    print(
        f"Compare A: {left_opponent["name"]}, "
        f"{left_opponent["description"]}, from {left_opponent["country"]}."
        f"{art.vs}"
        f"Against B: {right_opponent["name"]}, "
        f"{right_opponent["description"]}, from {right_opponent["country"]}."
    )
    resp = input("Who has more followers? Type 'A' or 'B': ").strip().upper()

    # Evaluate the user's response
    if resp == answer:
        score += 1
    else:
        game_end = True
