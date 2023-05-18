from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.common.by import By

from HouseListing import HouseListing

from bs4 import BeautifulSoup
import os, time
from sys import platform
import time
import json

maindir = os.path.dirname(os.path.abspath(__file__))

ZIP_CODE = True

url = r"https://www.zillow.com/novi-mi-48377/houses/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%2248377%22%2C%22mapBounds%22%3A%7B%22west%22%3A-83.52651613000488%2C%22east%22%3A-83.42678086999511%2C%22south%22%3A42.47373247081512%2C%22north%22%3A42.53637560960464%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A79170%2C%22regionType%22%3A7%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22manu%22%3A%7B%22value%22%3Afalse%7D%2C%22land%22%3A%7B%22value%22%3Afalse%7D%2C%22apa%22%3A%7B%22value%22%3Afalse%7D%2C%22apco%22%3A%7B%22value%22%3Afalse%7D%2C%22mf%22%3A%7B%22value%22%3Afalse%7D%2C%22con%22%3A%7B%22value%22%3Afalse%7D%2C%22tow%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A13%7D"

agent_a = "Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"
agent_b = "Mozilla/5.0 (Linux; Android 9; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Mobile Safari/537.36"
agent_c = "Mozilla/5.0 (iPad; U; CPU OS 3_2_1 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Mobile/7B405"
agents = [agent_a, agent_b, agent_c]

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
    # decide agent
    # with open('agent_to_use.json', 'r') as f:
    #     data = json.load(f)
    #     agent_to_use = agents[data['agent_to_use']]
    #     print("Using agent: " + agent_to_use)
    #     with open('agent_to_use.json', 'w') as f:
    #         data['agent_to_use'] = (data['agent_to_use'] + 1) % len(agents)
    #         json.dump(data, f)
    # headers = {'User-Agent': agent_to_use}

    print("Loading Selenium (firefox)...")
    driver = init_firefox(headless=False)

    print("Loading Zillow...")
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    print("Searching for results...")
    time.sleep(5)
    entries = soup.div.find_all(attrs={"class": "StyledPropertyCardDataWrapper-c11n-8-84-0__sc-1omp4c3-0 cXTjvn property-card-data"})

    if entries:
        house_list = []
        for entry in entries:
            hl = HouseListing(entry)
            house_list.append(hl)
            print(hl)
    else:
        print("No results found :(")

if __name__ == "__main__":
    main()