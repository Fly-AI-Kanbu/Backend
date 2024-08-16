from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, date
from models import User, Country, Subscribe, KoreanAbility, VocaPair, ChatMessage, Chat, Subject, Attendance, AccessToken, SubscribeLog  # Adjust this import according to your file structure

# 데이터베이스 연결 설정
DATABASE_URL = "mysql+pymysql://root:jth306241!@localhost/kanbu"  # 사용자의 MySQL 설정에 맞게 수정

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# 샘플 데이터 삽입
# Country 데이터
country1 = Country(name='South Korea', nicename='Korea', iso='KR', iso3='KOR', numcode=410, phonecode=82)
country2 = Country(name='United States', nicename='USA', iso='US', iso3='USA', numcode=840, phonecode=1)
session.add_all([country1, country2])
session.commit()W

# User 데이터
user1 = User(name='John', pwd='password123', first_name='John', last_name='Doe', age=30, nickname='Johnny', email='john.doe@example.com', phone='010-1234-5678', address='Seoul, South Korea', country_id=country1.country_id)
user2 = User(name='Jane', pwd='password456', first_name='Jane', last_name='Smith', age=28, nickname='Janie', email='jane.smith@example.com', phone='010-9876-5432', address='Busan, South Korea', country_id=country1.country_id)
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

# VocaPair 데이터
voca_pair1 = VocaPair(Korean="안녕하세요", Eng="hello")
voca_pair2 = VocaPair(Korean='사랑', Eng='love')
voca_pair3 = VocaPair(Korean='노동', Eng='work')
voca_pair4 = VocaPair(Korean='벌레', Eng='bug')
voca_pair5 = VocaPair(Korean='책', Eng='book')
voca_pair6 = VocaPair(Korean='컴퓨터', Eng='컴퓨터가 영어임')

session.add_all([voca_pair3, voca_pair4, voca_pair5, voca_pair6])
session.commit()

# ChatMessage 데이터
chat_message1 = ChatMessage(msg_id='msg123', chat_id=chat1.chat_id, content='How are you?', created_time=datetime.now(), is_human=True)
chat_message2 = ChatMessage(msg_id='msg456', chat_id=chat2.chat_id, content='I am fine, thank you!', created_time=datetime.now(), is_human=True)
session.add_all([chat_message1, chat_message2])
session.commit()

# LogQuiz 데이터
log_quiz1 = LogQuiz(log_id='log123', user_id=user1.user_id, word_id=voca_pair1.voca_id, is_answer=True, date=datetime.now())
log_quiz2 = LogQuiz(log_id='log456', user_id=user2.user_id, word_id=voca_pair2.voca_id, is_answer=False, date=datetime.now())
session.add_all([log_quiz1, log_quiz2])
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
access_token1 = AccessToken(Key=1, user_id=user1.user_id, access_token='token123', expiration_date=datetime.now())
access_token2 = AccessToken(Key=2, user_id=user2.user_id, access_token='token456', expiration_date=datetime.now())
session.add_all([access_token1, access_token2])
session.commit()

# SubscribeLog 데이터
subscribe_log1 = SubscribeLog(user_sub_log='log123', user_id=user1.user_id, sub_id=subscribe1.sub_id, pay_date=datetime.now(), payoff_date=datetime.now(), status=True)
subscribe_log2 = SubscribeLog(user_sub_log='log456', user_id=user2.user_id, sub_id=subscribe2.sub_id, pay_date=datetime.now(), payoff_date=datetime.now(), status=False)
session.add_all([subscribe_log1, subscribe_log2])
session.commit()

print("샘플 데이터 삽입 완료.")
