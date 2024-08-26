from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, date
from models import User, Country, Subscribe, KoreanAbility, VocaPair, ChatMessage, Chat, Subject, Attendance, AccessToken, SubscribeLog, AnswerLog, CountryImage, Base
import pandas as pd

# MySQL 연결 설정
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:1234@localhost:3306/kanbu"

# SQLAlchemy 엔진 생성
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True  # 연결 확인을 위한 옵션
)
Session = sessionmaker(bind=engine)
session = Session()

# 테이블 생성 (없으면)
Base.metadata.create_all(engine)

# 1. 엑셀 파일 읽기
df = pd.read_excel("교육부_3천단어_수정분.xls", sheet_name="Sheet1")

# 2. 엑셀 데이터를 데이터베이스에 삽입
for index, row in df.iterrows():
    voca_pair = VocaPair(Eng=row['단어'], Korean=row['뜻'])
    session.add(voca_pair)

# 3. 변경사항 커밋
session.commit()

# 샘플 데이터 삽입
# Country 데이터 삽입
country1 = Country(name='South Korea', nicename='Korea', iso='KR', iso3='KOR', numcode=410, phonecode=82)
country2 = Country(name='United States', nicename='USA', iso='US', iso3='USA', numcode=840, phonecode=1)
session.add_all([country1, country2])
session.commit()

# 이미지 파일 경로
image_path = r"C:\Users\SKT019\Desktop\US.svg"

# 이미지 파일을 읽어 바이너리 데이터로 저장
with open(image_path, 'rb') as file:
    image_data = file.read()

# CountryImage 데이터 삽입
country_image = CountryImage(country_id=country2.country_id, country_img=image_data, img_type='svg')
session.add(country_image)
session.commit()

# User 데이터
user1 = User(name='John', pwd='password123', first_name='Ed', last_name='Sheeran', age=30, email='john.doe@example.com', phone='010-1234-5678', address='Seoul, United States', country_id=country2.country_id)
user2 = User(name='Jane', pwd='password456', first_name='Jane', last_name='Smith', age=28, email='jane.smith@example.com', phone='010-9876-5432', address='Busan, South Korea', country_id=country1.country_id)
session.add_all([user1, user2])
session.commit()

# KoreanAbility 데이터
korean_ability1 = KoreanAbility(user_id=user1.user_id, complexity=5, toxicity=1, fluency=8, vocabulary=7, similarity=9)
korean_ability2 = KoreanAbility(user_id=user2.user_id, complexity=6, toxicity=2, fluency=7, vocabulary=8, similarity=8)
session.add_all([korean_ability1, korean_ability2])
session.commit()

# Subject 데이터
subject1 = Subject(subject_name='Korean Language', grade='A')
subject2 = Subject(subject_name='Mathematics', grade='B')
session.add_all([subject1, subject2])
session.commit()

# Chat 데이터
chat1 = Chat(chat_id='chat123', user_id=user1.user_id, subject_id=subject1.subject_id, created_time=datetime.now())
chat2 = Chat(chat_id='chat456', user_id=user2.user_id, subject_id=subject2.subject_id, created_time=datetime.now())
session.add_all([chat1, chat2])
session.commit()

# ChatMessage 데이터
chat_message1 = ChatMessage(msg_id='msg123', chat_id=chat1.chat_id, content='How are you?', created_time=datetime.now(), is_human=True)
chat_message2 = ChatMessage(msg_id='msg456', chat_id=chat2.chat_id, content='I am fine, thank you!', created_time=datetime.now(), is_human=True)
session.add_all([chat_message1, chat_message2])
session.commit()

# Attendance 데이터
attendance1 = Attendance(user_id=user1.user_id, attendance_date=date.today())
attendance2 = Attendance(user_id=user2.user_id, attendance_date=date.today())
session.add_all([attendance1, attendance2])
session.commit()

# Subscribe 데이터
subscribe1 = Subscribe(sub_id='sub123', sub_name='Basic Plan', price='10000')
subscribe2 = Subscribe(sub_id='sub456', sub_name='Premium Plan', price='20000')
session.add_all([subscribe1, subscribe2])
session.commit()

# AccessToken 데이터
access_token1 = AccessToken(key=1, user_id=user1.user_id, access_token='token123', expiration_date=datetime.now())
access_token2 = AccessToken(key=2, user_id=user2.user_id, access_token='token456', expiration_date=datetime.now())
session.add_all([access_token1, access_token2])
session.commit()

# SubscribeLog 데이터
subscribe_log1 = SubscribeLog(user_sub_log='log123', user_id=user1.user_id, sub_id=subscribe1.sub_id, pay_date=datetime.now(), payoff_date=datetime.now(), status=True)
subscribe_log2 = SubscribeLog(user_sub_log='log456', user_id=user2.user_id, sub_id=subscribe2.sub_id, pay_date=datetime.now(), payoff_date=datetime.now(), status=False)
session.add_all([subscribe_log1, subscribe_log2])
session.commit()

print("샘플 데이터 삽입 완료.")
