from fastapi import FastAPI, Depends, HTTPException, Request, UploadFile , File
from fastapi.responses import Response
from sqlalchemy.orm import Session
import crud, schemas
import models
import io
from typing import List
from sqlalchemy import func
import random
import datetime
from database import SessionLocal, engine
from uuid import uuid4
from fastapi.middleware.cors import CORSMiddleware
import requests
from fastapi.responses import JSONResponse, StreamingResponse
from sqlalchemy import desc,asc
# 데이터베이스 테이블 생성
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 출처에서 오는 요청을 허용
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용 (GET, POST, PUT, DELETE 등)
    allow_headers=["*"],  # 모든 헤더 허용
)# Dependency
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
async def get_userinfomation_from_db(user_id: int, db: Session = Depends(get_db)):
    user_id = 1 # 구현 확인을 위한 임시 data, 추후 업데이트 예정
    user = crud.get_user(user_id = user_id, db = db)
    if not user:
        raise HTTPException(status_code=404, detail = "User not found")
    country = crud.get_country(country_id = user.country_id, db = db)
    country_name = country.name # 국가 이름 반환

    return {"user_id" : user.user_id, "user_name" : user.first_name + ' ' + user.last_name, "country" : country_name}

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
def create_chat(user_id: int, db: Session = Depends(get_db)):
    user_id = 1  # 임시 하드코딩된 데이터
    subject = crud.get_random_subject(db=db)
    subject_id = subject.subject_id
    subject_name = subject.subject_name  # 주제를 추출
    subject_name += " 이라는 주제로 이제 수업을 시작해. 너가 먼저 나에게 질문해."

    # 새로운 채팅 생성
    new_chat = crud.create_chat(db=db, user_id=user_id, subject_id=subject_id)
    number_of_previous_chat = crud.get_chat_list(db = db, user_id = user_id)
    if len(number_of_previous_chat) > 10:
        deleted_chat = crud.delete_chatroom(db = db, chat_id = number_of_previous_chat[0].chat_id) 
    # GPT에게 새 주제를 보냄
    ai_url = "http://127.0.0.1:2937/chat"  # GPT 서버로 요청
    gpt_response = requests.post(ai_url, json={"session_id": new_chat.chat_id, "message": subject_name})
    
    if gpt_response.status_code == 200:
        bot_reply = gpt_response.json().get("reply")
        
        # 첫 번째 GPT 응답을 DB에 저장
        chat_message = schemas.ChatMessageCreate(content=bot_reply)
        crud.create_chatMessage(
            db=db, 
            chat_message=chat_message, 
            chat_id=new_chat.chat_id, 
            is_human=False  # GPT 응답이므로 is_human은 False
        )
    else:
        return JSONResponse(status_code=500, content={"message": "Error communicating with GPT"})

    # 새로운 채팅 정보 및 GPT 첫 응답 반환
    return {"chat_id": new_chat.chat_id, "subject_name": subject_name, "first_message": bot_reply}


@app.post("/user/{chat_id}/create_chat_message")
def create_chat_message(user_id: int, db: Session = Depends(get_db)):
    chat_id = 1 # 구현 확인을 위한 임시 data, 추후 업데이트 예정
    new_chat_message = crud.create_chatMessage(db = db)
    # request 

# 채팅방 list 조회
@app.get("/user/{user_id}/get-chat-list")
def get_chat_list(user_id: int, db: Session = Depends(get_db)):
    user_id = 1  # 임시 데이터
    chat_list_with_titles = crud.get_chats_with_titles(db=db, user_id=user_id)

    # 이미 DB에서 created_time으로 정렬된 데이터를 반환
    return [{"chat_id": chat.chat_id, "subject_name": chat.subject_name, "chat_time": chat.created_time} for chat in chat_list_with_titles]

@app.get("/quiz-list")
def get_quiz(db: Session = Depends(get_db)):
    num_quiz = 20
    quizs = crud.get_quiz_list(db, num_quiz)
    return quizs
    
