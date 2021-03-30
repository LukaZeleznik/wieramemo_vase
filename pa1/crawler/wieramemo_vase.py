from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup

# Define Browser Options
chrome_options = Options()
chrome_options.add_argument("--headless") # Hides the browser window

# Reference the local Chromedriver instance
chrome_path = r'./chromedriver'
driver = webdriver.Chrome(options=chrome_options)
# Run the Webdriver, save page an quit browser
driver.get("https://www.gov.si/")
# Scroll page to load whole content
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    # Scroll down to the bottom.
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # Wait to load the page
    time.sleep(2)
    # Calculate new scroll height and compare with last height.
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

htmltext = driver.page_source
driver.quit()

# Parse HTML structure
soup = BeautifulSoup(htmltext, "lxml")
# Extract links to profiles from TWDS Authors
authors = []
""" for link in soup.find_all("a", class_="link link--darker link--darken u-accentColor--textDarken u-baseColor--link u-fontSize14 u-flex1"): """
for link in soup.find_all("a"):
    authors.append(link.get('href'))

print(authors)