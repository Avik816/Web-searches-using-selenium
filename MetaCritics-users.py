# Code authored by Avik Chakraborty.
# This python script scrapes critics reviews from Meta Critics - Users Section.
# Selenium is used to automate the process.

# Importing necessary libraries
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
import time, pandas

driver = webdriver.Chrome()

driver.get('https://www.metacritic.com/movie/batman-v-superman-dawn-of-justice/user-reviews/')

wait = WebDriverWait(driver = driver, timeout = 50)


# Scroll down to the bottom of the page
lastHeight = driver.execute_script("return document.body.scrollHeight")

# Scrolling down the entire page to load all the comments
while True:
    # Scroll down to the bottom of the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    # Wait for new content to load (adjust time as necessary)
    time.sleep(5)
    
    # Calculate new scroll height and compare it with the last scroll height
    newHeight = driver.execute_script("return document.body.scrollHeight")
    
    if newHeight == lastHeight:
        break  # Exit the loop if we have reached the bottom of the page
    
    lastHeight = newHeight


# Scrapping begins
# Scrapping all the username
# names = driver.find_elements(by = By.CLASS_NAME, value = 'c-siteReviewHeader_username')
names = wait.until(expected_conditions.visibility_of_all_elements_located((By.CLASS_NAME, 'c-siteReviewHeader_username')))

# Scrapping all the date of upload
# dateOfUpload = driver.find_elements(by = By.CLASS_NAME, value = 'c-siteReviewHeader_reviewDate')
dateOfUpload = wait.until(expected_conditions.visibility_of_all_elements_located((By.CLASS_NAME, 'c-siteReviewHeader_reviewDate')))

# Scrapping all the reviews
# reviews = driver.find_elements(by = By.CLASS_NAME, value = 'c-siteReview_quote')
reviews = wait.until(expected_conditions.visibility_of_all_elements_located((By.CLASS_NAME, 'c-siteReview_quote')))


# Saving the scrapped data into a csv file.
name_of_reviewer = []
for index, name in enumerate(names):
    name_of_reviewer.append(name.text)

date_of_upload = []
for index, date in enumerate(dateOfUpload):
    date_of_upload.append(date.text)

review_list = []
for index, review in enumerate(reviews):
    review_list.append(review.text)

MetaCritic = {'Name' : name_of_reviewer, 'Date of Upload' : date_of_upload, 'Reviews' : review_list}

# Saving the files
MetaCritic = pandas.DataFrame(MetaCritic)
MetaCritic.to_csv('datasets/MetaCritic users review.csv', index = False)

driver.close()