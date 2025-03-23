from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import time
from datetime import datetime, timedelta

airlines = {}

# 开始日期和结束日期
START_DATE = datetime(2025, 1, 1)
END_DATE = datetime(2025, 12, 31)

# 定义间隔天数
interval = timedelta(days=7)

# 初始化列表
start_dates = []
end_dates = []

# 生成日期对
current_start = START_DATE
while current_start + interval <= END_DATE:
    current_end = current_start + interval  # 计算结束日期
    start_dates.append(current_start.strftime("%b %d").upper())
    end_dates.append(current_end.strftime("%b %d").upper())
    current_start += timedelta(days=1)  # 开始日期向后移动一天


PATH = "C:/Users/winst/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe"
service = Service(PATH)
options = Options()
options.add_argument('--headless')

# 啟動 WebDriver
driver = webdriver.Chrome(service=service, options=options)

driver.get("https://www.google.com/travel/flights?tfs=CBsQAhopEgoyMDI0LTEyLTI5ag0IAxIJL20vMDJtdzgwcgwIAxIIL20vMDdkZmsaKRIKMjAyNS0wMS0wNmoMCAMSCC9tLzA3ZGZrcg0IAxIJL20vMDJtdzgwQAFIAVIDVFdEcAF6bENqUklXVVpGTjNCRU15MDRMVWxCU2xSQmNFRkNSeTB0TFMwdExTMHRkR3hpWTJVeU1FRkJRVUZCUjJST2RsQlJSMlJZYzBWQkVnVkdSREl6TkJvS0NOUkFFQUFhQTFSWFJEZ2NjS2ZHQVE9PZgBAbIBGBIIL20vMDdkZmsqDAgDEggvbS8wN2Rmaw&sa=X&ved=0CAUQtY0DahcKEwjo0p6Dn4mKAxUAAAAAHQAAAAAQLQ")

location = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//input[@aria-label='Where from?']"))
)
location.clear()
location.send_keys("TPE")
suggestion = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//li[@data-code='TPE']"))
)
suggestion.click()

filter = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Stops, Not selected']"))
)
filter.click()

non_stop = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//label[@class='WC9k7 eoY5cb' and text()='Nonstop only']"))
)
non_stop.click()

close = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Close dialog']"))
)
close.click()

date_dialog = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//input[@aria-label='Departure']"))
)
date_dialog.click()
# date_begin.send_keys(Keys.CONTROL + "a")
# date_begin.send_keys(start_dates[0])
# date_begin.send_keys(Keys.RETURN)

# date_end = WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.XPATH, "//input[@aria-label='Return']"))
# )
# date_end.send_keys(Keys.CONTROL + "a")
# date_end.send_keys(end_dates[0])
# date_end.send_keys(Keys.RETURN)
time.sleep(2)
reset = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[@jsname='S9gUrf']"))
)
reset.click()
time.sleep(2)
next = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[@jsname='KpyLEe']"))
)
for i in range(10):
    next.click()
    time.sleep(2)

temp = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//div[@jsname='qCDwBb']"))
)

prices = driver.find_elements(By.XPATH, "//div[@jsname='qCDwBb']")
date = driver.find_elements(By.XPATH, "//div[@jsname='nEWxA']")

pr = []
da = []
for price in prices:
    if price.text == "":
        pr.append("NaN")
    else:
        pr.append(price.text)

for d in date:
    da.append(d.get_attribute('aria-label'))
    #print(d.get_attribute('aria-label'))

df = pd.DataFrame({
    'Date' : da,
    'Prices' : pr
})
print(df)
df.to_csv("airline.csv")

# time.sleep(2)
# WebDriverWait(driver, 10).until(
#     EC.presence_of_element_located((By.XPATH, "//div[@class='YMlIz FpEdX jLMuyc']"))
# )

# al_prices = np.array([])
# tmp = np.array([])
# low_prices = driver.find_elements(By.XPATH, "//div[@class='YMlIz FpEdX jLMuyc']")

# for price in low_prices:
#     if price.text != "":
#         temp = price.text
#         al_prices = np.append(al_prices, temp)
#         print(temp)

# com_prices = driver.find_elements(By.XPATH, "//div[@class='YMlIz FpEdX']")
# for price in com_prices:
#     if price.text != "":
#         temp = price.text
#         al_prices = np.append(al_prices, temp)
#         print(temp)

# WebDriverWait(driver, 10).until(
#     EC.presence_of_element_located((By.XPATH, "//span[@class='h1fkLb']"))
# )

# with open("page_source.html", "w", encoding="utf-8") as file:
#     file.write(driver.page_source)

# page_source = driver.page_source
# soup = BeautifulSoup(page_source, 'html.parser')

# al_name = []
# # 假設我們要找所有 class 為 h1fkLb 的 span 元素
# spans = soup.find_all('span', class_='h1fkLb')
# for i, span in enumerate(spans):
#     if i >= len(al_prices):
#         break
#     al_name.append(span.get_text())
#     print(span.get_text())


driver.quit()