
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


## DISCONTINUED ##
def purify_comments(comments):
    comments_data = []
    for comments in lis:
        # Revised code to handle extraneous characters and extract likes

        # Process each line (comment)
        for comment in comments:
            # Strip newline and leading/trailing spaces
            comment = comment.strip()

            # Remove leading and trailing special characters (", [, ])
            comment = re.sub(r'^[\["]*|[\]",]*$', '', comment)

            # Extract the timestamp and likes using regex
            match = re.search(r'(\d+[smhdw])(\d*)$', comment)
            if match:
                timestamp = match.group(1)
                likes = int(match.group(2)) if match.group(2) else None
                # Remove the timestamp and likes from the comment text
                comment = comment[:comment.rfind(timestamp)].strip()
            else:
                timestamp = None
                likes = None

            # Append to the results list
            comments_data.append({'comment': comment.strip('Verified'), 'time': timestamp, 'likes': likes})
## DISCONTINUED ##

# extracs text from unpure comments
def purify_comments(comment):

    # Remove leading and trailing special characters (", [, ])
    comment = re.sub(r'^[\["]*|[\]",]*$', '', comment)

    # Extract the timestamp and likes using regex
    match = re.search(r'(\d+[smhdw])(\d+)?$', comment)
    if match:
        timestamp = match.group(1)
        likes = int(match.group(2)) if match.group(2) else None
        # Remove the timestamp and likes from the comment text
        comment = comment[:comment.rfind(timestamp)].strip()
    else:
        timestamp = None
        likes = None

    # Append to the results list
    return {'comment': comment.strip('Verified'), 'time': timestamp, 'likes': likes}



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
            # comments_data.append(comment_text.strip('ReplyComment OptionsLike'))
            post_link = driver.current_url
            comment_data = purify_comments(comment_text.strip('ReplyComment OptionsLike'))
            comments_data.append({
                'user-id': username,
                'User_Profile_link': f"https://www.instagram.com{user_link}",
                'comment': comment_data['comment'],
                'post_link': post_link,
                'Posted ** time ago' : comment_data['time'],
            })
    return comments_data



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
    break
    # click on the next button
    # Find the specific button inside the div with classes "_aaqg _aaqh" and click on it
    specific_button = driver.find_element(By.CSS_SELECTOR, "div._aaqg._aaqh > button._abl-")
    specific_button.click()

import json

# Save the posts list to a text file
with open('test.txt', 'w', encoding='utf-8') as file:
    file.write(json.dumps(posts, indent=4))


time.sleep(1000)

