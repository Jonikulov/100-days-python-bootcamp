"""DAY 9. Secret Auction."""

GAVEL_ART = r'''
         ___________
         \         /
          )_______(
          |"""""""|_.-._,.---------.,_.-._
          |       | | |               | | ''-.
          |       |_| |_             _| |_..-'
          |_______| '-' `'---------'` '-'
          )"""""""(
         /_________\
       .-------------.
      /_______________\
'''

auction_bids = {}
while True:
    print(GAVEL_ART)
    name = input("Enter your name: ")
    bid = float(input("What is your bid: $"))
    auction_bids[name] = bid

    other_bid = input("Are there other bidders? [yes/no] ").strip().lower()
    print("\033[2J\033[H", end="")  # Clears the screen

    if other_bid in ["yes", "y"]:
        continue

    winner = max(auction_bids, key=auction_bids.get)  # gets max value's key
    print(f"The winner is {winner} with a bid of ${auction_bids[winner]}\n")
    break
