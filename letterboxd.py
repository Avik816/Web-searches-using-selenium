# Code authored by Avik Chakraborty.
# This python script scrapes critics reviews from Meta Critics - Users Section.
# Selenium is used to automate the process.

# Importing necessary libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions
import time, json


driver = webdriver.Chrome()

nextPage = 'https://letterboxd.com/film/batman-v-superman-dawn-of-justice/reviews'
driver.get(nextPage)

index = 1
all_names = []
all_dates = []
all_reviews = []

# wait = WebDriverWait(driver, 20)

while True:

    names = driver.find_elements(by = By.CLASS_NAME, value = 'name')
    dateOfUpload = driver.find_elements(by = By.CLASS_NAME, value = '_nobr')
    reviews = driver.find_elements(by = By.CLASS_NAME, value = 'body-text')


    for name in names:
        # all_names.update({index : name.text})
        all_names.append(name.text)

    for date in dateOfUpload:
        # all_dates.update({index : date.text})
        all_dates.append(date.text)

    for review in reviews:
        # all_reviews.update({index : review.text})
        all_reviews.append(review.text)
    
    nextPage = driver.find_element(by = By.CLASS_NAME, value = 'next')
    parentElement_ClassName = nextPage.find_element(by = By.XPATH, value = '..').get_attribute('class')

    if parentElement_ClassName == 'paginate-nextprev paginate-disabled':
        print('Scrapping Done !')
        break
    else:
        print('Next Page !')
        driver.get(nextPage.get_attribute('href'))
        time.sleep(5)

letterboxd = {'Name' : all_names, 'Date of Upload' : all_dates, 'Reviews' : all_reviews}

with open(file = 'datasets/letterboxd.json', mode = 'w', encoding = 'utf-8') as fp:
    json.dump(letterboxd, fp = fp, indent = 5)

print('File Saved !')

print(all_dates, all_names, all_reviews)

driver.close()