from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import os

# Initialize variables
PATH = "C:/Users/winst/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe"
service = Service(PATH)
options = Options()
options.add_argument('--headless')
# Launch the WebDriver
driver = webdriver.Chrome(service=service, options=options)

# Read the input CSV
source = pd.read_csv("output4.csv")

# Loop over each URL in the source data
for idx, row in source.iterrows():
    start_time = time.time()

    url = row['url']
    hotel_name = row['Hotel Name']
    index = row['Unnamed: 0']
    print("4processing..." + hotel_name)
    print(index)
    
    driver.get(url)
    driver.maximize_window()

    # Execute the extraction process
    time.sleep(1)
    checkin = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@jscontroller='ViZxZe']"))
    )
    checkin.click()
    time.sleep(1)
    
    top = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@jsname='S9gUrf']"))
    )
    top.click()
    
    done = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@jsname='iib5kc']"))
    )
    
    nextpage = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@class='d53ede rQItBb FfP4Bc Gm3csc']"))
    )
    
    time.sleep(1)
    
    date = WebDriverWait(driver, 10).until(
        EC.visibility_of_any_elements_located((By.XPATH, "//div[@jsname='nEWxA']"))
    )
    
    prices = []
    d = []
    
    prs = driver.find_elements(By.XPATH, "//div[@jsname='qCDwBb']")  # Prices
    tmp = driver.find_elements(By.XPATH, "//div[@jsname='nEWxA']")   # Dates
    
    for tmps in tmp:
        a_l = tmps.get_attribute('aria-label')
        d.append(a_l)
    
    time.sleep(1)
    for k in range(11):
        nextpage.click()
        time.sleep(1)

    j = 0
    for pr in prs:
        if pr.text == "" or pr.text == "——":
            prices.append("NaN")
        else:
            prices.append(pr.text)
        j += 1

    done.click()
    # Extract the rate value
    rate = "NaN"  # Default value in case rate is not found
    try:
        rate_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='yOgEz IVklEb']"))
        )
        rate = rate_element.text
    except Exception as e:
        print(f"Rate not found for {hotel_name}: {e}")
    
    # Collect the data for each hotel
    all_data = []
    for i in range(len(d)):
        all_data.append({
            'Hotel Name': hotel_name,
            'rate': rate,
            'date': d[i],
            'price': prices[i] if i < len(prices) else "NaN",
        })
    
    # Save the data for the current URL to a CSV file named after the hotel name or URL
    filename = f"{"4_" + str(index)}.csv"
    if not os.path.exists(filename):
        # If file doesn't exist, write headers
        df = pd.DataFrame(all_data)
        df.to_csv(filename, mode='w', header=True, index=False)
    else:
        # If file exists, append data
        df = pd.DataFrame(all_data)
        df.to_csv(filename, mode='a', header=False, index=False)

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"程式碼段落執行時間: {execution_time:.6f} 秒")
    print(f"結果: {index}")


# Close the WebDriver
driver.quit()

print("Data collection completed and saved to separate CSV files.")
