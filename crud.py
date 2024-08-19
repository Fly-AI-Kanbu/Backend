from sqlalchemy.orm import Session
# from passlib.context import CryptContext  # 비밀번호 해시를 위한 패키지
from typing import List
import random
import models, schemas


# 비밀번호 해시 설정
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = "sss"  # pwd_context.hash(user.password)  # 비밀번호 해시 생성
    db_user = models.User(
        name=user.name,
        pwd=hashed_password,  # 실제 비밀번호 해시를 저장
        first_name=user.first_name,
        last_name=user.last_name,
        age=user.age,
        nickname=user.nickname,
        email=user.email,
        phone=user.phone,
        address=user.address,
        country_id=user.country_id,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.user_id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


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
        similarity=korean.similarity
    )
    db.add(db_korean)
    db.commit()
    db.refresh(db_korean)
    return db_korean



def get_korean(db: Session, user_id: int):
    return db.query(models.KoreanAbility).filter(models.KoreanAbility.user_id == user_id).first()


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

def create_attendance(db: Session, attend: schemas.AttendanceCreate):
    # attendance_date가 제공되지 않았을 경우 현재 시간을 기본값으로 설정
    db_attend = models.Attendance(
        user_id=attend.user_id,
        attendance_date=attend.attendance_date,
    )
    db.add(db_attend)
    db.commit()
    db.refresh(db_attend)
    return db_attend


def get_attendance(db: Session, user_id: int):
    attendances = db.query(models.Attendance).filter(models.Attendance.user_id == user_id).all()
    return [schemas.Attendance.from_orm(attendance) for attendance in attendances]


def get_recent_attendances(db: Session, user_id: int):
    # 최근 10개의 출석 데이터를 가져옴
    attendances = (
        db.query(models.Attendance)
        .filter(models.Attendance.user_id == user_id)
        .order_by(models.Attendance.attendance_date.desc())  # 날짜 기준으로 내림차순 정렬
        .limit(10)  # 최근 10개만 가져옴
        .all()
    )
    return [schemas.Attendance.from_orm(attendance) for attendance in attendances]


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
def get_random_voca_pair(db: Session):
    voca_count = db.query(models.VocaPair).count()
    random_id = random_id = random.randint(1, voca_count)
    return db.query(models.VocaPair).filter(models.VocaPair.voca_id == random_id).first()

from sqlalchemy.orm import Session
import models, schemas

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


def get_subjects(db: Session, subject_id: int):
    return db.query(models.Subject).filter(models.Subject.subject_id == subject_id)


def delete_subject(db: Session, subject_id: int):
    db_subject = db.query(models.Subject).filter(models.Subject.subject_id == subject_id).first()
    if db_subject:
        db.delete(db_subject)
        db.commit()
    return db_subject


##############################################################################################################
# 채팅 DB
def create_ (db: Session, chat: schemas.ChatCreate):
    db_chatInfo = models.Chat(
        chat_id=chat.chat_id,
        user_id =chat.user_id,
        subject_id=chat.subject_id,
        created_time=chat.created_time
    )
    db.add(db_chatInfo)
    db.commit()
    db.refresh(db_chatInfo)
    return db_chatInfo


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
def get_chat(db: Session, user_id: int):
    return db.query(models.Chat).filter(models.Chat.user_id == user_id).all()


#채팅방 별 로그 정보
def get_chatLog(db: Session, chat_id: int):
    return db.query(models.ChatMessage).filter(models.ChatMessage.chat_id == chat_id)


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
