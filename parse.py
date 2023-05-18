from bs4 import BeautifulSoup

with open("entry.html", "r") as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')
# address
print(soup.address.text.strip())
# realtor
realtor = soup.find_all(attrs={"class": "StyledPropertyCardDataArea-c11n-8-84-0__sc-yipmu-0 dzjytt"})[0]
print(realtor.text.strip())
# price
price = soup.find_all(attrs={"class": "StyledPropertyCardDataArea-c11n-8-84-0__sc-yipmu-0 dJxUgr"})[0]
print(price.text.strip())
# beds
beds_baths_sqft = soup.find_all(attrs={"class": "StyledPropertyCardHomeDetailsList-c11n-8-84-0__sc-1xvdaej-0 ehrLVA"})[0]
beds, baths, sqft = beds_baths_sqft.find_all("b")
print(beds.text.strip())
# baths
print(baths.text.strip())
# sqft
print(sqft.text.strip())