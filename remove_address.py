import pandas as pd

# 원본 CSV 파일 경로
input_file = 'restaurant_with_latlng.csv'
# 수정된 CSV 파일 저장 경로
output_file = 'heong_category_restaurants.csv'

# CSV 파일 읽기
df = pd.read_csv(input_file)

# address 컬럼 삭제
df = df.drop(columns=['address'])
df = df.drop(columns=['region'])

# 수정된 데이터 CSV로 저장 (index 없이)
df.to_csv(output_file, index=False)

print(f"'region' 컬럼 제거 후 저장 완료: {output_file}")
