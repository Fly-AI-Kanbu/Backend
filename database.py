from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import config

user = config.mysql_user
password = config.mysql_password
ip = config.mysql_ip
db_name = config.mysql_db
# MySQL 연결 설정
#SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{user}:{password}@{ip}/{db_name}"
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:1234@localhost:3306/kanbu"

# SQLAlchemy 엔진 생성
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True  # 연결 확인을 위한 옵션
)

# 세션 로컬 설정
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 베이스 클래스 생성
Base = declarative_base()

