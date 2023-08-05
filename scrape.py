
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
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup


# Your existing setup
options = webdriver.ChromeOptions()
options.add_argument("--user-data-dir=C:\\Temp\\ChromeProfile")
driver = webdriver.Chrome(options=options)


def get_comments(comments_html):
    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(comments_html, 'html.parser')

    # Extract comments along with usernames and their links
    comments_data = []
    for li in soup.find_all('li'):
        # Check for a username and its associated link within the comment
        user_link_element = li.find('a')
        if user_link_element:
            user_link = user_link_element.get('href')
            # Extract the username from the user link (assuming the format is "/username/")
            username = user_link.strip('/')
            # Extract the comment text
            comment_text = li.get_text().replace(username, '', 1).strip()
            comments_data.append(comment_text.strip('ReplyComment OptionsLike'))
            # ({
            #     # 'user-id': username,
            #     # 'User_Profile_link': f"https://www.instagram.com{user_link}",
            #     'comment': comment_text.strip('ReplyComment OptionsLike')
            # })

    # Further refine the extraction process to capture the timestamp, likes, and clean up the comment text
    # for comment in comments_data:
        # print(comment)

    return comments_data
        # Extract the timestamp using regex
        # timestamp_match = re.search(r'(\d+[smh])', comment['comment'])
        # if timestamp_match:
        #     comment['time'] = timestamp_match.group(1)
        #     # Remove the timestamp from the comment text
        #     comment['comment'] = comment['comment'].replace(comment['time'], '', 1).strip()
        #     print(comment['comment'])

    #     # Extract the likes count using regex
    #     likes_match = re.search(r'(\d+) like', comment['comment'])
    #     if likes_match:
    #         comment['likes'] = int(likes_match.group(1))
    #         # Remove the likes count from the comment text
    #         comment['comment'] = comment['comment'].replace(f"{comment['likes']} like", '', 1).strip()
    #     else:
    #         likes_match = re.search(r'(\d+) likes', comment['comment'])
    #         if likes_match:
    #             comment['likes'] = int(likes_match.group(1))
    #             # Remove the likes count from the comment text
    #             comment['comment'] = comment['comment'].replace(f"{comment['likes']} likes", '', 1).strip()
    #         else:
    #             comment['likes'] = 0

    #     # Remove any metadata from the comment text
    #     comment['comment'] = comment['comment'].replace('ReplyComment OptionsLike', '', 1).strip()
    # return comments_data



# Navigate to the Instagram page
driver.get('https://www.instagram.com/hdfcbank/')

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

# print(html_content)


# Scroll to the bottom of the comments section
actions = ActionChains(driver)
actions.move_to_element(ul_element).perform()


# Scroll to the bottom of the comments section
actions = ActionChains(driver)
actions.move_to_element(ul_element).perform()


# comments and other details
posts = []

# Wait a bit for potential loading animations or transitions
# time.sleep(2)

for i in range(6):
    comments_container = driver.find_element(By.CSS_SELECTOR, "ul._a9z6._a9za")
    button = True
    while button:
        button = False
        # Use JavaScript to scroll to the bottom of the comments container/modal
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", comments_container)
        print('scrolling to the bottom')
        time.sleep(1.5)

        # Check if the "Load more comments" button with the specific attributes is present
        try:
            load_more_button = driver.find_element(By.CSS_SELECTOR, 'button._abl- div._abm0 svg[aria-label="Load more comments"]')
            load_more_button.click()
            print('hurray clicked on the button 😎😎')
            button = True
            # Optionally add a sleep after clicking the button to ensure the new comments are loaded
            time.sleep(.5)

        except NoSuchElementException:
            # If the button is not found, it means all comments are already loaded or the specific button is not present
            pass

    # Find the ul element with classes _a9z6 _a9za
    ul_element = driver.find_element(By.CSS_SELECTOR, "ul._a9z6._a9za")

    # Get the inner HTML of the ul element
    html_content = ul_element.get_attribute('outerHTML')
    comments = get_comments(html_content)
    try:
        posts.append(comments)
    except:
        print("didn't work")
    # break
    # click on the next button
    # Find the specific button inside the div with classes "_aaqg _aaqh" and click on it
    specific_button = driver.find_element(By.CSS_SELECTOR, "div._aaqg._aaqh > button._abl-")
    specific_button.click()

import json

# Save the posts list to a text file
with open('test.txt', 'w', encoding='utf-8') as file:
    file.write(json.dumps(posts, indent=4))


time.sleep(1000)

