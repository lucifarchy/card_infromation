import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

# 서버에서 화면 없이 실행하기 위한 설정
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=options)

print("크롤링 시작...")
driver.get("https://www.card-gorilla.com/event?cate=ING")
time.sleep(3)

data = []
items = driver.find_elements(By.CSS_SELECTOR, "div.event_list ul li")

for item in items:
    try:
        title = item.find_element(By.CSS_SELECTOR, "p.txt").text
        date = item.find_element(By.CSS_SELECTOR, "p.date").text
        tag = item.find_element(By.CSS_SELECTOR, "span.tag").text

        # '해외'나 '여행' 글자가 들어간 것만 수집
        if "해외" in title or "여행" in title or "항공" in title:
            data.append({"카드사": tag, "이벤트명": title, "기간": date})
    except:
        continue

driver.quit()

# 결과 저장
df = pd.DataFrame(data)
df.to_csv("benefits.csv", index=False)
print("크롤링 완료 및 저장 끝!")
