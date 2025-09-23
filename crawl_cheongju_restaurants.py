from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

# ───────────────────── 크롬 옵션 설정 ─────────────────────
options = Options()
options.add_argument("--start-maximized")
service = Service()
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 10)

# ───────────────────── 청주시 동/면 리스트 ─────────────────────
cheongju_regions = [
    # 상당구
    "금천동", "용담동", "용암동", "영운동", "문화동", "산성동", "탑동", "용정동", "문의면", "낭성면", "미원면", "가덕면", "남일면",
    # 서원구
    "모충동", "사직동", "사창동", "산남동", "성화동", "수곡동", "장성동", "죽림동", "남이면", "현도면",
    # 흥덕구
    "가경동", "강서동", "복대동", "비하동", "봉명동", "송정동", "운천동", "장암동", "오송읍", "옥산면", "강내면", "남촌동",
    # 청원구
    "내덕동", "율량동", "오창읍", "북이면", "외북동", "정북동"
]

all_data = []

def crawl_region(region):
    try:
        keyword = f"청주 {region} 식당"
        print(f"\n🔍 '{keyword}' 검색 시작")
        driver.get("https://map.kakao.com/")

        search_box = wait.until(EC.presence_of_element_located((By.ID, "search.keyword.query")))
        search_box.clear()
        search_box.send_keys(keyword)
        time.sleep(1)

        # dimmedLayer 제거 시도
        try:
            dimmed = driver.find_element(By.ID, "dimmedLayer")
            if dimmed.is_displayed():
                driver.execute_script("document.getElementById('dimmedLayer').remove()")
                time.sleep(0.5)
        except:
            pass

        submit_btn = driver.find_element(By.ID, "search.keyword.submit")
        submit_btn.click()

        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".placelist")))

        page = 1
        while True:
            time.sleep(1.5)
            items = driver.find_elements(By.CSS_SELECTOR, ".placelist .PlaceItem")
            print(f"📄 {region} - {page}페이지: {len(items)}개")

            for item in items:
                try:
                    name = item.find_element(By.CSS_SELECTOR, "a.link_name").text.strip()
                    category = item.find_element(By.CSS_SELECTOR, "span.subcategory.clickable").text.strip()
                    address = item.find_element(By.CSS_SELECTOR, "p[data-id='address']").text.strip()
                    print(f"수집: {name} | {category} | {address}")
                    all_data.append([name, address, category, region])
                except Exception as e:
                    print(f"아이템 수집 실패: {e}")
                    continue

            try:
                next_btn = driver.find_element(By.CSS_SELECTOR, "a.btn_next")
                if "off" in next_btn.get_attribute("class"):
                    break
                next_btn.click()
                page += 1
            except:
                break

        print(f"✅ '{region}' 완료 (총 {page}페이지)")
    except Exception as e:
        print(f"❌ '{region}' 에러 발생: {e}")

# ───────────────────── 메인 크롤링 실행 ─────────────────────
for region in cheongju_regions:
    crawl_region(region)

print(f"\n총 수집 데이터 수: {len(all_data)}")

# ───────────────────── 중복 제거 ─────────────────────
unique_data = []
seen = set()
for row in all_data:
    key = (row[0], row[1])  # 이름 + 주소 기준 중복 제거
    if key not in seen:
        seen.add(key)
        unique_data.append(row)

print(f"중복 제거 후 데이터 수: {len(unique_data)}")

# ───────────────────── CSV 저장 ─────────────────────
with open("cheongju_region_restaurants.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["name", "address", "category", "region"])
    writer.writerows(unique_data)

print(f"\n💾 완료: 총 {len(unique_data)}개 식당 저장됨 (cheongju_region_restaurants.csv)")

driver.quit