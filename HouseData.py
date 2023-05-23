import json
import csv

class HouseData:
    def __init__(self, jason = None) -> None:
        # takes in a .json file generated from dictionary of HouseListings
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
            for h in self.data:
                house = self.data[h]
                self.addresses.append(house['address'])
                self.realtors.append(house['realtor'])
                self.prices.append(house['price'])
                self.beds.append(house['beds'])
                self.baths.append(house['baths'])
                self.square_feets.append(house['square_feet'])

    def generate_csv(self, name = None):
        if not name:
            name = "HouseData.csv"
        if not name.endswith(".csv"):
            name += ".csv"
        
        with open(name, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Address", "Realtor", "Price", "Beds", "Baths", "Square Feet"])
            for i in range(len(self.addresses)):
                writer.writerow([self.addresses[i], self.realtors[i], self.prices[i], self.beds[i], self.baths[i], self.square_feets[i]])
        
        print(f"CSV file generated: {name}")