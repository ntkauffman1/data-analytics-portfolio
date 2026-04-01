import sys
import time
import csv
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

target_url = sys.argv[1]
app_id = "portfolio" if "portfolio" in target_url else "guide"

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
# Simulate a real laptop screen size
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def check_app(url):
    start_time = time.time()
    # Try 3 times with longer waits
    for attempt in range(3):
        try:
            print(f"Attempt {attempt + 1} for: {url}")
            driver.get(url)
            
            # Wait for any element to appear first
            time.sleep(10) 
            
            # Look for ANY part of your name (case insensitive)
            WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'kauffman') or contains(text(), 'Neal')]"))
            )
            
            return round(time.time() - start_time, 2), "Success"
        except Exception as e:
            print(f"Attempt {attempt + 1} failed. Details: {str(e)[:100]}")
            # Take a screenshot on the last failure to debug
            if attempt == 2:
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
                error_filename = f"error_{appid}_{timestamp}.png"
                driver.save_screenshot(error_filename)
                print(f"Screenshot saved: {error_filename}")
                time.sleep(10)  # Optional now with timestamped files
    return 0, "Failed"

try:
    duration, status = check_app(target_url)
    
    with open('app_performance_log.csv', mode='a', newline='') as f:
        csv.writer(f).writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), app_id, duration, status])
        
    if status == "Success":
        print(f"✅ {app_id} is LIVE ({duration}s)")
    else:
        print(f"❌ {app_id} FAILED - Check the error screenshot in the repo!")
        sys.exit(1)
finally:
    driver.quit()
