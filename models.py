from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Text, DateTime, Date, SmallInteger, BigInteger, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False)
    pwd = Column(String(15), nullable=False)
    first_name = Column(String(20), nullable=False)
    last_name = Column(String(20), nullable=False)
    age = Column(Integer, nullable=False)
    nickname = Column(String(20), nullable=True)
    email = Column(String(30), nullable=False)
    phone = Column(String(30), nullable=False)
    address = Column(String(60), nullable=False)
    country_id = Column(Integer, ForeignKey('country.country_id'), nullable=False)

    korean_abilities = relationship("KoreanAbility", back_populates="user", cascade="all, delete-orphan")
    country = relationship("Country", back_populates="users")
    access_tokens = relationship("AccessToken", back_populates="user", cascade="all, delete-orphan")
    attendances = relationship("Attendance", back_populates="user", cascade="all, delete-orphan")
    chats = relationship("Chat", back_populates="user", cascade="all, delete-orphan")
    subscribe_logs = relationship("SubscribeLog", back_populates="user", cascade="all, delete-orphan")
    log_quizzes = relationship("AnswerLog", back_populates="user", cascade="all, delete-orphan")



class KoreanAbility(Base):
    __tablename__ = 'korean_ability'

    ability_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete="CASCADE"), nullable=False)
    complexity = Column(Integer, nullable=False)
    toxicity = Column(Integer, nullable=False)
    fluency = Column(Integer, nullable=False)
    vocabulary = Column(Integer, nullable=False)
    similarity = Column(Integer, nullable=False)

    user = relationship("User", back_populates="korean_abilities")

class Chat(Base):
    __tablename__ = 'chat'

    chat_id = Column(String(50), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete="CASCADE"), nullable=False, default=1)
    subject_id = Column(Integer, ForeignKey('subject.subject_id'), nullable=False)
    created_time = Column(DateTime, nullable=False)

    user = relationship("User")
    subject = relationship("Subject")
    messages = relationship("ChatMessage", back_populates="chat", cascade="all, delete-orphan")

class VocaPair(Base):
    __tablename__ = 'voca_pair'

    voca_id = Column(Integer, primary_key=True, autoincrement=True)
    Korean = Column(String(10), nullable=False)
    Eng = Column(String(60), nullable=False)

class ChatMessage(Base):
    __tablename__ = 'chat_message'

    msg_id = Column(String(50), primary_key=True)
    chat_id = Column(String(50), ForeignKey('chat.chat_id', ondelete="CASCADE"), nullable=False)
    content = Column(Text, nullable=False)
    created_time = Column(DateTime, nullable=False)
    is_human = Column(Boolean, nullable=False)

    chat = relationship("Chat", back_populates="messages")
class AnswerLog(Base):
    __tablename__ = 'log_quiz'

    log_id = Column(String(10), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete="CASCADE"), nullable=False)
    voca_id = Column(Integer, nullable=False)
    is_answer = Column(Boolean, nullable=False)
    date = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="log_quizzes")

class Subject(Base):
    __tablename__ = 'subject'

    subject_id = Column(Integer, primary_key=True, autoincrement=True)
    subject_name = Column(String(50), nullable=False)
    grade = Column(String(2), nullable=False)

class Attendance(Base):
    __tablename__ = 'attendance'

    attendance_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete="CASCADE"), nullable=False)
    attendance_date = Column(DateTime, nullable=False)
    user = relationship("User", back_populates="attendances")
class Country(Base):
    __tablename__ = 'country'

    country_id = Column(Integer, primary_key=True, autoincrement=True)
    iso = Column(CHAR(2), nullable=True)
    name = Column(String(20), nullable=True)
    nicename = Column(String(20), nullable=True)
    iso3 = Column(CHAR(3), nullable=True)
    numcode = Column(SmallInteger, nullable=True)
    phonecode = Column(Integer, nullable=True)

    users = relationship("User", back_populates="country")

class Subscribe(Base):
    __tablename__ = 'subscribe'

    sub_id = Column(String(10), primary_key=True)
    sub_name = Column(String(20), nullable=False)
    price = Column(String(10), nullable=False)

class AccessToken(Base):
    __tablename__ = 'access_token'

    key = Column(BigInteger, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete="CASCADE"), nullable=False)
    access_token = Column(Text, nullable=False)
    expiration_date = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="access_tokens")

class SubscribeLog(Base):
    __tablename__ = 'subscribe_log'

    user_sub_log = Column(String(64), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False, default=1)
    sub_id = Column(String(10), ForeignKey('subscribe.sub_id'), nullable=False)
    pay_date = Column(DateTime, nullable=False)
    payoff_date = Column(DateTime, nullable=False)
    status = Column(Boolean, nullable=False)

    user = relationship("User")
    subscribe = relationship("Subscribe")
