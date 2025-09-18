class FlightData:
    '''This is responsible for structuring the flight data'''
    def __init__(self, resp_data: dict = {}):
        self.data = resp_data
        if self.data.get("meta", {}).get("count", 0) > 0:
            self.data = resp_data["data"][0]
            self.price = float(self.data["price"]["grandTotal"])
            self.origin_airport_code = self.data["itineraries"][0]["segments"][0]["departure"]["iataCode"]
            self.dest_airport_code = self.data["itineraries"][0]["segments"][0]["arrival"]["iataCode"]
            self.out_date = self.data["itineraries"][0]["segments"][0]["departure"]["at"].split("T")[0]
            self.return_date = self.data["itineraries"][1]["segments"][0]["departure"]["at"].split("T")[0]
            self.stops = len(self.data["itineraries"][0]["segments"]) - 1
        else:
            self.price = "N/A"
            self.origin_airport_code = "N/A"
            self.dest_airport_code = "N/A"
            self.out_date = "N/A"
            self.return_date = "N/A"
            self.stops = "N/A"

    def find_cheapest_flight(self):
        return self.price
