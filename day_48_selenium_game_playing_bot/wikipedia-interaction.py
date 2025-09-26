"""Day 48. Selenium Webdriver & Game Playing Bot"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions
import time

# Keep browser open even after program finishes
chrome_opts = webdriver.ChromeOptions()
chrome_opts.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_opts)

# Go to the main page
driver.get("http://en.wikipedia.org/wiki/Main_Page")
# Get the number of articles
english_articles_num = driver.find_element(
    By.XPATH, "(//div[@id='articlecount']//a[@title='Special:Statistics'])[2]"
)
print("Number of articles in English:", english_articles_num.text)

# Find & click the search bar
search_bar = driver.find_element(
    By.XPATH, "//div[@id='p-search']/a"
)
try:
    search_bar.click()
except exceptions.ElementNotInteractableException:
    # Browser page working in max size
    print("The search bar is already at its full size...")
search_bar = driver.find_element(
    By.XPATH, "//form[@id='searchform']//input[@name='search']"
)
search_bar.click()
search_bar.send_keys("python")  # Keys.ENTER
time.sleep(1)
driver.find_element(
    By.XPATH, "//a//bdi[contains(text(), '(programming language)')]"
).click()

# driver.quit()
