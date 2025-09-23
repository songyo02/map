import pandas as pd

df = pd.read_csv("categorized_restaurants.csv")  # 기존 csv 파일 불러오기

# 카테고리별 이름에 포함된 키워드 사전
name_category_map = {
    "한식": ["한식", "칼국수", "삼계탕", "국밥", "불고기", "닭", "순대", "곱창", "막창", "한정식", "갈비", "감자탕", "두부", "전주", "백반"],
    "중식": ["중식", "짜장", "짬뽕", "탕수육", "마파두부", "양장피", "마라", "샤브샤브"],
    "양식": ["피자", "스테이크", "파스타", "이탈리안", "베이커리", "디저트", "카페", "커피", "뷔페", "샌드위치", "케이크"],
    "일식": ["초밥", "롤", "우동", "돈까스", "일식", "회", "일본"],
    "패스트푸드": ["치킨", "햄버거", "버거", "도넛", "도시락"],
    "분식": ["떡볶이", "김밥", "튀김", "만두", "오뎅", "분식", "순대", "호떡"]
}

def categorize_by_name(name):
    name = str(name)
    for cat, keywords in name_category_map.items():
        for kw in keywords:
            if kw in name:
                return cat
    return "기타"

# name 기준으로 category 새로 지정
df["category"] = df["name"].apply(categorize_by_name)

print(df["category"].value_counts())

# 변경된 데이터 저장
df.to_csv("re_categorized_restaurants.csv", index=False, encoding="utf-8-sig")
