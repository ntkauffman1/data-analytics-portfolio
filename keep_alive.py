import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

target_url = sys.argv[1]

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    print(f"Checking: {target_url}")
    driver.get(target_url)
    
    # 1. Handle potential 'Wake Up' button
    try:
        wake_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Yes, get this app back up!')]"))
        )
        print("App was hibernating. Clicking Wake Up...")
        wake_button.click()
        time.sleep(20) 
    except:
        pass

    # 2. THE HEALTH CHECK: Look for your name or a key word
    # This ensures the app didn't just load a blank page.
    # We look for 'Kauffman' since it's in your portfolio title.
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Kauffman')]"))
    )
    
    print(f"Verified: App is healthy and displaying content.")

except Exception as e:
    print(f"CRITICAL ERROR: App at {target_url} failed health check!")
    print(f"Details: {e}")
    sys.exit(1) # This tells GitHub the job FAILED so you get an email
finally:
    driver.quit()
