class Travel:
    def __init__(self, destination, hotel, transport, meal, activities, insurance):
        self.destination =destination
        self.hotel=hotel
        self.transport=transport
        self.meal=meal
        self.activities=activities
        self.insurance=insurance

    def show(self):
        print("Destination: ", self.destination)
        print("Hotel: ", self.hotel)
        print("Transport: ", self.transport)
        print("Meal: ", self.meal)
        print("Activities: ", self.activities)
        print("Insurance: ", self.insurance)


class TravelBuilder:
    def __init__(self):
        self.destination = None
        self.hotel = None
        self.transport = None
        self.meal = None
        self.activities = None
        self.insurance = None

    def set_destination(self, destination):
        self.destination = destination
        return self

    def set_hotel(self, hotel):
        self.hotel = hotel
        return self

    def set_transport(self, transport):
        self.transport = transport
        return self

    def set_meal(self, meal):
        self.meal = meal
        return self

    def set_activities(self, activities):
        self.activities = activities
        return self

    def set_insurance(self, insurance):
        self.insurance = insurance
        return self

    def build(self):
        return Travel(
                self.destination,
                self.hotel,
                self.transport,
                self.meal,
                self.activities,
                self.insurance)


def main():
    travel: Travel = (
        TravelBuilder()
        .set_destination("Auckland")
        .set_hotel("3-star")
        .set_transport("Bus")
        .set_meal("Full board")
        .set_activities("Museum")
        .set_insurance("No")
        .build())
    travel.show()
    

if __name__ == "__main__":
    main()