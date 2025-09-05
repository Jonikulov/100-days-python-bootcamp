"""The NATO alphabet converter"""

import pandas as pd

df = pd.read_csv("nato_phonetic_alphabet.csv")

def get_letter_code(let):
    return df[df["letter"]==let]["code"].item()

while True:
    input_text = input("Enter a word: ").strip().upper()
    if input_text.isalpha():
        print([get_letter_code(ch) for ch in input_text])
        break
    print("Sorry, only letters in the alphabet please.")
