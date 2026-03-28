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

start_time = time.time()

try:
    print(f"Tracking Performance: {target_url}")
    driver.get(target_url)
    
    # 1. Handle potential 'Wake Up' button (Common on Streamlit Cloud)
    try:
        wake_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Yes, get this app back up!')]"))
        )
        print("App was hibernating. Clicking Wake Up...")
        wake_button.click()
        time.sleep(15) # Wait for reboot
    except:
        pass

    # 2. INCREASED PATIENCE: Wait 60 seconds for the app to fully render
    # We search for 'Neal' or 'Kauffman'
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Kauffman') or contains(text(), 'Neal')]"))
    )
    
    end_time = time.time()
    load_duration = round(end_time - start_time, 2)
    
    # Log to CSV
    with open('app_performance_log.csv', mode='a', newline='') as f:
        csv.writer(f).writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), app_name, load_duration, "Success"])
        
    print(f"Logged: {app_name} loaded in {load_duration}s")

except Exception as e:
    # If it fails, we still want to log the failure but let the script end
    with open('app_performance_log.csv', mode='a', newline='') as f:
        csv.writer(f).writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), app_name, 0, "Failed"])
    print(f"Timeout or Error: {target_url}")
    sys.exit(1)
finally:
    driver.quit()
