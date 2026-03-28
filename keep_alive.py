import sys
import time
import csv
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

target_url = sys.argv[1]
app_name = "Portfolio" if "portfolio" in target_url else "Reference Guide"

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

start_time = time.time() # Start the timer

try:
    print(f"Tracking Performance: {target_url}")
    driver.get(target_url)
    
    # Wait for the app to load content
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Kauffman')]"))
    )
    
    end_time = time.time() # Stop the timer
    load_duration = round(end_time - start_time, 2)
    
    # Log the data to a CSV
    log_entry = [datetime.now().strftime("%Y-%m-%d %H:%M:%S"), app_name, load_duration, "Success"]
    
    with open('app_performance_log.csv', mode='a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(log_entry)
        
    print(f"Logged: {app_name} loaded in {load_duration}s")

except Exception as e:
    with open('app_performance_log.csv', mode='a', newline='') as f:
        csv.writer(f).writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), app_name, 0, f"Failed: {str(e)[:50]}"])
    print(f"CRITICAL ERROR: {e}")
    sys.exit(1)
finally:
    driver.quit()
