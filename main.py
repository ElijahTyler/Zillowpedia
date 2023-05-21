from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from HouseListing import HouseListing

from bs4 import BeautifulSoup
import os, time
from sys import platform
import time
import json
import math
import re

maindir = os.path.dirname(os.path.abspath(__file__))

# replace USER_URL with your own zillow search query
# step 1: Go to zillow.com
# step 2: Set your search parameters
# ex. I typed a zip code and drew a region in which to search for
# step 3: Copy the url and paste it here
# aside: using r"" (raw string) eliminates the need to escape the backslashes
USER_URL = r"https://www.zillow.com/homes/for_sale/?searchQueryState=%7B%22usersSearchTerm%22%3A%2248377%22%2C%22mapBounds%22%3A%7B%22west%22%3A-83.67611902001953%2C%22east%22%3A-83.27717797998046%2C%22south%22%3A42.379650083592%2C%22north%22%3A42.63022260878972%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22con%22%3A%7B%22value%22%3Afalse%7D%2C%22mf%22%3A%7B%22value%22%3Afalse%7D%2C%22manu%22%3A%7B%22value%22%3Afalse%7D%2C%22land%22%3A%7B%22value%22%3Afalse%7D%2C%22tow%22%3A%7B%22value%22%3Afalse%7D%2C%22apa%22%3A%7B%22value%22%3Afalse%7D%2C%22apco%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A11%2C%22customRegionId%22%3A%223343264666X1-CR1fmc8b99lrgsl_19hukm%22%7D"

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



def main():
    start_time = time.time()

    print("Loading Selenium (firefox)...")
    driver = init_firefox(headless=False)

    print("Loading Zillow...")
    driver.get(USER_URL)

    CURRENT_CLASS = re.compile("StyledPropertyCardDataWrapper-c11n-8-8.*")
    result_count = driver.find_element(By.CLASS_NAME, "result-count")
    result_num = int(result_count.text.split()[0].replace(",", ""))
    page_limit = math.ceil(result_num / 40)

    house_list = []
    for page_num in range(page_limit):
        print(f"Scraping results from page {page_num+1}...")
        container = driver.find_element(By.ID, "search-page-list-container")
        action = ActionChains(driver)
        for i in range(12):
            action.move_to_element(container).perform()
            if i < 10:
                action.click(container).perform()
            action.send_keys(Keys.PAGE_DOWN).perform()
            time.sleep(0.5)
        entries = []
        while not entries:
            time.sleep(1)
            html = driver.execute_script("return document.documentElement.outerHTML")
            soup = BeautifulSoup(html, 'html.parser')
            entries = soup.find_all(attrs={"class": CURRENT_CLASS})

        print(f"Results for this page: {len(entries)}")
        
        for entry in entries:
            hl = HouseListing(str(entry))
            house_list.append(hl)

        if page_num < page_limit - 1:
            next_button = driver.find_element(By.CLASS_NAME, "StyledButton-c11n-8-84-0__sc-wpcbcc-0 hFaVRz PaginationButton-c11n-8-84-0__sc-si2hz6-0 ekxYeX")
            action.click(next_button).perform()

    print(f"Success! {result_count.text}")
    
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

    driver.quit()
    # time taken to 2 decimal points
    total_time = round(time.time() - start_time, 2)
    print(f"Time taken: {total_time} seconds")

if __name__ == "__main__":
    main()