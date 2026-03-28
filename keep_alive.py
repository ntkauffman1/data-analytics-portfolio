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
app_name = "Portfolio" if "portfolio" in target_url else "Reference Guide"

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def check_app(url):
    start_time = time.time()
    # Try up to 3 times to find the app content
    for attempt in range(3):
        try:
            print(f"Attempt {attempt + 1} for: {url}")
            driver.get(url)
            
            # Look for 'Kauffman' or 'Neal' with a 45-second timeout per attempt
            WebDriverWait(driver, 45).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Kauffman') or contains(text(), 'Neal')]"))
            )
            
            load_duration = round(time.time() - start_time, 2)
            return load_duration, "Success"
        except Exception as e:
            print(f"Attempt {attempt + 1} failed. Retrying...")
            time.sleep(5)
    return 0, "Failed"

try:
    duration, status = check_app(target_url)
    
    # Log the results
    with open('app_performance_log.csv', mode='a', newline='') as f:
        csv.writer(f).writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), app_name, duration, status])
        
    if status == "Success":
        print(f"✅ {app_name} loaded in {duration}s")
    else:
        print(f"❌ {app_name} failed all retries.")
        sys.exit(1)

finally:
    driver.quit()
