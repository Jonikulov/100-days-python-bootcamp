"""Day 51. Internet Twitter Complaining Bot"""

import os
from pathlib import Path
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()

PROMISED_DOWN = 100
PROMISED_UP = 10
CHROME_DRIVER_PATH = Path("../chrome_profile").absolute().resolve()
TWITTER_USERNAME = os.getenv("TWITTER_USERNAME")
TWITTER_EMAIL = os.getenv("TWITTER_EMAIL")
TWITTER_PASSWORD = os.getenv("TWITTER_PASSWORD")
TWITTER_URL = "https://twitter.com/login"
SPEED_TEST_URL = "https://speedtest.net"

class InternetSpeedTwitterBot:
    def __init__(self):
        chrome_opts = webdriver.ChromeOptions()
        chrome_opts.add_experimental_option("detach", True)
        chrome_opts.add_argument(f"--user-data-dir={CHROME_DRIVER_PATH}")
        self.driver = webdriver.Chrome(options=chrome_opts)
        # self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 100)
        self.down = 0  # PROMISED_DOWN
        self.up = 0  # PROMISED_UP
        self.result_link = None

    def get_internet_speed(self):
        print("Checking the internet speed via SpeedTest...")
        self.driver.get(SPEED_TEST_URL)
        # Click run button to start measuring internet speed
        run = self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "div.start-button a")
                # (By.XPATH, "//a[@role='button']/span[contains(text(), 'Go')]")
        ))
        run.click()
        # Get the result link
        result_id = self.wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "div[data-result-id='true']")
        )).text
        # Get the download speed
        self.down = float(self.driver.find_element(
            By.CSS_SELECTOR, "span.download-speed"
        ).text)
        # Get the upload speed
        self.up = float(self.driver.find_element(
            By.CSS_SELECTOR, "span.upload-speed"
        ).text)
        self.result_link = f"{SPEED_TEST_URL}/result/{result_id}"
        print("DOWNLOAD (Mbps):", self.down)
        print("UPLOAD (Mbps):", self.up)
        print("Result Link:", self.result_link)

    def tweet_at_provider(self):
        if self.down == 0 or self.down > PROMISED_DOWN / 5:
            return
        print("Speed is signifantly slow, tweeting about it...")
        # Go to the twitter login page
        self.driver.get(TWITTER_URL)
        # Enter email and continue
        login_input = self.wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "input[name='text']")
        ))
        login_input.clear()
        login_input.send_keys(TWITTER_EMAIL, Keys.ENTER)
        # Enter password and login
        pass_input = self.wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "input[name='password']")
        ))
        pass_input.clear()
        pass_input.send_keys(TWITTER_PASSWORD, Keys.ENTER)
        # Input the tweet text
        message = f"Hey <Internet Provider>, why is my internet speed " \
            f"↓{self.down} / ↑{self.up} when I pay for ↓{PROMISED_DOWN}" \
            f" / ↑{PROMISED_UP}?\n{self.result_link}"
        msg_input = self.wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR,
            "div.DraftEditor-root div.public-DraftStyleDefault-block")
        ))
        msg_input.send_keys(message)
        # Click post button
        self.driver.find_element(
            By.CSS_SELECTOR, "button[data-testid='tweetButtonInline']"
        ).click()
        print("Tweeted message:", message)


if __name__ == "__main__":
    bot = InternetSpeedTwitterBot()
    bot.get_internet_speed()
    bot.tweet_at_provider()
    # bot.driver.quit()
