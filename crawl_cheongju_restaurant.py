from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

options = Options()
options.add_argument("--start-maximized")
service = Service()
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 10)

# 업종 리스트
categories = ["한식", "중식", "일식", "패스트푸드", "양식", "분식"]

all_data = []

def crawl_category(category):
    try:
        keyword = f"청주 {category} 식당"
        print(f"\n🔍 '{keyword}' 검색 시작")
        driver.get("https://map.kakao.com/")

        search_box = wait.until(EC.presence_of_element_located((By.ID, "search.keyword.query")))
        search_box.clear()
        search_box.send_keys(keyword)
        time.sleep(1)

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
            print(f"📄 {category} - {page}페이지: {len(items)}개")

            for item in items:
                try:
                    name = item.find_element(By.CSS_SELECTOR, "a.link_name").text.strip()
                    category_text = item.find_element(By.CSS_SELECTOR, "span.subcategory.clickable").text.strip()
                    address = item.find_element(By.CSS_SELECTOR, "p[data-id='address']").text.strip()
                    print(f"수집: {name} | {category_text} | {address}")
                    all_data.append([name, address, category_text, category])
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

        print(f"✅ '{category}' 완료 (총 {page}페이지)")
    except Exception as e:
        print(f"❌ '{category}' 에러 발생: {e}")

for category in categories:
    crawl_category(category)

print(f"\n총 수집 데이터 수: {len(all_data)}")

# 중복 제거
unique_data = []
seen = set()
for row in all_data:
    key = (row[0], row[1])  # 이름+주소 기준 중복 제거
    if key not in seen:
        seen.add(key)
        unique_data.append(row)

print(f"중복 제거 후 데이터 수: {len(unique_data)}")

with open("cheongju_category_restaurants.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["name", "address", "category_text", "searched_category"])
    writer.writerows(unique_data)

print(f"\n💾 완료: 총 {len(unique_data)}개 식당 저장됨 (cheongju_category_restaurants.csv)")

driver.quit()
