"""Day 52. Instagram Follower Bot"""

import os
import time
from pathlib import Path
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()

INSTAGRAM_USERNAME = os.getenv("INSTAGRAM_USERNAME")
INSTAGRAM_PASSWORD = os.getenv("INSTAGRAM_PASSWORD")
CHROME_DRIVER_PATH = Path("../chrome_profile").absolute().resolve()
SIMILAR_ACCOUNT = "programmerplus"

class InstaFollower:
    def __init__(self):
        chrome_opts = webdriver.ChromeOptions()
        chrome_opts.add_experimental_option("detach", True)
        chrome_opts.add_argument(f"--user-data-dir={CHROME_DRIVER_PATH}")
        self.driver = webdriver.Chrome(options=chrome_opts)
        # driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 20)
        self.url = "https://instagram.com"

    def login(self):
        self.driver.get(self.url + "/accounts/login")
        login_input = self.wait.until(EC.presence_of_element_located(
            (By.NAME, "username")
        ))
        login_input.clear()
        login_input.send_keys(INSTAGRAM_USERNAME)
        pass_input = self.driver.find_element(By.NAME, "password")
        pass_input.clear()
        pass_input.send_keys(INSTAGRAM_PASSWORD, Keys.ENTER)
        self.wait.until(EC.staleness_of(pass_input))

    def find_followers(self):
        self.driver.get(f"{self.url}/{SIMILAR_ACCOUNT}")
        self.wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, f"a[href='/{SIMILAR_ACCOUNT}/followers/']")
        )).click()
        dialog_xpath = "/html/body/div[4]/div[2]/div/div/div[1]/div/div[2]" \
            "/div/div/div/div/div[2]/div/div/div[3]"
        # Scroll the followers popup window
        for _ in range(10):
            followers = self.wait.until(EC.visibility_of_element_located(
                (By.XPATH, dialog_xpath)
            ))
            self.driver.execute_script(
                "arguments[0].scrollTop = arguments[0].scrollHeight",
                followers
            )
            time.sleep(2)

    def follow(self):
        follow_buttons = self.driver.find_elements(
            By.XPATH, "//button//div[text() = 'Follow']"
        )
        for flw_btn in follow_buttons:
            # flw_btn.location_once_scrolled_into_view
            flw_btn.click()
            time.sleep(2)


insta_follower = InstaFollower()
insta_follower.login()
insta_follower.find_followers()
insta_follower.follow()
# insta_follower.driver.quit()
