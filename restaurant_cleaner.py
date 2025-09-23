import pandas as pd

df = pd.read_csv("latlng_restaurants.csv")

category_map = {
    "한식": ["한식", "갈비", "해장국", "삼계탕", "국밥", "찌개", "불고기", "오리", "닭요리", "장어", "삼겹살", "순대", "곱창", "막창", "한정식", "한식뷔페"],
    "중식": ["중식", "중국요리", "샤브샤브", "짜장", "짬뽕", "탕수육", "마파두부"],
    "양식": ["양식", "피자", "스테이크", "파스타", "이탈리안", "제과", "베이커리", "디저트카페", "커피전문점", "패밀리레스토랑", "뷔페", "샌드위치"],
    "일식": ["일식", "초밥", "롤", "우동", "돈까스", "일본식", "회"],
    "패스트푸드": ["패스트푸드", "치킨", "햄버거", "버거"],
    "분식": ["분식", "떡볶이", "순대", "튀김", "김밥", "만두", "오뎅", "호떡"]
}

def map_category(cat):
    cat = str(cat)
    for main_cat, keywords in category_map.items():
        if any(keyword in cat for keyword in keywords):
            return main_cat
    return "기타"

df["category"] = df["category"].apply(map_category)

print(df["category"].value_counts())

df.to_csv("categorized_restaurants.csv", index=False, encoding="utf-8-sig")
