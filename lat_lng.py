import pandas as pd
import requests
from tqdm import tqdm
import time

# 여기에 본인 구글 API 키 넣기
API_KEY = "AIzaSyBCyU2qprBvlv8MriekBO86iTzNb8IIpuE"

# 입력 CSV 파일명 (주소가 있는 파일)
INPUT_CSV = "cheongju_category_restaurants.csv"

# 출력 CSV 파일명 (위경도 포함 결과 저장)
OUTPUT_CSV = "restaurant_with_latlng.csv"

def get_lat_lng(address):
    """주소를 받아서 구글 지오코딩 API 호출 후 위도, 경도 반환"""
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": address,
        "key": API_KEY,
        "language": "ko"  # 한국어 결과 요청 (선택사항)
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        result = response.json()

        if result["status"] == "OK":
            location = result["results"][0]["geometry"]["location"]
            return location["lat"], location["lng"]
        else:
            print(f"API 오류: {result['status']} - 주소: {address}")
            return None, None

    except Exception as e:
        print(f"예외 발생: {e} - 주소: {address}")
        return None, None

def main():
    # CSV 파일 읽기 (인코딩은 필요시 맞춰서 조정)
    df = pd.read_csv(INPUT_CSV, encoding="utf-8-sig")
    print(df.columns)    # 컬럼명 확인
    print(df.head())     # 데이터 샘플 확인
    print(len(df))       # 데이터 행 개수 확인

    # 위도, 경도 컬럼 추가
    lat_list = []
    lng_list = []

    # tqdm으로 진행 상황 시각화
    for addr in tqdm(df["address"]):
        lat, lng = get_lat_lng(addr)
        lat_list.append(lat)
        lng_list.append(lng)
        time.sleep(0.1)  # API 요청 제한에 걸리지 않도록 약간 딜레이 (필요시 조정)

    df["lat"] = lat_list
    df["lng"] = lng_list

    # 결과 CSV 저장
    df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")
    print(f"✅ 변환 완료: {OUTPUT_CSV}")

if __name__ == "__main__":
    main()
