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

maindir = os.path.dirname(os.path.abspath(__file__))

# replace this with your own zillow search query
# example: I went to zillow.com and typed 48377 in my search, then drew a region around me in which to search for
url = r"https://www.zillow.com/homes/for_sale/?searchQueryState=%7B%22usersSearchTerm%22%3A%2248377%22%2C%22mapBounds%22%3A%7B%22west%22%3A-83.67611902001953%2C%22east%22%3A-83.27717797998046%2C%22south%22%3A42.379650083592%2C%22north%22%3A42.63022260878972%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22con%22%3A%7B%22value%22%3Afalse%7D%2C%22mf%22%3A%7B%22value%22%3Afalse%7D%2C%22manu%22%3A%7B%22value%22%3Afalse%7D%2C%22land%22%3A%7B%22value%22%3Afalse%7D%2C%22tow%22%3A%7B%22value%22%3Afalse%7D%2C%22apa%22%3A%7B%22value%22%3Afalse%7D%2C%22apco%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A11%2C%22customRegionId%22%3A%223343264666X1-CR1fmc8b99lrgsl_19hukm%22%7D"

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
    driver.get(url)

    print("Scraping results...")
    result_count = driver.find_element(By.CLASS_NAME, "result-count")
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
        entries = soup.find_all(attrs={"class": "StyledPropertyCardDataWrapper-c11n-8-84-0__sc-1omp4c3-0 cXTjvn property-card-data"})

    print(f"Success! {result_count.text}")
    print(f"Results for this page: {len(entries)}")
    house_list = []
    for entry in entries:
        hl = HouseListing(str(entry))
        house_list.append(hl)

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