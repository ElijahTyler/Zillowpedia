from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from HouseListings import HouseListings

from bs4 import BeautifulSoup
import os, time
from sys import platform
import time
import json
import math
import re

maindir = os.path.dirname(os.path.abspath(__file__))



def init_firefox(headless=False):
    opts = FirefoxOptions()
    if headless:
        opts.add_argument("--headless")
    opts.add_argument("--ignore-certificate-errors")
    opts.add_argument("--start-maximized")

    if platform == "win32":
        opts.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
        driver_executable = os.path.join(maindir, 'geckodriver.exe')
    elif platform == "linux" or platform == "linux2":
        driver_executable = os.path.join(maindir, 'geckodriver')
    driver = webdriver.Firefox(options = opts, executable_path = driver_executable)
    return driver



def main(url_list):
    start_time = time.time()

    house_list = []
    for USER_URL in url_list:
        print("Loading Selenium (firefox)...")
        driver = init_firefox(headless=False)

        print("Loading Zillow URL...")
        driver.get(USER_URL)

        CURRENT_CLASS = "StyledPropertyCardDataWrapper-c11n-8-84-0__sc-1omp4c3-0 cXTjvn property-card-data"

        container = driver.find_element(By.ID, "search-page-list-container")
        action = ActionChains(driver)
        for i in range(12):
            action.move_to_element(container).perform()
            if i < 10:
                action.click(container).perform()
            action.send_keys(Keys.PAGE_DOWN).perform()
            time.sleep(0.5)
        entries = []
        timeout = 0
        while not entries:
            time.sleep(1)
            html = driver.execute_script("return document.documentElement.outerHTML")
            soup = BeautifulSoup(html, 'html.parser')
            entries = soup.find_all(attrs={"class": CURRENT_CLASS})
            timeout += 1
            if timeout > 10:
                print(f"Timeout reached. Ending program...")
                driver.close()
                break

        for entry in entries:
            hl = HouseListings(str(entry))
            house_list.append(hl)

        driver.close()

    print(f"Success! Results found: {len(house_list)}")
    
    # with open("listings.json", "r") as f:
    #     data = json.load(f)
    with open("listings.json", "w") as f:
        listing = 1
        house_dict = {}
        for house in house_list:
            house_dict[listing] = house.to_dict()
            listing += 1
        # data.update(house_dict)
        # json.dump(data, f, indent=4)
        json.dump(house_dict, f, indent=4)

    # time taken to 2 decimal points
    total_time = round(time.time() - start_time, 2)
    print(f"Time taken: {total_time} seconds")

if __name__ == "__main__":
    # step 1: Go to zillow.com
    # step 2: Set your search parameters (ex. I typed a zip code and drew a region in which to search for)
    # step 3: Copy the urls FOR EACH INDIVIDUAL PAGE and paste it here
    # aside: r"" (raw string) eliminates the need to escape the backslashes

    # example setup:
    # url1 = r"https://www.zillow.com/homes/for_sale/?searchQueryState=blahblahblah"
    # url2 = r""
    # url3 = r""
    # url4 = r""
    # ...
    # urls = [url1, url2, url3, url4, ...]
    # main(urls)

    urls = []
    main(urls)