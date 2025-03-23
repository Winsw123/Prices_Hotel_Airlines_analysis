from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import numpy as np
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

airlines = {}

PATH = "C:/Users/winst/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe"
service = Service(PATH)
options = Options()
options.add_argument('--headless')

driver = webdriver.Chrome(service=service, options=options)

driver.get("https://www.google.com/travel/search?q=tokyo%20hotels&ts=CAESCgoCCAMKAggDEAAaUAoyEi4yJTB4NjA1ZDFiODdmMDJlNTdlNzoweDJlMDE2MThiMjI1NzFiODk6BVRva3lvGgASGhIUCgcI6Q8QARgPEgcI6Q8QARgQGAEyAhAAKg4KCBIBAzoDVFdEGgAoCA&sa=X&qs=CAEgASgAOA0&ap=KigKEgl_39EwSNVBQBFa0eY-vXVhQBISCaIkV0Ww20FAEVrR5jIxd2FAMAG6AQdkZXRhaWxz&ved=0CAAQ5JsGahcKEwiY4u6bt7GKAxUAAAAAHQAAAAAQCw")
data = []
urls = []
timeout_limit = 3  # 超时次数限制
timeout_count = 0  # 当前超时计数

for count in range(2):
    try:
        print("processing...")
        print(count)

        for attempt in range(3):  # 最多尝试 3 次
            try:
                test = WebDriverWait(driver, 10).until(
                    EC.visibility_of_any_elements_located((By.XPATH, "//a[@class='PVOOXe']"))
                )
                time.sleep(0.5)  # 稍作延迟，确保稳定
                break  # 成功点击后退出循环
            except StaleElementReferenceException:
                print("StaleElementReferenceException occurred, retrying...")
            except TimeoutException:
                print("Element not found within the timeout period.")
                break
        # 等待 test 出现
        # test = WebDriverWait(driver, 10).until(
        #     EC.visibility_of_any_elements_located((By.XPATH, "//a[@class='PVOOXe']"))
        # )
        targets = driver.find_elements(By.XPATH, "//a[@class='PVOOXe']")

        for target in targets:
            url = target.get_attribute("href")
            urls.append(url)

        time.sleep(1)

        # 等待 amen 元素
        amen = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[@class='lXJaOd']"))
        )
        amens = driver.find_elements(By.XPATH, "//span[@class='lXJaOd']")

        driver.implicitly_wait(10)  # 或使用 WebDriverWait，视页面需求而定

        # 获取页面源代码
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        # 查找目标元素
        amens = soup.find_all("span", class_="lXJaOd")
        for amen in amens:
            print(amen.text)
            data.append(amen.text)

        # 点击下一页
        for attempt in range(3):  # 最多尝试 3 次
            try:
                next_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@jsname='OCpkoe']"))
                )
                time.sleep(0.5)  # 稍作延迟，确保稳定
                next_button.click()
                break  # 成功点击后退出循环
            except StaleElementReferenceException:
                print("StaleElementReferenceException occurred, retrying...")
            except TimeoutException:
                print("Element not found within the timeout period.")
                break
        time.sleep(1)

        # 成功处理一轮后重置 timeout_count
        timeout_count = 0

    except TimeoutException:
        print("TimeoutException occurred while waiting for elements.")
        timeout_count += 1
        if timeout_count >= timeout_limit:  # 超过最大超时次数限制
            print(f"Exceeded timeout limit of {timeout_limit}. Exiting loop.")
            break


parsed_data = []
pattern = r"Amenities for (.*?), a (\d)-star hotel\.: (.*)"

# 遍历每行数据并解析
for i, line in enumerate(data):
    match = re.match(pattern, line)
    if match:
        url = urls[i]
        name = match.group(1)
        stars = int(match.group(2))
        amenities = [amen.strip() for amen in match.group(3).split(",") if amen.strip()]
        parsed_data.append({"Hotel Name": name, "Stars": stars, "Amenities": amenities, "url": url})

# 转为 DataFrame
df = pd.DataFrame(parsed_data)

# 查看解析后的 DataFrame
#print(df)

# 将 Amenities 列进行独热编码
amenities_encoded = pd.get_dummies(df["Amenities"].explode()).groupby(level=0).max()

# 合并原始数据和独热编码结果
df_encoded = pd.concat([df.drop(columns=["Amenities"]), amenities_encoded], axis=1)

# 查看独热编码后的 DataFrame
print(df_encoded)

filepath = r"C:\Users\winst\OneDrive\Desktop\dataS\output3.csv"
df_encoded.to_csv(filepath, sep=',', index=True, encoding='utf-8')




