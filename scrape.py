# Your existing imports
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as chromeOptions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import os
import time
import re

# Additional imports
from selenium.webdriver.common.action_chains import ActionChains

# Your existing setup
options = webdriver.ChromeOptions()
options.add_argument("--user-data-dir=C:\\Temp\\ChromeProfile")
driver = webdriver.Chrome(options=options)

# Navigate to the Instagram page
driver.get('https://www.instagram.com/hdfcbank/')

# test
# driver.get('https://www.instagram.com/p/CvKmgR1Ij4f/')
# test

# Wait for the posts to load
# time.sleep(4)


# Wait for the div with class _aagw to be clickable
element = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "div._aagw"))
)

# Click on the element
element.click()
# Find the ul element with classes _a9z6 _a9za
ul_element = driver.find_element(By.CSS_SELECTOR, "ul._a9z6._a9za")

# Get the inner HTML of the ul element
html_content = ul_element.get_attribute('outerHTML')

print(html_content)


# Scroll to the bottom of the comments section
actions = ActionChains(driver)
actions.move_to_element(ul_element).perform()

# Wait a bit for potential loading animations or transitions
time.sleep(2)


# Importing Keys
from selenium.webdriver.common.keys import Keys

# ... [Your existing code]

# Send the "End" key to the page to scroll to the bottom
driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)

# Wait a bit to ensure the page has scrolled to the end and any potential loading animations complete
time.sleep(2)

# Check if a button with class "_abl-" is present
try:
    load_more_button = driver.find_element(By.CSS_SELECTOR, "button._abl-")
    if load_more_button:
        load_more_button.click()
        # Optionally add a sleep after clicking the button to ensure the new comments are loaded
        time.sleep(2)
except NoSuchElementException:
    # If the button is not found, it means all comments are already loaded or there's no more button
    pass

# ... [The rest of your code]





# # Check if a button with class "_abl-" is present
# try:
#     load_more_button = driver.find_element(By.CSS_SELECTOR, "button._abl-")
#     if load_more_button:
#         load_more_button.click()
#         # Optionally add a sleep after clicking the button to ensure the new comments are loaded
#         time.sleep(2)
# except NoSuchElementException:
#     # If the button is not found, it means all comments are already loaded or there's no more button
#     pass

# ... [The rest of your code]


time.sleep(1000)