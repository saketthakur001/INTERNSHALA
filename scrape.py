
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
import pandas as pd

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
            comments_data.append({'comment': comment.replace('Verified', ''), 'time': timestamp, 'likes': likes})
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
    return {'comment': comment.replace('Verified', ''), 'time': timestamp, 'likes': likes}


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
            user_id = user_link.strip('/')
            # send request to get the user name
            # user_name = Get_User_Name_From_Insta(f"https://www.instagram.com{user_link}")
            # time.sleep(1)
            user_name = 'none'
            # Extract the comment text
            comment_text = li.get_text().replace(user_id, '', 1).strip()
            # comments_data.append(comment_text.strip('ReplyComment OptionsLike'))
            post_link = driver.current_url
            if 'ReplySee translationComment OptionsLike' in comment_text:
                print(comment_text)
            comment_data = purify_comments(comment_text.replace('ReplyComment OptionsLike', '').replace('ReplySee translationComment OptionsLike', ''))
            # print(comment_data['comment'])
            
            comments_data.append({
                'user-id': user_id,
                # 'uesrname': user_name['user_name'],
                'Posted * time ago' : comment_data['time'],
                'comment': comment_data['comment'],
                'post_link': post_link,
                'User_Profile_link': f"https://www.instagram.com{user_link}",
            })
            if comment_data['time'] == None:
                print(comment_data)
            print(comment_data['time'])
    return comments_data

import requests
from bs4 import BeautifulSoup

# example url
#url = "https://www.instagram.com/hdfcbank/"

def Get_User_Name_From_Insta(user_profile_link):
    # Send a GET request to the URL
    response = requests.get(user_profile_link)
    # Check if the request was successful (status code 200 means success)
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Get the entire HTML content of the page
        html_content = soup.prettify()
        # Print or use the HTML content as needed    # Get the text from the HTML
        page_text = soup.get_text()
        # print(html_content)
        # print(page_text)
        txt = page_text.strip().split('•')[0].split('(@')
        user_name = txt[0].strip()
        user_id = txt[1].split(')')[0]
        # print(user_name, user_id)
        return {'user_name' : user_name, 'user_id' :  user_id}
    else:
        print(f"Failed to retrieve the page. Status Code: {response.status_code}")


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
    # click on the next button
    # Find the specific button inside the div with classes "_aaqg _aaqh" and click on it
    specific_button = driver.find_element(By.CSS_SELECTOR, "div._aaqg._aaqh > button._abl-")
    specific_button.click()


# Flatten the list
flat_list = [item for sublist in posts for item in sublist]

# Convert the list of dictionaries to a DataFrame
df = pd.DataFrame(flat_list)

# Save the DataFrame to a csv file
df.to_csv('comments.csv', index=False)

time.sleep(1000)

