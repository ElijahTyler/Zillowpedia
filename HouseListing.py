class HouseListing:
    def __init__(self) -> None:
        self.address = ""
        self.realtor = ""
        self.price = 0
        self.beds = 0
        self.baths = 0
        self.square_feet = 0

    def __str__(self) -> str:
        return f'Address: {self.address}\nRealtor: {self.realtor}\nPrice: {self.price}\nBeds: {self.beds}\nBaths: {self.baths}\nSquare feet: {self.square_feet}'
    
    def set_address(self, address):
        self.address = address
    def get_address(self):
        return self.address
    
    def set_realtor(self, realtor):
        self.realtor = realtor
    def get_realtor(self):
        return self.realtor
    
    def set_price(self, price):
        self.price = price
    def get_price(self):
        return self.price

    def set_beds(self, beds):
        self.beds = beds
    def get_beds(self):
        return self.beds
    
    def set_baths(self, baths):
        self.baths = baths
    def get_baths(self):
        return self.baths
    
    def set_square_feet(self, square_feet):
        self.square_feet = square_feet
    def get_square_feet(self):
        return self.square_feet