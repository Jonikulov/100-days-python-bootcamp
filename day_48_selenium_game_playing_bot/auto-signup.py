"""Day 48. Selenium Webdriver & Game Playing Bot"""

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import random
import string

# Keep browser open even after program finishes
chrome_opts = webdriver.ChromeOptions()
chrome_opts.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_opts)

# Go to the main page
driver.get("https://secure-retreat-92358.herokuapp.com")
time.sleep(1)

first_name = "".join(random.choices(string.ascii_letters, k=7))
last_name = "".join(random.choices(string.ascii_letters, k=9))
email = "".join(random.sample(string.ascii_lowercase, k=5)) + "@mail.com"

driver.find_element(
    By.XPATH, "//input[@name='fName']"
).send_keys(first_name)
driver.find_element(
    By.XPATH, "//input[@name='lName']"
).send_keys(last_name)
driver.find_element(
    By.XPATH, "//input[@name='email']"
).send_keys(email)

driver.find_element(
    By.XPATH, "//button[@type='submit']"
).click()

# driver.quit()
