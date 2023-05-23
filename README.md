# Zillowpedia

Let's say you want to search Zillow for property around you, and want to compile all of the data. This is the function that Zillowpedia fits to serve. Zillowpedia will scrape all of the house listings from any Zillow search URL you give it. In addition, you have the option of generating a .csv file from the given data.

NOTE: Only tested on Linux Mint, Windows version under development

## Installation

0. Ensure you have Firefox installed to the default location
1. Download and extract the .zip at <https://github.com/ElijahTyler/Zillowpedia.git>
2. Open Terminal in the project directory and type `python -m pip install -r requirements.txt`

## Usage

IMPORTANT: Open `main.py` and add your personal Zillow search URLs (example is in the file), otherwise nothing will happen once you run the file.

Open Terminal in the project directory and type `python main.py`. This will open an automated Firefox window that will scrape the Zillow webpage for all house listings. Then, a HouseListing object is created for each listing it finds. Lastly, `listings.json` will be created, a dictionary of all listings found.

If you want, you can use HouseData.py to create a .csv file with all of your listings. To do so, open Python in your terminal with `/bin/python3` and run the following commands:

```python
from HouseData import HouseData
data = HouseData('your_file_here.json')
data.generate_csv('your_file_here.csv')
```

This, by default, will generate a .csv file named `HouseData.csv`. You can pass in whatever name you like.
