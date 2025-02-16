# Code authored by Avik Chakraborty
# This script scrapes IMDB comments of a movie
# Selenium is used for this approach
# Importing necessary libraries

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import time, pandas

# Initialize the WebDriver
driver = webdriver.Chrome()

# Opening IMDb reviews page.
driver.get('https://www.imdb.com/title/tt2975590/reviews/')

# Setting up a wait object for the dynamic element to load
wait = WebDriverWait(driver, 20) # Setting the timeout for 10 seconds

'''Procedure :
- So the IMDB page shows only few comments each time and hide the rest of the comments.
- The "load more" button shows the next sets of comments each time when clicked.
- The script must load all the commnets first before scrapping all the comments.

The following function does the same.
The function uses a try-except method inside an infinite while loop to load all the comments by clicking the "load more" button, then all the comments are scrapped with the name of the user, date posted and the contents of the comments.'''

def loading_all_comments():
    while True:
        try:
            # Using the wait object to wait untill the 'Load More' button is clickable
            LoadMore_button = wait.until(
                # X-Path of the 'Load More' button.
                expected_conditions.element_to_be_clickable((By.XPATH, "//div[@class='ipl-load-more ipl-load-more--loaded']/button[@id='load-more-trigger']"))
            )

            # Clicking the "Load More" button until all reviews are loaded
            LoadMore_button.click()

            # Waiting for new content to load
            time.sleep(2)

        except Exception as e:
            # Breaking loop if no more 'Load More' button is found or other exceptions occur
            break

loading_all_comments()
print('<-----All the Load-More buttons are clicked----->')
print('<-----Commence Scrapping----->')

# Scrapping of username, date-of-upload, review-title and review-description.
# Scrapping all the username
usernames = driver.find_elements(by = By.XPATH, value = '//*[@class = "display-name-link"]/a')

# Scrapping all the date of upload
dateOfUpload = driver.find_elements(by = By.CLASS_NAME, value = 'review-date')

# Scrapping all the review title
reviewTitle = driver.find_elements(by = By.CLASS_NAME, value = 'title')

# Scrapping all the reviews
reviews = driver.find_elements(by = By.XPATH, value = '//*[@class = "content"]/div[1]')

# Scrapping the review rating
# rating = driver.find_elements(by = By.XPATH, value = '//*[@class = "ipc-rating-star ipc-rating-star--base ipc-rating-star--otherUserAlt review-rating"]/span[1]')
rating = driver.find_elements(by = By.CLASS_NAME, value = 'ipc-rating-star--rating')


'''Now, the textual data from each of the web-elements are extracted and saved in a dictionary using index.
Then the dataframe will be created based on the index and each row will have the data corresponding to the index of the row.'''

usernames_dict = {}
for index, username in enumerate(usernames):
    usernames_dict.update({index : username.text})

dateOfUpload_dict = {}
for index, date in enumerate(dateOfUpload):
    dateOfUpload_dict.update({index : date.text})

reviewTitle_dict = {}
for index, title in enumerate(reviewTitle):
    reviewTitle_dict.update({index : title.text})
    
reviews_dict = {}
for index, title in enumerate(reviews):
    reviews_dict.update({index : title.text})

rating_dict = {}
for index, rate in enumerate(rating):
    rating_dict.update({index : rate.text})

# Forming the dataframe
imdbDF = {}
imdbDF = pandas.DataFrame(imdbDF, columns = ['Username', 'Date of Upload', 'Review Title', 'Review Description', 'Rating (1-10)'])
imdbDF

# Inserting the data at each row, corresponding to the index value
for index in usernames_dict:
    imdbDF.loc[index] = [usernames_dict.get(index), dateOfUpload_dict.get(index), reviewTitle_dict.get(index), reviews_dict.get(index), rating_dict.get(index)]

imdbDF.head()

# Saving the data to a .csv file
imdbDF.to_csv('datasets/imdb reviews1.csv', index = False)
print('File Saved !')

print(rating_dict)

# Closing the browser instance
driver.quit()