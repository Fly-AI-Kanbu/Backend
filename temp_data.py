from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, date
from models import User, Country, CountryImage, Subscribe, KoreanAbility, VocaPair, ChatMessage, Chat, Subject, Attendance, AccessToken, SubscribeLog, AnswerLog   # Adjust this import according to your file structure

# 데이터베이스 연결 설정
DATABASE_URL = "mysql+pymysql://root:jth306241!@localhost/kanbu"  # 사용자의 MySQL 설정에 맞게 수정

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# 이미지 파일 경로 (raw string으로 처리)
image_path = r'C:\Users\TH\Downloads\외교부_국가(지역)별 국기 이미지_20230210\US.gif'

# 이미지 파일 읽기
with open(image_path, 'rb') as file:
    image_data = file.read()

# 샘플 데이터 삽입
# Country 데이터
country_images = [
    CountryImage(country_id=2, country_img = image_data, img_type = image_path[-3:])
]
session.add_all(country_images)
session.commit()
