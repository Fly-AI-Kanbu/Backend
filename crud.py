from sqlalchemy.orm import Session
# from passlib.context import CryptContext  # 비밀번호 해시를 위한 패키지
from typing import List
import random
import models, schemas
from datetime import timedelta
from sqlalchemy import func, and_
import uuid
from fastapi import HTTPException
from sqlalchemy import desc,asc
# 비밀번호 해시 설정
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = "sss"  # pwd_context.hash(user.password)  # 비밀번호 해시 생성
    db_user = models.User(
        user_id=user.user_id,
        pwd=hashed_password,  # 실제 비밀번호 해시를 저장
        first_name=user.first_name,
        last_name=user.last_name,
        age=user.age,
        name=user.name,
        email=user.email,
        phone=user.phone,
        address=user.address,
        country_id=user.country_id,
    )
    db.add(db_user)
    db.commit()
    print('adsfadfadf')
    db.refresh(db_user)
    print('너야?')
    return db_user


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.user_id == user_id).first()


def get_user_by_account_id(db: Session, name: str): # 유저 중복 확인
    return db.query(models.User).filter(models.User.name == name).first()


def get_users(db: Session, skip: int = 0, limit: int = None):
    query = db.query(models.User).offset(skip)

    if limit is not None:
        query = query.limit(limit)
    return query.all()


def update_user(db: Session, user_id: int, updated_user: schemas.UserCreate):
    db_user = db.query(models.User).filter(models.User.user_id == user_id).first()
    for key, value in updated_user.model_dump().items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user


##########################################################################################
#한국어 능력


def create_korean(db: Session, korean: schemas.KoreanAbilityCreate):
    # 스키마에 값이 제공되지 않았을 경우 기본값을 설정
    db_korean = models.KoreanAbility(
        user_id=korean.user_id,
        complexity=korean.complexity,
        toxicity=korean.toxicity,
        fluency=korean.fluency,
        vocabulary=korean.vocabulary,
        accuracy=korean.accuracy,
        context_score=korean.context_score
    )
    db.add(db_korean)
    db.commit()
    db.refresh(db_korean)
    return db_korean



def get_korean(db: Session, user_id: int):
    koability = db.query(models.KoreanAbility).filter(models.KoreanAbility.user_id == user_id).first()
    korean ={
        'complexity':koability.complexity,
        'toxicity':koability.toxicity,
        'fluency':koability.fluency,
        'vocabulary':koability.vocabulary,
        'accuracy':koability.accuracy,
        'context_score' : koability.context_score
        }
    return korean

def update_korean(db: Session, user_id: int, updated_korean: schemas.KoreanAbilityBase):
    korean = db.query(models.KoreanAbility).filter(models.KoreanAbility.user_id == user_id).first()
    for key, value in updated_korean.model_dump().items():
        setattr(korean, key, value)
    db.commit()
    db.refresh(korean)
    return korean


