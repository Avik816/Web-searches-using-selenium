# Code authored by Avik Chakraborty.
# This python script scrapes critics reviews from Rotten Tomatoes.
# Selenium is used to automate the process.

# Importing necessary libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import time, pandas

driver = webdriver.Chrome()

driver.get('https://www.rottentomatoes.com/m/batman_v_superman_dawn_of_justice/reviews?type=user')

wait = WebDriverWait(driver = driver, timeout = 20)

# Clicking all the load-more buttons.
def click_LoadMore_buttons():
    while True:
        try:
            LoadMore_button = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, '//*[@class="load-more-container"]/rt-button')))

            LoadMore_button.click()

            time.sleep(2)

        except Exception as e:
            break

click_LoadMore_buttons()

print('<-----All the Buttons are clicked----->')
print('<-----Commencing Scrapping----->')

# Scrapping all the username
names = driver.find_elements(by = By.CLASS_NAME, value = 'display-name')

# Scrapping all the date of upload
dateOfUpload = driver.find_elements(by = By.XPATH, value = '//*[@class="original-score-and-url"]/span')

# Scrapping all the reviews
reviews = driver.find_elements(by = By.CLASS_NAME, value = 'review-text')


# Saving the scrapped data into a csv file.
name_of_reviewer = []
for index, name in enumerate(names):
    name_of_reviewer.append(name.text)

date_of_upload = []
for index, date in enumerate(dateOfUpload):
    date_of_upload.append(date.text)

review_title = []
for index, review in enumerate(reviews):
    review_title.append(review.text)

rottom = {'Name' : name_of_reviewer, 'Date of Upload' : date_of_upload, 'Reviews' : review_title}


# Saving the files
rottom = pandas.DataFrame(rottom)
rottom.to_csv('datasets/rot-tom users review.csv', index = False)

driver.close()