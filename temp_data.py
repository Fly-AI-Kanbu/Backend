from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, date
from models import User, Country, CountryImage, Subscribe, KoreanAbility, VocaPair, ChatMessage, Chat, Subject, Attendance, AccessToken, SubscribeLog, AnswerLog, DialogueVideo, Dialogue, DialogueScript   # Adjust this import according to your file structure
import config

user = config.mysql_user
password = config.mysql_password
ip = config.mysql_ip
db_name = config.mysql_db
# MySQL 연결 설정
DATABASE_URL = f"mysql+pymysql://{user}:{password}@{ip}/{db_name}"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# # 이미지 파일 경로 (raw string으로 처리)
# image_path = r'C:\Users\TH\Downloads\외교부_국가(지역)별 국기 이미지_20230210\US.gif'

# # 이미지 파일 읽기
# with open(image_path, 'rb') as file:
#     image_data = file.read()

# # 샘플 데이터 삽입
# # Country 데이터
# country_images = [
#     CountryImage(country_id=2, country_img = image_data, img_type = image_path.split('.')[-1])
# ]
# session.add_all(country_images)
# session.commit()

# video = Dialogue(dialogue_id = 3, title = "재혁 기일")
# session.add(video)
# session.commit()

# video_path = r'C:\Users\TH\OneDrive\Documents\카카오톡 받은 파일\KakaoTalk_20240821_165010869.mp4'

# with open(video_path, 'rb') as file:
#     video_data = file.read()

# video_data = [
#     DialogueVideo(video_id = 'abc', dialogue_id = 3, sequence = 1, video_data = video_data, video_type = video_path.split('.')[-1])
# ]
# session.add_all(video_data)
# session.commit()

script = DialogueScript(script_id = 'aaa', dialogue_id = 3, sequence = 1, script_ai = "안녕하세요", script_user = "네 반가워요")
session.add(script)
session.commit()