def delete_korean(db: Session, user_id: int):
    db_user = db.query(models.KoreanAbility).filter(models.KoreanAbility.user_id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user



##########################################################################################\
#국가 정보
def create_country(db: Session, country: schemas.CountryCreate):
    db_country = models.Country(
        country_id=country.country_id,
        iso=country.iso,
        name=country.name,
        nicename=country.nicename,
        iso3=country.iso3,
        numcode=country.numcode,
        phonecode=country.phonecode
    )
    db.add(db_country)
    db.commit()
    db.refresh(db_country)
    return db_country


def get_country(db: Session, country_id: int):
    return db.query(models.Country).filter(models.Country.country_id == country_id).first()

def get_country_image(db: Session, country_id: int):
    return db.query(models.CountryImage).filter(models.CountryImage.country_id == country_id).first()


def update_country(db: Session, country_id: int, updated_country: schemas.CountryBase):
    db_country = db.query(models.Country).filter(models.Country.country_id == country_id).first()
    if not db_country:
        return None
    for key, value in updated_country.model_dump().items():
        setattr(db_country, key, value)
    db.commit()
    db.refresh(db_country)
    return db_country


def delete_country(db: Session, country_id: int):
    db_country = db.query(models.Country).filter(models.Country.country_id == country_id).first()
    if db_country:
        db.delete(db_country)
        db.commit()
    return db_country




###############################################################################################################
#출석 정보


from datetime import datetime

def create_attendance(db: Session, user_id: int):
    # attendance_date가 제공되지 않았을 경우 현재 시간을 기본값으로 설정
    attendance_log = models.Attendance(
        user_id=user_id,
        attendance_date=datetime.now().date()
    )
    db.add(attendance_log)
    db.commit()
    db.refresh(attendance_log)
    return attendance_log


def get_attendance(db: Session, user_id: int):
    attendances = db.query(models.Attendance).filter(models.Attendance.user_id == user_id).all()
    return [schemas.Attendance.from_orm(attendance) for attendance in attendances]


from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_

def get_attendances_of_the_week(db: Session, user_id: int):
    attendances_of_the_week = {  # 주간 출석 db 조회
        0: False,  # "Mon"
        1: False,  # "Tue"
        2: False,  # "Wed"
        3: False,  # "Thu"
        4: False,  # "Fri"
        5: False,  # "Sat"
        6: False   # "Sun"
    } 

    today = datetime.now().date()

    for i in range(today.weekday() + 1):
        check_date = today - timedelta(days=i)  # 오타 수정
        data_exists = db.query(models.Attendance).filter(
            and_(
                models.Attendance.attendance_date == check_date,
                models.Attendance.user_id == user_id
            )
        ).first() is not None

        if data_exists:
            attendances_of_the_week[check_date.weekday()] = True  # check_date.weekday()

    return attendances_of_the_week



def update_attendance(db: Session, user_id: int, updated_attend: schemas.AttendanceCreate):
    attend = db.query(models.Attendance).filter(models.Attendance.user_id == user_id).first()
    for key, value in updated_attend.model_dump().items():
        setattr(attend, key, value)
    db.commit()
    db.refresh(attend)
    return attend


def delete_attendance(db: Session, user_id: int):
    db_attend = db.query(models.Attendance).filter(models.Attendance.user_id == user_id).first()
    if db_attend:
        db.delete(db_attend)
        db.commit()
    return db_attend

# 누적 출석 업데이트
def get_consecutive_attendance(db: Session, user_id: int):
    return db.query(models.ConsecutiveAttendance).filter(models.ConsecutiveAttendance.user_id == user_id).first()

from datetime import datetime, timedelta

def update_consecutive_attendance(db: Session, user_id: int):
    user_consecutive_attendance = get_consecutive_attendance(db, user_id)
    today = datetime.now().date()
    
    if user_consecutive_attendance:
        # 연속 출석 여부를 판단
        if user_consecutive_attendance.last_attendance_date == (today - timedelta(days=1)):
            user_consecutive_attendance.consecutive_days += 1
        elif user_consecutive_attendance.last_attendance_date == today:
            pass
        else:
            user_consecutive_attendance.consecutive_days = 1
        
        # 마지막 출석 날짜 업데이트
        user_consecutive_attendance.last_attendance_date = today
        db.commit()
        db.refresh(user_consecutive_attendance)
        db_attendance = user_consecutive_attendance
    else:
        # 새로운 출석 기록 생성
        new_attendance = models.ConsecutiveAttendance(
            user_id=user_id,
            consecutive_days=1,
            last_attendance_date=today
        )
        db.add(new_attendance)
        db.commit()
        db.refresh(new_attendance)
        db_attendance = new_attendance
    
    return db_attendance

##################################################################################################
#단어 DB(quiz)


def create_quiz(db: Session, voca: schemas.VocaPairCreate):
    db_voca = models.VocaPair(
        Voca_id=voca.voca_id,
        quiz_korean=voca.Korean,
        quiz_eng=voca.Eng
    )
    db.add(db_voca)
    db.commit()
    db.refresh(db_voca)
    return db_voca


def create_AnswerLog(db: Session, AnswerLog: schemas.AnswerLogCreate):
    db_AnswerLog = models.AnswerLog(
        log_id=AnswerLog.log_id,
        user_id=AnswerLog.user_id,
        voca_id=AnswerLog.voca_id,
        is_answer=AnswerLog.is_answer,
        date=AnswerLog.date
    )
    db.add(db_AnswerLog)
    db.commit()
    db.refresh(db_AnswerLog)
    return db_AnswerLog


def get_quiz(db: Session, voca_id: int):
    return db.query(models.VocaPair).filter(models.VocaPair.voca_id == voca_id).first()


def get_AnswerLog(db: Session, user_id: int):
    return db.query(models.AnswerLog).filter(models.AnswerLog.user_id == user_id)


def update_quiz(db: Session, voca_id: int, updated_voca: schemas.AnswerLogCreate):
    voca = db.query(models.VocaPair).filter(models.VocaPair.voca_id == voca_id).first()
    for key, value in updated_voca.model_dump().items():
        setattr(voca, key, value)
    db.commit()
    db.refresh(voca)
    return voca


def delete_quiz(db: Session, voca_id: int):
    db_quiz = db.query(models.VocaPair).filter(models.VocaPair.voca_id== voca_id).first()
    if db_quiz:
        db.delete(db_quiz)
        db.commit()
    return db_quiz

# 메인페이지 단어
def get_voca_pair(db: Session, index: int | None):
    voca_count = db.query(models.VocaPair).count()
    if not index:
        voca_id = random.randint(1, voca_count)
    
    return db.query(models.VocaPair).filter(models.VocaPair.voca_id == voca_id).first()

def create_or_ignore_answer_log(db: Session, answer_log: schemas.AnswerLogCreate):
    # 특정 user_id와 voca_id가 이미 존재하는지 확인
    existing_logs = db.query(models.AnswerLog).filter(
        models.AnswerLog.user_id == answer_log.user_id,
        models.AnswerLog.voca_id == answer_log.voca_id
    ).all()

    # is_answer가 False일 때: 바로 로그를 저장
    if not answer_log.is_answer:
        return create_AnswerLog(db=db, AnswerLog=answer_log)

    # is_answer가 True일 때:
    # 1. 기존에 is_answer가 True인 로그가 없는 경우에만 vocabulary에 1점 추가
    is_answer_correct_logged = any(log.is_answer for log in existing_logs)
    if not is_answer_correct_logged:
        # KoreanAbility 업데이트 (vocabulary에 1점 추가)
        korean_ability = db.query(models.KoreanAbility).filter(
            models.KoreanAbility.user_id == answer_log.user_id
        ).first()

        if korean_ability:
            korean_ability.vocabulary += 1
            db.commit()
            db.refresh(korean_ability)

    # 2. 새로운 로그 추가
    return create_AnswerLog(db=db, AnswerLog=answer_log)


###############################################################################################################
#subject DB
def create_subject(db: Session, subject: schemas.SubjectCreate):
    db_subject = models.Subject(
        subject_id=subject.subject_id,
        subject_name=subject.subject_name,
        grade=subject.grade
    )
    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)
    return db_subject


