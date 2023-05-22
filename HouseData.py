import json

class HouseData:
    def __init__(self, jason = None) -> None:
        self.addresses = []
        self.realtors = []
        self.prices = []
        self.beds = []
        self.baths = []
        self.square_feets = []
        if not jason:
            return
        with open(jason, 'r') as f:
            self.data = json.load(f)
            for house in self.data:
                self.addresses.append(house['address'])
                self.realtors.append(house['realtor'])
                self.prices.append(house['price'])
                self.beds.append(house['beds'])
                self.baths.append(house['baths'])
                self.square_feets.append(house['square_feet'])

    #TODO add methods

    def sort_price(self):
        return sorted(self.prices)