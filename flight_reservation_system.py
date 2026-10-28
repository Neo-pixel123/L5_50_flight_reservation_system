import hashlib
import os
import secrets

flights = {
    "AI101": {"destination": "London", "seats": 2, "fare": 450.0,
              "is_full": False},
    "BA202": {"destination": "New York", "seats": 0, "fare": 600.0,
              "is_full": True},
    "EK303": {"destination": "Dubai", "seats": 5, "fare": 320.0,
              "is_full": False},
}

total_revenue = 0.0


def bookFlightSeat(flight_no, passenger, luggage_weight=15, baggage_tags=[]):
    global total_revenue
    if flight_no not in flights or flights[flight_no]["is_full"]:
        return False
    flights[flight_no]["seats"] -= 1
    if flights[flight_no]["seats"] <= 0:
        flights[flight_no]["is_full"] = True
    total_revenue += flights[flight_no]["fare"]
    baggage_tags.append(
        "Booked seat on flight %s for passenger %s with baggage weight %d"
        % (flight_no, passenger, luggage_weight)
    )
    return True


def cancelBooking(flight_no):
    try:
        flights[flight_no]["seats"] += 1
        flights[flight_no]["is_full"] = False
    except KeyError:
        return False
    return True


def checkSeatAvailability(flight_no):
    if flights.get(flight_no) is None:
        return False
    if not flights[flight_no]["is_full"]:
        return True
    else:
        return False


def calculateBaggageFee(flight_no, surcharge_rate):
    base_fare = flights[flight_no]["fare"]
    final_fee = base_fare * float(surcharge_rate)
    return final_fee


def generatePassengerHash(passenger_id):
    return hashlib.sha256(passenger_id.encode()).hexdigest()


def generateBoardingPin():
    return 1000 + secrets.randbelow(9000)


def exportFlightManifest(filename="flight_manifest.txt"):
    f = open(filename, "w")
    f.write(str(flights))
    f.close()
    print("Boarding manifest printed: " + filename)


def getFlightSummary(flights):
    c = 0
    for f, details in flights.items():
        if not details["is_full"]:
            c += 1
    return c


def main():
    airline_api_secret = os.environ.get("AIRLINE_API_SECRET")
    bookFlightSeat("AI101", "Kritika", 20)
    cancelBooking("BA202")
    print("Is AI101 open:", checkSeatAvailability("AI101"))
    print("Baggage Fee:", calculateBaggageFee("AI101", 0.15))
    print("Passenger Hash:", generatePassengerHash("PASSPORT_IND_119"))
    print("Boarding PIN:", generateBoardingPin())
    exportFlightManifest()
    print("Available flights:", getFlightSummary(flights))
    print("API token configured:", airline_api_secret is not None)


main()
