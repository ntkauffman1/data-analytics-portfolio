import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Get URL from GitHub Action argument
target_url = sys.argv[1]

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    print(f"Visiting: {target_url}")
    driver.get(target_url)
    
    # Wait to see if the 'Wake Up' button appears (if app is hibernating)
    try:
        wake_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Yes, get this app back up!')]"))
        )
        print("App was sleeping. Clicking 'Wake Up' button...")
        wake_button.click()
        time.sleep(20) # Give it extra time to boot up
    except:
        print("App is already awake or button not found. Proceeding...")

    # Final wait to ensure Streamlit websockets connect
    time.sleep(10)
    print(f"Success! Current page title: {driver.title}")

except Exception as e:
    print(f"Error: {e}")
finally:
    driver.quit()