def get_subject(db: Session, subject_id: int):
    return db.query(models.Subject).filter(models.Subject.subject_id == subject_id).first()

def get_random_subject(db: Session):
    return db.query(models.Subject).order_by(func.rand()).first()


def delete_subject(db: Session, subject_id: int):
    db_subject = db.query(models.Subject).filter(models.Subject.subject_id == subject_id).first()
    if db_subject:
        db.delete(db_subject)
        db.commit()
    return db_subject

# 채팅 id로 subject title 받아오기
def get_chats_with_titles(db: Session, user_id: int):
    result = db.query(
        models.Chat.chat_id, 
        models.Subject.subject_name,
        models.Chat.created_time
    ).join(
        models.Subject, 
        models.Chat.subject_id == models.Subject.subject_id
    ).filter(
        models.Chat.user_id == user_id
    ).order_by(
        models.Chat.created_time.desc()  # 내림차순 정렬 (최신 항목이 위로 가도록 정렬)
    ).all()
    
    return result


##############################################################################################################
# 채팅 DB
def get_chat_id() -> str:
    # UUID를 기반으로 20자리 랜덤 문자열 생성
    return str(uuid.uuid4())[:20]
def create_chat(db: Session, user_id: int, subject_id: int):
    # Chat ID 생성
    chat_id = get_chat_id()

    # 새로운 채팅 생성
    new_chat = models.Chat(
        chat_id=chat_id,
        user_id=user_id,
        subject_id=subject_id,
        created_time=datetime.now()  # created_time 필드 추가
    )

    try:
        # 데이터베이스에 저장
        db.add(new_chat)
        db.commit()
        db.refresh(new_chat)
    except Exception as e:
        print(f"Error : {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Chat creation failed")

    # 반환할 때 Pydantic 모델로 변환
    return schemas.Chat.from_orm(new_chat)


