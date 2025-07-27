from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Initialize the Chrome WebDriver (make sure chromedriver is in PATH)
driver = webdriver.Chrome()

try:
    # Open Google
    driver.get("https://www.google.com")

    # Find the search box, type in a query, and hit ENTER
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys("Selenium Python")
    search_box.send_keys(Keys.RETURN)

    # Wait for a few seconds to let results load
    time.sleep(3)

    # Print the title of the page
    print("Page title is:", driver.title)

finally:
    # Close the browser
    driver.quit()

