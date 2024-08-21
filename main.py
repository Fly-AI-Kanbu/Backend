from fastapi import FastAPI, Depends, HTTPException
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

# 사용자 생성 엔드포인트
@app.post("/users/", response_model=schemas.User)
def create_user_with_details(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # 사용자 생성
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

# 연속 출석 기록 조회 엔드포인트
@app.put("/consecutive_attendance/", response_model=schemas.ConsecutiveAttendance)
async def update_attendance(attendance_data: schemas.ConsecutiveAttendanceCreate, db: Session = Depends(get_db)):
    db_attendance = crud.update_consecutive_attendance(db, attendance_data)
    return db_attendance

# 모든 사용자 조회 엔드포인트
@app.get("/users/", response_model=list[schemas.User])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


# 특정 사용자 조회 엔드포인트
@app.get("/users/{user_id}", response_model=schemas.User)
def get_user_info(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.patch("/users/{user_id}", response_model=schemas.User)
def update_user_partial(user_id: int, updated_user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # 부분적으로 업데이트 적용
    for key, value in updated_user.model_dump().items():
        if value is not None:  # 새로운 값이 있는 필드만 업데이트
            setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user


@app.delete("/users/{user_id}", response_model=schemas.User)
def delete_user_api(user_id: int, db: Session = Depends(get_db)):
    # delete_user 함수를 호출하여 사용자 삭제
    db_user = crud.delete_user(db=db, user_id=user_id)

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    return db_user


###########################################################################################
@app.post("/users/{user_id}/korean-ability", response_model=schemas.KoreanAbility)
def create_korean_ability(user_id: int, korean_ability: schemas.KoreanAbilityCreate, db: Session = Depends(get_db)):
    # 사용자에 대한 기존 한국어 능력 정보가 있는지 확인
    db_existing_ability = crud.get_korean(db, user_id=user_id)
    if db_existing_ability:
        raise HTTPException(status_code=400, detail="Korean ability already exists for the user")

    # KoreanAbilityCreate 스키마에 user_id가 없을 수 있으므로 추가
    korean_ability.user_id = user_id

    # create_korean 함수를 사용하여 새 한국어 능력 정보를 생성
    return crud.create_korean(db=db, korean=korean_ability)


@app.patch("/users/{user_id}/korean-ability", response_model=schemas.KoreanAbility)
def update_korean_ability(user_id: int, updated_ability: schemas.KoreanAbilityBase, db: Session = Depends(get_db)):
    db_ability = crud.get_korean(db, user_id=user_id)
    if not db_ability:
        raise HTTPException(status_code=404, detail="Korean ability not found for the user")

    # crud.update_korean 함수를 호출하여 업데이트 처리
    return crud.update_korean(db=db, user_id=user_id, updated_korean=updated_ability)


@app.get("/users/{user_id}/korean-ability", response_model=schemas.KoreanAbility)
def get_korean_ability(user_id: int, db: Session = Depends(get_db)):
    db_ability = crud.get_korean(db, user_id=user_id)
    if not db_ability:
        raise HTTPException(status_code=404, detail="Korean ability not found for the user")

    # 예시로 유저 평균 및 누적 어휘력 등을 계산해 추가할 수 있습니다.
    # 예를 들어:
    # db_ability.total_vocabulary = calculate_total_vocabulary(db_ability)
    # db_ability.user_average = calculate_user_average(db)

    return db_ability
##########################################################################################
@app.get("/countries/{country_id}", response_model=schemas.Country)
def get_country_api(country_id: int, db: Session = Depends(get_db)):
    country = crud.get_country(db=db, country_id=country_id)
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")
    return country

@app.get("/countries/{country_id}/image", response_model=schemas.CountryImage)
async def get_country_image_api(country_id: int, db: Session = Depends(get_db)):
    country_image = crud.get_country_image(db=db, country_id=country_id)
    if not country_image:
        raise HTTPException(status_code=404, detail="CountryImage not found")
    return Response(content=country_image.country_img, media_type="image/" + country_image.img_type)


@app.get("/countries/", response_model=list[schemas.Country])
def get_countries_api(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    countries = db.query(models.Country).offset(skip).limit(limit).all()
    return countries



##########################################################################################
@app.post("/users/{user_id}/attendance", response_model=schemas.Attendance)
def create_attendance(user_id: int, attendance: schemas.AttendanceCreate, db: Session = Depends(get_db)):
    attendance.user_id = user_id
    return crud.create_attendance(db=db, attend=attendance)


@app.get("/users/{user_id}/attendance", response_model=List[schemas.Attendance])
def get_attendance_api(user_id: int, db: Session = Depends(get_db)):
    attendances = crud.get_attendance(db=db, user_id=user_id)
    if not attendances:
        raise HTTPException(status_code=404, detail="Attendance not found")
    return attendances

@app.get("/users/{user_id}/attendance/recent", response_model=List[schemas.Attendance])
def get_recent_attendance_api(user_id: int, db: Session = Depends(get_db)):
    attendances = crud.get_recent_attendances(db=db, user_id=user_id)
    if not attendances:
        raise HTTPException(status_code=404, detail="Attendance not found")
    return attendances

###########################################################################################
#단어관련

@app.get("/voca_pair", response_model=schemas.VocaPair)
def get_voca_for_main(db: Session = Depends(get_db)):
    voca_pair = crud.get_random_voca_pair(db)
    return voca_pair


# 퀴즈 API
@app.get("/quiz", response_model=dict)
def get_quiz(db: Session = Depends(get_db)):
    # 전체 단어 중에서 무작위로 4개 선택
    voca_pairs = db.query(models.VocaPair).order_by(func.random()).limit(4).all()

    if len(voca_pairs) < 4:
        raise HTTPException(status_code=404, detail="Not enough vocabulary pairs in the database.")

    # 하나의 단어는 한국어로 표시, 나머지 3개는 영어로 표시
    korean_word = random.choice(voca_pairs)
    english_words = [voca.Eng for voca in voca_pairs]

    # 퀴즈 응답 구조 정의
    quiz = {
        "voca_id": korean_word.voca_id,  # 한국어 단어의 voca_id
        "korean": korean_word.Korean,  # 한국어 단어
        "options": english_words,  # 영어 단어 선택지
        "answer": korean_word.Eng  # 정답 (한국어 단어에 해당하는 영어 번역)
    }

    return quiz


@app.post("/quiz/log", response_model=schemas.AnswerLog)
def create_or_ignore_answer_log_api(answer_log: schemas.AnswerLogCreate, db: Session = Depends(get_db)):
    # 로그를 생성하거나 이미 존재하는 로그를 반환
    log = crud.create_or_ignore_answer_log(db=db, answer_log=answer_log)

    # 생성된 로그 또는 기존 로그 반환
    return log


##############################################################################################################

@app.post("/chatrooms/")
def create_chat_room(user_id: int, subject_id: int, db: Session = Depends(get_db)):
    # User와 Subject 존재 여부 확인
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    subject = db.query(models.Subject).filter(models.Subject.subject_id == subject_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")

    # 채팅방 생성
    new_chat_room = models.Chat(
        chat_id=str(50),
        user_id=user_id,
        subject_id=subject_id,
        created_time=datetime.datetime.now()
    )

    db.add(new_chat_room)
    db.commit()
    db.refresh(new_chat_room)

    return new_chat_room

@app.post("/chatrooms/chatmessages/")
async def create_message(chat_msg : schemas.ChatMessageCreate, db : Session = Depends(get_db)):
    msg_id = str(uuid4())
    chatroom = db.query(models.Chat).filter(models.Chat.chat_id == chat_msg.chat_id).first()
    created_time = datetime.datetime.now()

    if not chatroom:
        raise HTTPException(status_code=404, detail="Chatroom not found")
    
    new_chat_msg = models.ChatMessage(
        msg_id=msg_id,
        chat_id=chat_msg.chat_id,
        content=chat_msg.content,
        created_time=created_time,
        is_human=chat_msg.is_human  # bool 값을 할당
    )


    db.add(new_chat_msg)
    db.commit()
    db.refresh(new_chat_msg)

    return new_chat_msg

@app.get("/chats/{user_id}", response_model = List[schemas.Chat])
async def get_chat(user_id: int, db : Session = Depends(get_db)):
    chats = crud.get_chat(db, user_id = user_id)
    return chats
