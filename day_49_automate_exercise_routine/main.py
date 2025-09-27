"""Day 49. Automating Your Exercise Routine at the Gym"""

from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# TODO: make this robust & clean & readable & maintainable code,
#   first make sure it's working correctly.

ACCOUNT_EMAIL = "my-gym-test@mail.com"
ACCOUNT_PASSWORD = "xcCVBlkj3858#%?790"
GYM_URL = "https://appbrewery.github.io/gym/"
SCHEDULE_DAYS = ["Tue", "Thu", "Mon", "Fri", "Sun"]
CLASS_TYPE = "Spin"
CLASS_TIME = "6:00 PM"

chrome_opts = webdriver.ChromeOptions()
chrome_opts.add_experimental_option("detach", True)
user_data_dir = Path().absolute() / "chrome_profile"
chrome_opts.add_argument(f"--user-data-dir={user_data_dir}")
driver = webdriver.Chrome(options=chrome_opts)
# driver.maximize_window()
driver.get(GYM_URL)
wait = WebDriverWait(driver, 5)  # TODO: 10

booked_classes = 0
joined_waitlists = 0
classes_already_joined = 0
total_date_classes = 0
detailed_classes = []

def retry(func, retries=7, description=None):
    for i in range(7):
        print(f"{description}. Attempt: {i+1}")
        try:
            func()
            break
        except:
            pass


def login():
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
    print("Successfully logged in!")


def book_class():
    global booked_classes
    global joined_waitlists
    global classes_already_joined
    global total_date_classes
    global detailed_classes

    class_days = driver.find_elements(By.CSS_SELECTOR, "div[id*='day-group']")
    # driver.find_elements(By.CSS_SELECTOR, "h2[id*='day-title']")
    # driver.find_element(By.XPATH, "//h2[contains(@id, 'day-title')]")
    for day in class_days:
        class_date = day.find_element(By.TAG_NAME, "h2")
        # if SCHEDULE_DAYS not in class_date.text:
        has_weekday = any(weekday in class_date.text for weekday in SCHEDULE_DAYS)
        if not has_weekday:
            continue
        gym_classes = day.find_elements(By.CSS_SELECTOR, "h3[id*='class-name']")
        gym_times = day.find_elements(By.CSS_SELECTOR, "p[id*='class-time']")
        for gym_class, gym_time in zip(gym_classes, gym_times):
            if CLASS_TYPE in gym_class.text and CLASS_TIME in gym_time.text:
                # Click join waitlist OR book class button
                button = gym_class.find_element(
                    By.XPATH, "./parent::div/following-sibling::div/button")
                # button.location_once_scrolled_into_view
                driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'center'});", button
                )
                message = f"{CLASS_TYPE} Class on {class_date.text}"
                if button.text.lower().startswith("join") or \
                    button.text.lower().startswith("wait"):
                    msg = "Joined Waitlist: " + message
                    card_type = "Waitlist"
                    joined_waitlists += 1 if button.is_enabled() else 0
                else:
                    msg = "Booked: " + message
                    card_type = "Booking"
                    booked_classes += 1 if button.is_enabled() else 0

                if button.is_enabled():
                    button.click()
                    driver.implicitly_wait(0.5)
                    # wait.until_not(EC.element_to_be_clickable(button))
                    wait.until_not(EC.element_to_be_clickable(
                        (By.XPATH, "./parent::div/following-sibling::div/button")
                    ))
                    detailed_classes.append(f"• [New {card_type}] {message}")
                    msg = "✓ " + msg
                else:
                    msg = "✓ Already " + msg
                print(msg)
                break
        else:
            continue
        # Count chosen date's joined/booked classes
        for button in day.find_elements(By.CSS_SELECTOR, "button[id^='book-button-']"):
            total_date_classes += 0 if button.is_enabled() else 1


def get_my_bookings():
    global booked_classes
    global joined_waitlists
    global classes_already_joined
    global total_date_classes
    global detailed_classes
    # Verifying & calculating booked classes
    # Go to My Bookings page
    driver.find_element(By.ID, "my-bookings-link").click()
    my_bookings = wait.until(EC.visibility_of_element_located(
        (By.ID, "my-bookings-page")
    ))
    classes_already_joined = len(my_bookings.find_elements(
        By.CSS_SELECTOR, "div[id*='-card-']"))
    # Fix the calculation
    classes_already_joined -= (booked_classes + joined_waitlists)
    if classes_already_joined < 0:
        classes_already_joined = 0

    summary = f"""
    --- BOOKING SUMMARY ---
    New Bookings: {booked_classes}
    New Waitlist Entires: {joined_waitlists}
    Already Booked/Waitlisted: {classes_already_joined}
    Total {' & '.join(SCHEDULE_DAYS)} {CLASS_TIME} {CLASS_TYPE} \
    Classes: {total_date_classes}
    """
    if detailed_classes:
        summary += f"\n--- DETAILED CLASS LIST ---\n{'\n'.join(detailed_classes)}"
    print(summary)


retry(login, description="Trying Login")  # TODO: retry=10
retry(book_class, description="Trying Booking")  # TODO: retry=10
retry(get_my_bookings, description="Trying Verify My Bookings")  # TODO: retry=10

# driver.quit()
