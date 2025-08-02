"""Day 15. Coffee Machine Program."""

# Program specification in the PDF file.

MENU = {
    "espresso": {
        "ingredients": {
            "water": 50,
            "coffee": 18,
        },
        "cost": 1.5,
    },
    "latte": {
        "ingredients": {
            "water": 200,
            "milk": 150,
            "coffee": 24,
        },
        "cost": 2.5,
    },
    "cappuccino": {
        "ingredients": {
            "water": 250,
            "milk": 100,
            "coffee": 24,
        },
        "cost": 3.0,
    }
}

def report(resources_):
    print(
        f"Water: {resources_["water"]} ml\n"
        f"Milk: {resources_["milk"]} ml\n"
        f"Coffee: {resources_["coffee"]} g\n"
        f"Money: $ {resources_["money"]}"
    )


def check_resources(coffee, resources_):
    for item, value in coffee["ingredients"].items():
        if value > resources_[item]:
            print(f"Sorry, there is not enough {item}.")
            return False
    return True


def process_transaction(coffee):
    print("Please insert coins.")
    coins_map = {
        "quarters": 0.25, "dimes": 0.1, "nickles": 0.05, "pennies": 0.01
    }
    money = 0
    for coin, value in coins_map.items():
        money += int(input(f"How many {coin}: ")) * value
    if money > coffee["cost"]:
        change = money - coffee["cost"]
        print(f"Here is the $ {change:.2f} in change.")
        money -= change
    elif money < coffee["cost"]:
        print("Sorry, that's not enough money. Money refunded.")
        money = 0
    return money


def make_coffee(coffee, resources_):
    for item, value in MENU[coffee]["ingredients"].items():
        resources_[item] -= value
    print(f"Here is your {coffee} ☕. Enjoy!")
    return resources_


resources = {
    "water": 300,
    "milk": 200,
    "coffee": 100,
    "money": 0
}

is_on = True
while is_on:
    prompt = input(
        "\nWhat would you like? (espresso/latte/cappuccino): "
    ).strip().lower()

    if prompt == "report":
        report(resources)
    elif prompt == "off":
        print("Enjoy This Service!")
        is_on = False
    else:
        if check_resources(MENU[prompt], resources):
            profit = process_transaction(MENU[prompt])
            if profit:
                resources["money"] += profit
                resources = make_coffee(prompt, resources)
