from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import crud, schemas
import models
from typing import List
from database import SessionLocal, engine

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


@app.get("/voca_pair", response_model=schemas.VocaPair)
def get_voca_for_main(db: Session = Depends(get_db)):
    voca_pair = crud.get_random_voca_pair(db)
    return voca_pair