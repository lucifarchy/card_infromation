import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

# 1. 브라우저 설정 (사람인 척 속이기)
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("--window-size=1920,1080")
# 중요: 이 줄이 있어야 사이트가 로봇인 줄 모릅니다.
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")

driver = webdriver.Chrome(options=options)

print("카드고릴라 접속 중...")
driver.get("https://www.card-gorilla.com/event?cate=ING")
time.sleep(5) # 로딩 기다리기

data = []

try:
    # 2. 데이터 수집 시도
    items = driver.find_elements(By.CSS_SELECTOR, "div.event_list ul li")
    
    if len(items) == 0:
        print("항목을 찾을 수 없습니다. (사이트 구조 변경 또는 로딩 실패)")
    
    for item in items:
        try:
            title = item.find_element(By.CSS_SELECTOR, "p.txt").text
            date = item.find_element(By.CSS_SELECTOR, "p.date").text
            tag = item.find_element(By.CSS_SELECTOR, "span.tag").text
            
            # 검색어 필터 (원하는 키워드가 있으면 저장)
            keywords = ["해외", "여행", "항공", "달러", "직구"]
            if any(word in title for word in keywords):
                data.append({"카드사": tag, "이벤트명": title, "기간": date})
        except:
            continue

except Exception as e:
    print(f"에러 발생: {e}")

driver.quit()

# 3. 비상 대책: 만약 하나도 못 찾았다면 '수집 실패'라고라도 적어서 저장
# (이렇게 해야 EmptyDataError가 안 뜨고 화면에 실패했다는 게 보입니다)
if len(data) == 0:
    data.append({"카드사": "시스템", "이벤트명": "수집된 정보가 없습니다 (재시도 필요)", "기간": "-"})

# 4. 파일 저장
df = pd.DataFrame(data)
df.to_csv("benefits.csv", index=False)
print(f"저장 완료: {len(data)}개 항목")
