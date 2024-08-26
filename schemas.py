from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# User 모델
class UserBase(BaseModel):
    account_id: str
    pwd: str
    first_name: str
    last_name: str
    age: int
    nickname: Optional[str] = None
    email: str
    phone: str
    address: str
    country_id: int

class UserCreate(UserBase):
    pass

class User(UserBase):
    user_id: int

    class Config:
        from_attributes = True  # Allows Pydantic to work with ORM models

# Country 모델
class CountryBase(BaseModel):
    country_id: int
    iso: Optional[str] = None
    name: Optional[str] = None
    nicename: Optional[str] = None
    iso3: Optional[str] = None
    numcode: Optional[int] = None
    phonecode: Optional[int] = None

class CountryCreate(CountryBase):
    pass

class Country(CountryBase):
    class Config:
        from_attributes = True
class CountryImageBase(BaseModel):
    country_id: int
    country_img: bytes
    img_type: str

class CountryImageCreate(CountryImageBase):
    pass

class CountryImage(CountryImageBase):
    class Config:
        from_attributes = True

class CountryWithImage(BaseModel):
    country: Country
    country_img: CountryImage

# Subscribe 모델
class SubscribeBase(BaseModel):
    sub_id: str
    sub_name: str
    price: str

class SubscribeCreate(SubscribeBase):
    pass

class Subscribe(SubscribeBase):
    class Config:
        from_attributes = True

# KoreanAbility 모델
class KoreanAbilityBase(BaseModel):
    complexity: int = 0
    toxicity: int = 0
    fluency: int = 0
    vocabulary: int = 0
    accuracy: int = 0
    context_score: int = 0

class KoreanAbilityCreate(KoreanAbilityBase):
    user_id: int

class KoreanAbility(KoreanAbilityBase):
    ability_id: int

    class Config:
        from_attributes = True

# Chat 모델
class ChatBase(BaseModel):
    chat_id: str
    user_id: int
    subject_id: int
    created_time: datetime



class Chat(ChatBase):
    class Config:
        from_attributes = True

# VocaPair 모델
class VocaPairBase(BaseModel):
    voca_id: int
    Korean: str
    Eng: str

class VocaPairCreate(VocaPairBase):
    pass

class VocaPair(VocaPairBase):
    class Config:
        from_attributes = True

# ChatMessage 모델
class ChatMessageBase(BaseModel):
    msg_id: str
    chat_id: str
    content: str
    created_time: datetime
    is_human: bool

class ChatMessageCreate(ChatMessageBase):
    pass

class ChatMessage(ChatMessageBase):
    class Config:
        from_attributes = True

# AnswerLog 모델
class AnswerLogBase(BaseModel):
    log_id: str
    user_id: int
    voca_id: int
    is_answer: bool
    date: datetime

class AnswerLogCreate(AnswerLogBase):
    pass

class AnswerLog(AnswerLogBase):
    class Config:
        from_attributes = True

# Subject 모델
class SubjectBase(BaseModel):
    subject_id: int
    subject_name: str
    grade: str

class SubjectCreate(SubjectBase):
    pass

class Subject(SubjectBase):
    class Config:
        from_attributes = True

# Attendance 모델
class AttendanceBase(BaseModel):
    user_id: int
    attendance_id: int = None
    attendance_date: datetime = datetime.now().date()

class AttendanceCreate(AttendanceBase):
    pass

class Attendance(AttendanceBase):
    class Config:
        from_attributes = True

# Consecutive_Attendance 모델
class ConsecutiveAttendanceBase(BaseModel):
    user_id: int
    last_attendance_date: datetime
    Consecutive_days: int = 1

class ConsecutiveAttendanceCreate(ConsecutiveAttendanceBase):
    pass

class ConsecutiveAttendance(ConsecutiveAttendanceBase):
    class Config:
        from_attributes = True

# AccessToken 모델
class AccessTokenBase(BaseModel):
    Key: int
    user_id: int
    access_token: str
    expiration_date: datetime

class AccessTokenCreate(AccessTokenBase):
    pass

class AccessToken(AccessTokenBase):
    class Config:
        from_attributes = True

# SubscribeLog 모델
class SubscribeLogBase(BaseModel):
    user_sub_log: str
    user_id: int
    sub_id: str
    pay_date: datetime
    payoff_date: datetime
    status: bool

class SubscribeLogCreate(SubscribeLogBase):
    pass

class SubscribeLog(SubscribeLogBase):
    class Config:
        from_attributes = True

class QuizAnswerRequest(BaseModel):
    user_id: int
    voca_id: int
    selected_answer: str

# ChatMessage 모델
class ChatMessageBase(BaseModel):
    content: str

class ChatMessageCreate(ChatMessageBase):
    pass

class ChatMessage(ChatMessageBase):
    chat_id: str
    is_human: bool
    msg_id: str
    created_time: datetime
    class Config:
        from_attributes = True

        