"""Day 39. Capstone Part 1: Flight Deal Finder"""

'''     Program Requirements:
* Use the Flight Search and Sheety API to populate your own copy of the Google
Sheet with International Air Transport Association (IATA) codes for each city.
Most of the cities in the sheet include multiple airports, you want the city
code (not the airport code see here).

* Use the Flight Search API to check for the cheapest flights from tomorrow to
6 months later for all the cities in the Google Sheet.

* If the price is lower than the lowest price listed in the Google Sheet then
send an SMS (or WhatsApp Message) to your own number using the Twilio API.

* The SMS should include the departure airport IATA code, destination airport
IATA code, flight price and flight dates.'''

from data_manager import DataManager
from flight_data import FlightData
from flight_search import FlightSearch
from notification_manager import NotificationManager

from datetime import date, timedelta

data_manager = DataManager()
sheet_data = data_manager.get_sheet_rows()

flight_search = FlightSearch()

def main():
    origin_city_code = "LON"  # London
    tomorrow = date.today() + timedelta(days=1)
    from_time = date.strftime(tomorrow, "%Y-%m-%d")
    next_six_months = date.today() + timedelta(days=180)
    to_time = date.strftime(next_six_months, "%Y-%m-%d")

    for row in sheet_data:
        dest_city_code = row.get("iataCode")
        if dest_city_code:
            print(f"Getting flights for {row['city']}...")
            # Search flight offer
            flight_offer = flight_search.find_flights(
                origin_city_code,
                dest_city_code,
                from_time,
                to_time,
            )
            flight_data = FlightData(flight_offer)
            new_price = flight_data.find_cheapest_flight()
            print(f"{row['city']}: ${new_price}...")
            if isinstance(new_price, (float, int)) and new_price < row.get("lowestPrice", 0):
                message = f"Low price alert! Only ${new_price} to fly " \
                    f"from {origin_city_code} to {dest_city_code}, on " \
                    f"{flight_data.out_date} until {flight_data.return_date}."
                print(f"\t<Sending SMS...> :\n{message}")
                NotificationManager(message).send_sms_msg()
        else:
            # Get the IATA code of the city
            dest_city_code = flight_search.get_city_iata_code(row["city"])
            # Update the sheet by filling IATA code data
            data_manager.update_row(row["id"], {"iataCode": dest_city_code})
            row["iataCode"] = dest_city_code


if __name__ == "__main__":
    main()
