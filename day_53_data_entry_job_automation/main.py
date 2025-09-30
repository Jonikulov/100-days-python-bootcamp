"""Day 53. Data Entry Job Automation"""

import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

ZILLOW_URL = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.69219435644531%2C%22east%22%3A-122.17446364355469%2C%22south%22%3A37.703343724016136%2C%22north%22%3A37.847169233586946%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A11%7D"
ZILLOW_CLONE_URL = "https://appbrewery.github.io/Zillow-Clone"
GOOGLE_FORM_URL = ""
CHROME_DRIVER_PATH = Path("../chrome_profile").absolute().resolve()

import requests
from bs4 import BeautifulSoup

resp = requests.get(ZILLOW_CLONE_URL)
soup = BeautifulSoup(resp.text, "html.parser")

# Scrape apartments data
zillow_data = {}
apartments = soup.select("#grid-search-results > ul > li")
for i, apartment in enumerate(apartments):
    address = apartment.select_one("address").text.strip()
    price = apartment.select_one(
        "span[data-test='property-card-price']"
    ).text.strip()
    link = apartment.select_one("a.property-card-link").get("href")

    print(f"{i}) {address}")
    print(price)
    print(link)
    print("*" * 80)

    zillow_data[i] = {"address": address, "price": price[:6], "link": link}


# Fill out the form with the data
chrome_opts = webdriver.ChromeOptions()
# chrome_opts.add_experimental_option("detach", True)
# chrome_opts.add_argument(f"--user-data-dir={CHROME_DRIVER_PATH}")

driver = webdriver.Chrome(options=chrome_opts)
# driver.maximize_window()
wait = WebDriverWait(driver, 15)

for apartment in zillow_data.values():
    driver.get(GOOGLE_FORM_URL)
    wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//div[@role='heading'][contains(., 'SF Renting Research')]")
    ))
    time.sleep(1)
    form_inputs = driver.find_elements(
        By.CSS_SELECTOR, "input[type=text].whsOnd.zHQkBf"
    )
    # form_inputs[0].click()
    form_inputs[0].send_keys(apartment["address"])
    # form_inputs[1].click()
    form_inputs[1].send_keys(apartment["price"])
    # form_inputs[2].click()
    form_inputs[2].send_keys(apartment["link"])
    # Click submit button
    driver.find_element(
        By.CSS_SELECTOR, "div.lRwqcd > div[role=button] > span"
    ).click()
    time.sleep(1)


driver.quit()