@app.post("/check-answer/")
def quiz_answer(request: schemas.QuizAnswerRequest, db: Session = Depends(get_db)):
    is_correct = crud.get_quiz_answer(db,request.user_id, request.voca_id, request.selected_answer)
    return {"is_correct": is_correct}

# 채팅 메시지 입력, DB랑 Chatbot으로 전송
#######한국어 능력 페이지######
#내 한국어 능력 보여줘
@app.get("/user/{user_id}/koability")
def get_koability(user_id : int, db: Session = Depends(get_db)):
    korean = crud.get_korean(db, user_id)
    return korean


# 채팅 메시지 입력, DB랑 Chatbot으로 전송
@app.post("/chat/{chat_id}/send_chat_message")
def send_chat_message(chat_id: str, chat_message: schemas.ChatMessageCreate, db: Session = Depends(get_db)):
    # 여기서는 URL에서 받은 chat_id를 사용해야 합니다. 따라서 하드코딩된 'chat123'을 제거합니다.

    # 새로운 채팅 메시지를 DB에 저장 (사용자가 보낸 메시지)
    new_chat_message_user = crud.create_chatMessage(
        db=db, 
        chat_message=chat_message, 
        chat_id=chat_id,  # URL에서 받은 chat_id를 사용
        is_human=True
    )
    user_message = chat_message.content

    # AI 서버로 POST 요청을 보내서 응답을 받음
    ai_url = "http://127.0.0.1:2937/chat2"  # AI 서버 URL 수정

    response = requests.post(
        ai_url,
        json={"session_id": chat_id, "message": user_message}
    )

    # AI 서버 응답 처리
    if response.status_code == 200:
        bot_reply = response.json().get('reply')
        chat_message.content = bot_reply
        # AI 응답을 DB에 저장
        new_chat_message_ai = crud.create_chatMessage(
            db=db, 
            chat_message=chat_message, 
            chat_id=chat_id, 
            is_human=False
        )
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return JSONResponse(status_code=500, content={"message": "Error communicating with GPT"})
    
    # AI 응답 반환
    return {"content": bot_reply, "created_time": new_chat_message_ai.created_time}


@app.get("/chat/{chat_id}/get_chat_log")
def get_chat_log(chat_id: str, db: Session = Depends(get_db)):
    # chat_id에 해당하는 모든 메시지를 오래된 순서대로 가져옴
    chat_messages = db.query(models.ChatMessage).filter(models.ChatMessage.chat_id == chat_id).order_by(asc(models.ChatMessage.created_time)).all()
    
    # 필요한 데이터만 반환
    return [{"content": msg.content, "created_time": msg.created_time, "is_human": msg.is_human} for msg in chat_messages]

@app.put("/chat/{chat_id}/finish-chat")
def finish_chat_message(chat_id: str, db: Session = Depends(get_db)):
    # chat_id = "chat123" # 구현 확인을 위한 임시 data, 추후 업데이트 예정
    chat_message_log = crud.get_chatLog(db = db, chat_id = chat_id)
    if not chat_message_log:
        raise HTTPException(status_code=404, detail="No chat message found for this chat_id.")
    
    user_id = 1 #db.query(models.Chat).filter(models.ChatMessage.chat_id == chat_id).first().user_id
    user_chat_log_len = len(crud.get_chat_list(db = db, user_id = user_id)) # 유저의 현재까지 채팅 횟수
    user_previous_ability = crud.get_korean(db = db, user_id = user_id) # 유저의 현재 점수 조회
    # is_human이 False인 메시지와 True인 메시지로 구분
    model_logs = [log for log in chat_message_log if not log.is_human]
    user_logs = [log for log in chat_message_log if log.is_human]

    results = []
    for i in range(len(user_logs)):
        model1_msg = model_logs[i]
        user_msg = user_logs[i]
        model2_msg = model_logs[i + 1]

        # 그룹화하여 TextInput으로 변환
        text_input = {
            "model1" : model1_msg.content,
            "user" : user_msg.content,
            "model2" : model2_msg.content,
        }
        results.append(text_input)
    url = 'http://127.0.0.1:597/predict'

    model_input = {
        "inputs": results
    }
    new_score = requests.post(url, json=model_input).json()
    # 점수 결과를 new_score 변수로 받아왔다고 가정, 
    # 이전 채팅 로그와 비교 후 업데이트
    updated_korean = user_previous_ability # 업데이트 정보를 전달받을 변수 생성
    updated_korean = schemas.KoreanAbilityBase(
        complexity=(user_previous_ability['complexity'] * user_chat_log_len + new_score['Delivery_score']) // (user_chat_log_len + 1),
        toxicity=(user_previous_ability['toxicity'] * user_chat_log_len + new_score['Toxicity_score']) // (user_chat_log_len + 1),
        fluency=(user_previous_ability['fluency'] * user_chat_log_len + new_score['mlum_score']) // (user_chat_log_len + 1),
        accuracy=(user_previous_ability['accuracy'] * user_chat_log_len + new_score['cos_sim_answer']) // (user_chat_log_len + 1),
        context_score=(user_previous_ability['context_score'] * user_chat_log_len + new_score['cos_sim_question']) // (user_chat_log_len + 1),
        vocabulary=user_previous_ability['vocabulary']
    )
    
    updated_score = crud.update_korean(db = db, user_id = user_id, updated_korean = updated_korean)
    print(updated_score)
    return {'complexity': updated_score.complexity,
            'toxicity': updated_score.toxicity,
            'context_score': updated_score.context_score,
            'accuracy': updated_score.accuracy,
            'fluency': updated_score.fluency
            }
    

