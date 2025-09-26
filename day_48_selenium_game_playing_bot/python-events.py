from selenium import webdriver
from selenium.webdriver.common.by import By

# Keep browser open even after program finishes
chrome_opts = webdriver.ChromeOptions()
chrome_opts.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_opts)
driver.get("https://python.org")

upcoming_events = driver.find_element(
    By.XPATH, '//*[@id="content"]//div[2]/div[2]//ul'
)
event_dates = upcoming_events.find_elements(By.TAG_NAME, "time")
event_names = upcoming_events.find_elements(By.TAG_NAME, "a")
events_data = {}
for i in range(len(event_dates)):
    events_data[i] = {
        "time": event_dates[i].text,
        "name": event_names[i].text,
    }

print(events_data)

driver.quit()
