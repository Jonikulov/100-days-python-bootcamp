"""Day 17. The Quiz Project (implemented my own version/solution)"""

import random
from data import question_data

questions = random.sample(question_data, k=10)
score = 0
for idx, q in enumerate(questions):
    answer = input(f'Q_{idx+1}: {q["text"]} (True/False): ').strip().lower()
    if answer == q["answer"].lower():
        score += 1
        print("CORRECT! ", end="")
    else:
        print("INCORRECT! ", end="")
    print(f"Current score: {score}/{idx+1}\n")

print(f"You've completed the QUIZ.\nYour final score: {score}/10")
