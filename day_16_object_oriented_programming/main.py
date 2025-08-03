"""Day 16. Object-Oriented Programming."""
# Program specification in the ../day_15_.../PDF file.
# Docs in the ./PDF file.

from coffee_maker import CoffeeMaker
from money_machine import MoneyMachine
from menu import Menu

coffee_maker = CoffeeMaker()
money_machine = MoneyMachine()
menu = Menu()

is_on = True
while is_on:
    options = menu.get_items()
    choice = input(f"\nWhat would you like? ({options}): ").strip().lower()

    if choice == "report":
        coffee_maker.report()
        money_machine.report()
    elif choice == "off":
        print("Enjoy This Service!")
        is_on = False
    else:
        drink = menu.find_drink(choice)
        if drink and coffee_maker.is_resource_sufficient(drink) and \
                money_machine.make_payment(drink.cost):
            coffee_maker.make_coffee(drink)
