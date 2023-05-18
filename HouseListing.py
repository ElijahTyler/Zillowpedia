from bs4 import BeautifulSoup

class HouseListing:
    def __init__(self, obj = None) -> None:
        if not obj:
            print("Please pass in a BeautifulSoup object")
            return
        soup = BeautifulSoup(obj, 'html.parser')
        # address
        self.address = soup.address.text.strip()
        # realtor
        realtor = soup.find_all(attrs={"class": "StyledPropertyCardDataArea-c11n-8-84-0__sc-yipmu-0 dzjytt"})[0]
        self.realtor = realtor.text.strip()
        # price
        price = soup.find_all(attrs={"class": "StyledPropertyCardDataArea-c11n-8-84-0__sc-yipmu-0 dJxUgr"})[0]
        self.price = int(price.text.strip().replace("$", "").replace(",", ""))
        # beds
        beds_baths_sqft = soup.find_all(attrs={"class": "StyledPropertyCardHomeDetailsList-c11n-8-84-0__sc-1xvdaej-0 ehrLVA"})[0]
        beds, baths, sqft = beds_baths_sqft.find_all("b")
        self.beds = int(beds.text.strip())
        # baths
        self.baths = int(baths.text.strip())
        # sqft
        self.square_feet = int(sqft.text.strip().replace(",", ""))

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