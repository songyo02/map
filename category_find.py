import pandas as pd

df = pd.read_csv("latlng_restaurants.csv")

# value_counts 결과 전체 출력하려면 아래 옵션 쓰기
pd.set_option('display.max_rows', None)

print(df['category'].value_counts())
