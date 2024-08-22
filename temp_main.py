from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import Response
from sqlalchemy.orm import Session
import crud, schemas
import models
from typing import List
from sqlalchemy import func
import random
import datetime
from database import SessionLocal, engine
from uuid import uuid4


# 데이터베이스 테이블 생성
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

 # 사용자 생성
@app.post("/users/", response_model=schemas.User)
def create_user_account(user: schemas.UserCreate, db: Session = Depends(get_db)):
   
    db_user = crud.create_user(db=db, user=user)

    if not db_user:
        raise HTTPException(status_code=400, detail="User could not be created")

    # Korean Ability 생성 (기본값이 이미 CRUD에 설정되어 있음)
    korean_ability = schemas.KoreanAbilityCreate(user_id=db_user.user_id)
    crud.create_korean(db=db, korean=korean_ability)

    # Attendance 생성 (기본값이 이미 CRUD에 설정되어 있음)
    attendance = schemas.AttendanceCreate(user_id=db_user.user_id)
    crud.create_attendance(db=db, attend=attendance)

    return db_user

############# 메인화면 ###############
# 유저 정보 불러오기
@app.get("/user/{user_id}/get-user-info")
def get_userinfomation_from_db(user_id: int, db: Session = Depends(get_db)):
    user_id = 1 # 구현 확인을 위한 임시 data, 추후 업데이트 예정
    user = crud.get_user(user_id = user_id, db = db)
    if not user:
        raise HTTPException(status_code=404, detail = "User not found")
    country = crud.get_country(country_id = user.country_id, db = db)
    country_name = country.name # 국가 이름 반환

    return {"user_id" : user.user_id, "user_name" : user.first_name + user.last_name, "country" : country_name}

# 유저 국가 이미지 불러오기
@app.get("/user/{user_id}/get-country-image", response_model = schemas.CountryImage)
def get_countryimage_from_db(user_id: int, db: Session = Depends(get_db)):
    user_id = 1 # 구현 확인을 위한 임시 data, 추후 업데이트 예정
    user = crud.get_user(user_id = user_id, db = db) # 유저 조회
    if not user:
        raise HTTPException(status_code=404, detail = "User not found")
    country_image = crud.get_country_image(db = db, country_id = user.country_id)
    if not country_image:
        raise HTTPException(status_code=404, detail="CountryImage not found")
    return Response(content=country_image.country_img, media_type="image/" + country_image.img_type)

# 출석 정보 생성 및 업데이트
# 출석 정보 log 생성
@app.post("/user/{user_id}/create-attendance-log")
def create_attendacne_log(user_id: int, db: Session = Depends(get_db)):
    user_id = 1 # 구현 확인을 위한 임시 data, 추후 업데이트 예정
    user_attendance_log = crud.create_attendance(db = db, user_id = user_id) # 유저 접속 로그 생성
    return user_attendance_log

# 주간 출석 db 조회
@app.get("/user/{user_id}/get-attendance-log")
def get_attendacne_log(user_id: int, db: Session = Depends(get_db)):
    user_id = 1 # 구현 확인을 위한 임시 data, 추후 업데이트 예정
    user_attendance_of_the_week = crud.get_attendances_of_the_week(db = db, user_id = user_id) # 유저 접속 로그 생성
    return user_attendance_of_the_week

# 연속 출석 db 업데이트
@app.put("/user/{user_id}/update-consecutive-attendance")
def update_consecutive_attandance(user_id : int, db: Session = Depends(get_db)):
    user_id = 1 # 구현 확인을 위한 임시 data, 추후 업데이트 예정
    updated_consecutive_attendance = crud.update_consecutive_attendance(db = db, user_id = user_id) # 유저 연속 접속 정보 업데이트
    return updated_consecutive_attendance

# 연속 출석 db 조회
@app.get("/user/{user_id}/get-consecutive-attendance")
def get_consecutive_attandance(user_id : int, db: Session = Depends(get_db)):
    user_id = 1 # 구현 확인을 위한 임시 data, 추후 업데이트 예정
    consecutive_attendance = crud.get_consecutive_attendance(db = db, user_id = user_id) # 유저 연속 접속 정보 업데이트
    return consecutive_attendance.consecutive_days

#-----------------구현필요------------------------
# # 오늘의 단어 불러오기
# @app.get("/get-vocapair")
# def get_vocafair_from_db(db: Session = Depends(get_db)):


############# 채팅화면 ###############
# 채팅방 생성
@app.post("/user/{user_id}/create-chat")
def create_chat(user_id : int, db: Session = Depends(get_db)):
    user_id = 1 # 구현 확인을 위한 임시 data, 추후 업데이트 예정
    subject_id = crud.get_random_subject(db = db)
    new_chat = crud.create_chat(db = db, user_id = user_id, subject_id = subject_id)
    ## ai서버에 주제 전달 및 첫 문장 요청 or db
    # request = Reuqest(127.0.0.1/8001/)
    # 받아온 답변을 chat_message db에 저장
    return new_chat

# 채팅 메시지 입력, DB랑 AI 모델로 전송
@app.post("/user/{chat_id}/create_chat_message")
def create_chat_message(user_id: int, db: Session = Depends(get_db)):
    chat_id = 1 # 구현 확인을 위한 임시 data, 추후 업데이트 예정
    new_chat_message = crud.create_chatMessage(db = db)
    # request 

# 채팅방 list 조회
@app.get("/user/{user_id}/get-chat-list")
def get_chat_list(user_id: int, db: Session = Depends(get_db)):
    user_id = 1 # 구현 확인을 위한 임시 data, 추후 업데이트 예정
    chat_list_with_titles = crud.get_chats_with_titles(db = db, user_id = user_id) # user id가 1인 chat들의 title 조회
    return [{"chat_id": chat.chat_id, "subject_name": chat.subject_name} for chat in chat_list_with_titles]

# 채팅방 선택 및 채팅 메시지 조회
@app.get("/chat/{chat_id}/get-chat-messages")
def get_chat_messages(chat_id: str, db: Session = Depends(get_db)):
    chat_id = "chat123" # 구현 확인을 위한 임시 data, 추후 업데이트 예정
    chat_messages = crud.get_chatLog(db = db, chat_id = chat_id)
    return [{"is_human" : chat_message.is_human, "content" : chat_message.content} for chat_message in chat_messages]

    