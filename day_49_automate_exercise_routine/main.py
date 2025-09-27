"""Day 49. Automating Your Exercise Routine at the Gym"""

from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

ACCOUNT_EMAIL = "my-gym-test@mail.com"
ACCOUNT_PASSWORD = "xcCVBlkj3858#%?790"
GYM_URL = "https://appbrewery.github.io/gym/"

chrome_opts = webdriver.ChromeOptions()
chrome_opts.add_experimental_option("detach", True)
user_data_dir = Path().absolute() / "chrome_profile"
chrome_opts.add_argument(f"--user-data-dir={user_data_dir}")
driver = webdriver.Chrome(options=chrome_opts)
# driver.maximize_window()

driver.get(GYM_URL)
wait = WebDriverWait(driver, 10)

login_button = wait.until(EC.element_to_be_clickable(
    (By.ID, "login-button"))
)
login_button.click()

email_input = wait.until(EC.presence_of_element_located(
    (By.ID, "email-input")
))
email_input.clear()
email_input.send_keys(ACCOUNT_EMAIL)

password_input = driver.find_element(By.ID, "password-input")
password_input.clear()
password_input.send_keys(ACCOUNT_PASSWORD)

# Click login button
driver.find_element(By.ID, "submit-button").click()
# Wait for the schedule page to load
wait.until(EC.presence_of_element_located(
    (By.ID, "schedule-page")
))

SCHEDULE_DAY = "Tue"
CLASS_TYPE = "Spin"
CLASS_TIME = "6:00 PM"
booked_classes = 0
joined_waitlists = 0
classes_already_available = 0
total_date_classes = 0
class_days = driver.find_elements(By.CSS_SELECTOR, "div[id*='day-group']")
# driver.find_elements(By.CSS_SELECTOR, "h2[id*='day-title']")
# driver.find_element(By.XPATH, "//h2[contains(@id, 'day-title')]")
for day in class_days:
    class_date = day.find_element(By.TAG_NAME, "h2")
    if SCHEDULE_DAY not in class_date.text:
        continue
    gym_classes = day.find_elements(By.CSS_SELECTOR, "h3[id*='class-name']")
    gym_times = day.find_elements(By.CSS_SELECTOR, "p[id*='class-time']")
    for gym_class, gym_time in zip(gym_classes, gym_times):
        if CLASS_TYPE in gym_class.text and CLASS_TIME in gym_time.text:
            # Click join waitlist OR book class button
            button = gym_class.find_element(
                By.XPATH, "./parent::div/following-sibling::div/button")
            # driver.execute_script(
            #     "arguments[0].scrollIntoView({block: 'center'});", button
            # )
            msg = f": {CLASS_TYPE} Class on {class_date.text}"
            if button.text.lower().startswith("join") or \
                button.text.lower().startswith("wait"):
                msg = "Joined Waitlist" + msg
            else:
                msg = "Booked" + msg

            if button.is_enabled():
                button.click()
                msg = "✓ " + msg
            else:
                msg = "✓ Already " + msg
            print(msg)
            break
    else:
        continue
    # Count chosen date's joined/booked classes
    # total_date_classes += ???
    break
else:
    print("Unfortunately, chosen time or gym type currently not available.")


summary = f"""
--- BOOKING SUMMARY ---
Classes booked: {booked_classes}
Waitlists joined: {joined_waitlists}
Already booked/waitlisted: {classes_already_available}
Total {class_date.text} classes: {total_date_classes}
"""
print(summary)

# driver.quit()
