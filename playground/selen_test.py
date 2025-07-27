from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time

# --- CONFIGURATION ---
proxy = "oc-7a572446969ee5c24ffbe8a8ed851cf24600b41a9d898982dbb70c435ec59fbb-country-TR-session-d9242:v1leozow6ges@proxy.oculus-proxy.com:31111"  # Replace with your proxy IP:port

# Set up Chrome options
chrome_options = Options()
# chrome_options.add_argument(f'--proxy-server=http://{proxy}')

# Initialize WebDriver with proxy
driver = webdriver.Chrome(options=chrome_options)

try:
    driver.get("https://www.google.com")
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys("Selenium Python")
    search_box.send_keys(Keys.RETURN)
    time.sleep(3)
    print("Page title is:", driver.title)

finally:
    driver.quit()
