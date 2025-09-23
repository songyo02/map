import pandas as pd

# CSV 파일 불러오기
df = pd.read_csv("categorized_restaurants.csv")

# '기타' 카테고리만 따로 필터링
df_etc = df[df['category'] == '기타']

# 기타 카테고리 데이터 개수 출력
print(f"기타 카테고리 개수: {len(df_etc)}")

# 기타 카테고리 데이터 확인 (원하면)
print(df_etc)

# 파일로 저장하고 싶으면
df_etc.to_csv("etc_category_restaurants.csv", index=False, encoding="utf-8-sig")