#####전화페이지######
#전화 버튼이 있다면 눌러라
@app.post("/call")
def user_call(chat_id: str=None, file: UploadFile = File(...), db: Session = Depends(get_db)):
    url = 'http://localhost:597'  # AI 서버 주소
    url2 = 'http://localhost:2937'
    session_id = str(uuid4())

    # STT 요청: 파일을 STT API로 전송
    with file.file as audio_file:
        stt_response = requests.post(
            url + '/stt',
            files={'file': (file.filename, audio_file, file.content_type)}
        )

    if stt_response.status_code != 200:
        raise HTTPException(status_code=stt_response.status_code, detail="STT failed")

    # STT 응답에서 텍스트 추출
    user_message = stt_response.json().get('transcript')
    if not user_message:
        raise HTTPException(status_code=400, detail="No transcript found in STT response")

    print(f"User message: {user_message}")
    ## STT로 받은 텍스트를 DB에 저장 (사용자가 보낸 메시지로)
    # crud.create_chatMessage(db=db, chat_message=user_message, chat_id=chat_id, is_human=True)

    # GPT 모델에 텍스트를 전송하여 응답 받기
    response = requests.post(
        url2 + '/chat3',
        json={"session_id": session_id, "message": user_message}  # Correct field names
    )

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Chat model request failed")

    bot_reply = response.json().get('reply')
    if not bot_reply:
        raise HTTPException(status_code=400, detail="No response from GPT model")

    # GPT 응답에서 TTS로 변환할 텍스트 추출
    input_tts = bot_reply.split('발음:')[0][4:]  # 혹은 필요한 텍스트 추출 방식 사용
    print(f"GPT reply: {input_tts}")

    ## GPT 모델의 응답을 DB에 저장 (모델이 보낸 메시지로)
    # crud.create_chatMessage(db=db, chat_message=bot_reply, chat_id=chat_id, is_human=False)

    # TTS 요청: GPT 모델의 응답을 음성으로 변환
    speed = 1.0
    voice = 'nova'
    data = {
        "input_text": input_tts,
        "speed": speed,
        "voice": voice
    }

    # TTS API 호출
    tts_response = requests.post(url + '/tts', data=data)

    if tts_response.status_code != 200:
        raise HTTPException(status_code=tts_response.status_code, detail=f"TTS API failed: {tts_response.text}")

    # TTS 응답을 메모리 스트림으로 변환하여 클라이언트에 전달
    audio_stream = io.BytesIO(tts_response.content)
    audio_stream.seek(0)

    return StreamingResponse(audio_stream, media_type='audio/mpeg', headers={
        "Content-Disposition": "attachment; filename=output.mp3"
    })