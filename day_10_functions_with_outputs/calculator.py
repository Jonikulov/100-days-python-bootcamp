"""DAY 10. Calculator."""

CALCULATOR_ART = r"""
 _____________________
|  _________________  |
| | Python_Dev   0. | |
| |_________________| |            _            _       _             
|  ___ ___ ___   ___  |           | |          | |     | |            
| | 7 | 8 | 9 | | + | |   ___ __ _| | ___ _   _| | __ _| |_ ___  _ __ 
| |___|___|___| |___| |  / __/ _` | |/ __| | | | |/ _` | __/ _ \| '__|
| | 4 | 5 | 6 | | - | | | (_| (_| | | (__| |_| | | (_| | || (_) | |   
| |___|___|___| |___| |  \___\__,_|_|\___|\__,_|_|\__,_|\__\___/|_|   
| | 1 | 2 | 3 | | x | |
| |___|___|___| |___| |
| | . | 0 | = | | / | |
| |___|___|___| |___| |
|_____________________|

"""

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    return a / b

OPERATIONS_MAP = {
    "+": add,
    "-": subtract,
    "*": multiply,
    "/": divide
}

def calculator():
    print("\033[2J\033[H", end="")  # Clears the screen
    print(CALCULATOR_ART)
    num1 = float(input("What's the first number?: "))
    continue_calc = True
    while continue_calc:
        operation = input(
            f"Pick an operation [ {"  ".join(OPERATIONS_MAP)} ]: ")
        num2 = float(input("What's the next number?: "))
        result = OPERATIONS_MAP[operation](num1, num2)
        print(f"{num1} {operation} {num2} = {result}")
        restart = input(
            f"Type 'y' to continue calculating with {result}, or "
            f"type 'n' to start a new calculation: "
        ).lower()
        if restart == "y":
            num1 = result
        else:
            continue_calc = False
            calculator()


if __name__ == "__main__":
    calculator()
