from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import CountryImage
import os

# 데이터베이스 연결 설정
DATABASE_URL = "mysql+pymysql://root:kanbu@localhost:3307/kanbu"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# 이미지 파일 경로
image_path = r"C:\Users\SKT019\Desktop\US.svg"

# 이미지 파일 읽기
with open(image_path, 'rb') as file:
    image_data = file.read()

# 이미지 파일 타입 추출 (확장자)
img_type = os.path.splitext(image_path)[-1].replace('.', '')

# CountryImage 모델에 데이터 삽입
country_images = [
    CountryImage(country_id=1, country_img=image_data, img_type=img_type)
]

# 데이터베이스에 데이터 저장
session.add_all(country_images)
session.commit()
session.close()

print("이미지가 성공적으로 데이터베이스에 추가되었습니다.")
