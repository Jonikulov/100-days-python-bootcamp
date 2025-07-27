import random
import string

print("Welcome to the PyPassword Generator!")
letters = int(input("How many letters would you like in your password?\n"))
symbols = int(input("How many symbols would you like?\n"))
numbers = int(input("How many numbers would you like?\n"))

letters = random.choices(string.ascii_letters, k=letters)
symbols = random.choices(string.punctuation, k=symbols)
numbers = random.choices(string.digits, k=numbers)

result = letters + symbols + numbers
print(f"[{', '.join(result)}]")
random.shuffle(result)
print("Password:", "".join(result))
