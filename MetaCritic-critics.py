# Code authored by Avik Chakraborty.
# This python script scrapes critics reviews from Meta Critics - Critics Section.
# Selenium is used to automate the process.

# Importing necessary libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
import time, pandas

driver = webdriver.Chrome()

driver.get('https://www.metacritic.com/movie/batman-v-superman-dawn-of-justice/critic-reviews/')

# Scrapping all the username
names = driver.find_elements(by = By.CLASS_NAME, value = 'c-siteReview_criticName')

# Scrapping all the date of upload
dateOfUpload = driver.find_elements(by = By.CLASS_NAME, value = 'c-siteReviewHeader_reviewDate')

# Scrapping all the reviews
reviews = driver.find_elements(by = By.CLASS_NAME, value = 'c-siteReview_quote')


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
MetaCritic.to_csv('datasets/MetaCritic critics review.csv', index = False)

driver.close()