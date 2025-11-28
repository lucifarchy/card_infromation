import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

# 1. 브라우저 설정
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("--window-size=1920,1080")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")

driver = webdriver.Chrome(options=options)

print("카드고릴라 접속 중...")
driver.get("https://www.card-gorilla.com/event?cate=ING")

# 2. 로딩 대기 시간을 10초로 늘리고, 스크롤을 내립니다 (중요!)
time.sleep(5)
driver.execute_script("window.scrollTo(0, 500);")
time.sleep(2)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(5)

data = []

try:
    # 이벤트 리스트 찾기
    items = driver.find_elements(By.CSS_SELECTOR, "div.event_list ul li")
    print(f"발견된 항목 수: {len(items)}개")
    
    for item in items:
        try:
            # 제목과 기간, 카드사 정보 가져오기
            title = item.find_element(By.CSS_SELECTOR, "span.txt").text  # p.txt 에서 span.txt로 변경 시도
            if not title: # 만약 위 태그가 아니면 p.txt로 재시도
                 title = item.find_element(By.CSS_SELECTOR, "p.txt").text
                 
            date = item.find_element(By.CSS_SELECTOR, "p.date").text
            
            try:
                tag = item.find_element(By.CSS_SELECTOR, "span.tag").text
            except:
                tag = "전체"
            
            # [중요] 필터 제거! 일단 보이는 건 무조건 다 저장합니다.
            data.append({"카드사": tag, "이벤트명": title, "기간": date})
            
        except Exception as e:
            # 하나 읽다 에러나도 무시하고 다음 거 읽기
            continue

except Exception as e:
    print(f"전체 에러 발생: {e}")

driver.quit()

# 3. 결과 저장
if len(data) == 0:
    data.append({"카드사": "오류", "이벤트명": "여전히 로봇이 차단되었거나 태그가 바뀌었습니다.", "기간": "-"})

df = pd.DataFrame(data)
df.to_csv("benefits.csv", index=False)
print(f"최종 저장 완료: {len(data)}개")