def create_chatMessage(db: Session, chatMessage: schemas.ChatMessageCreate):
    db_chatMessage = models.ChatMessage(
        chat_id=chatMessage.chat_id,
        msg_id=chatMessage.msg_id,
        content=chatMessage.content,
        created_time=chatMessage.created_time,
        is_human=chatMessage.is_human
    )
    db.add(db_chatMessage)
    db.commit()
    db.refresh(db_chatMessage)
    return db_chatMessage


#채팅방 정보
def get_chat_list(db: Session, user_id: int):
    return db.query(models.Chat).filter(models.Chat.user_id == user_id).order_by(models.Chat.created_time).all()


#채팅방 별 메시지 정보
def get_chatLog(db: Session, chat_id: int):
    return db.query(models.ChatMessage).filter(models.ChatMessage.chat_id == chat_id).order_by(asc(models.ChatMessage.created_time)).all()

#채팅 방 삭제
def delete_chatroom(db: Session, chat_id: int):
    db_chatroom = db.query(models.Chat).filter(models.Chat.chat_id == chat_id).first()
    if db_chatroom:
        db.delete(db_chatroom)
        db.commit()
    return db_chatroom


#채팅 메세지 삭제
def delete_chatMessage(db: Session, msg_id: int):
    db_message = db.query(models.ChatMessage).filter(models.ChatMessage.msg_id == msg_id).first()
    if db_message:
        db.delete(db_message)
        db.commit()
    return db_message

def get_quiz_list(db: Session, num_quizzes: int):
    total_words_needed = num_quizzes * 4
    voca_pairs = db.query(models.VocaPair).order_by(func.random()).limit(total_words_needed).all()

    quizs = []
    for i in range(num_quizzes):
        selected_words = voca_pairs[i * 4:(i + 1) * 4]
        korean_word = random.choice(selected_words)
        english_words = [voca.Eng for voca in selected_words]
        
        # 셔플하여 정답의 위치를 랜덤하게 배치
        random.shuffle(english_words)
        
        quiz = {
            "voca_id": korean_word.voca_id,
            "korean": korean_word.Korean,
            "options": english_words,
        }
        quizs.append(quiz)

    return quizs

##퀴즈에서 단어를 클릭했을 경우 호출
def get_quiz_answer(db: Session, user_id : int, voca_id: int, answer: str):
    true_answer = db.query(models.VocaPair).filter(models.VocaPair.voca_id == voca_id).first()

    if true_answer.Eng == answer:
        existing_logs = db.query(models.AnswerLog).filter(
        models.AnswerLog.user_id == user_id,
        models.AnswerLog.voca_id == voca_id
        ).all()

        #맞춘 기록이 있는가?
        is_answer_correct_logged = any(log.is_answer for log in existing_logs)

        #기존에 is_answer가 True인 로그가 없는 경우에만 vocabulary에 1점 추가
        if not is_answer_correct_logged:
            # KoreanAbility 업데이트 (vocabulary에 1점 추가)
            korean_ability = db.query(models.KoreanAbility).filter(
                models.KoreanAbility.user_id == user_id
            ).first()

            if korean_ability:
                korean_ability.vocabulary += 1
                db.commit()
                db.refresh(korean_ability)

            log = models.AnswerLog(
            log_id=uuid.uuid4(),
            user_id=user_id,
            voca_id=voca_id,
            is_answer=True,
            date=datetime.now()
        )
            create_AnswerLog(db=db, AnswerLog=log)
        return True
    else:
        log = models.AnswerLog(
            log_id=uuid.uuid4(),
            user_id=user_id,
            voca_id=voca_id,
            is_answer=False,
            date=datetime.now()
        )
        create_AnswerLog(db=db, AnswerLog=log)
        return False
    
    
def create_chatMessage(db: Session, chat_message: schemas.ChatMessage, chat_id: str, is_human: bool):
    db_chatMessage = models.ChatMessage(
        chat_id=chat_id,
        msg_id=uuid.uuid4(),
        content=chat_message.content,
        created_time=datetime.now(),
        is_human=is_human
    )
    db.add(db_chatMessage)
    db.commit()
    db.refresh(db_chatMessage)
    return db_chatMessage