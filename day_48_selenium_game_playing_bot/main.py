"""Day 48. Selenium Webdriver & Game Playing Bot"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException

# Keep browser open even after program finishes
chrome_opts = webdriver.ChromeOptions()
chrome_opts.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_opts)

game_url = "https://ozh.github.io/cookieclicker"
# game_url = "https://orteil.dashnet.org/cookieclicker"
driver.get(game_url)
wait = WebDriverWait(driver, 15)  # poll_frequency=0.1

# Check & select the language pop-up window
language = wait.until(EC.element_to_be_clickable(
    (By.CSS_SELECTOR, "div#langSelect-EN"))
)
language.click()
driver.implicitly_wait(10)

wait.until(EC.element_to_be_clickable(
    (By.LINK_TEXT, "Got it!")
)).click()

start_time = last_time = time.time()
while True:
    try:
        # Goto the cookie and click it
        wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "button#bigCookie"))
        ).click()

        # Check the cookies every 5 seconds
        if time.time() > last_time + 1 and time.localtime().tm_sec % 5 == 0:
            last_time = time.time()
            # Purchase the most expensive upgrade that is affordable
            for i in range(5, -1, -1):  # max start: 19
                product = driver.find_element(
                    By.CSS_SELECTOR, f"div#product{i}"
                )
                # Select the most expensive purchase
                if "enabled" in product.get_attribute("class"):
                    product.click()
                    break

        # Time out after 5 mintues
        if time.time() > start_time + 60 * 5:
            per_second = driver.find_element(
                By.CSS_SELECTOR, "div#cookiesPerSecond"
            ).text
            print("Cookies", per_second)
            break

    except StaleElementReferenceException:
        # Element got replaced between wait and click; just try again
        continue

driver.quit()
