"""The NATO alphabet converter"""

import pandas as pd

df = pd.read_csv("nato_phonetic_alphabet.csv")

def get_letter_code(let):
    return df[df["letter"]==let]["code"].item()

input_text = input("Enter a word: ").strip().upper()
print([get_letter_code(ch) for ch in input_text])
