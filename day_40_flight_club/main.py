"""Day 40. Capstone Part 2: Flight Club"""

from data_manager import DataManager
from flight_data import FlightData
from flight_search import FlightSearch
from notification_manager import NotificationManager

from datetime import date, timedelta

data_manager = DataManager()
sheet_data = data_manager.get_prices_rows()
customer_data = data_manager.get_customer_emails()
customer_emails = [row["email"] for row in customer_data]

flight_search = FlightSearch()

notif_manager = NotificationManager()

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
            # Search direct flight offers
            flight_offer = flight_search.find_flights(
                origin_city_code,
                dest_city_code,
                from_time,
                to_time,
            )
            flight_data = FlightData(flight_offer)
            new_price = flight_data.find_cheapest_flight()
            if not isinstance(new_price, (int, float)):
                # Search indirect flight offers
                flight_offer = flight_search.find_flights(
                    origin_city_code,
                    dest_city_code,
                    from_time,
                    to_time,
                    False,
                )
                flight_data = FlightData(flight_offer)
                new_price = flight_data.find_cheapest_flight()

            print(f"{row['city']}: ${new_price}...")
            if isinstance(new_price, (float, int)) and new_price < row.get("lowestPrice", 0):
                message = f"Low price alert! Only ${new_price} to fly " \
                    f"from {origin_city_code} to {dest_city_code}, on " \
                    f"{flight_data.out_date} until {flight_data.return_date}" \
                    f", stops: {flight_data.stops}."
                print(f"\t<Sending Messages...> :\n{message}")
                notif_manager.send_emails(customer_emails, message)
        else:
            # Get the IATA code of the city
            dest_city_code = flight_search.get_city_iata_code(row["city"])
            # Update the sheet by filling IATA code data
            data_manager.update_price_row(row["id"], {"iataCode": dest_city_code})
            row["iataCode"] = dest_city_code


if __name__ == "__main__":
    main()
