from schema.response import TodoResponse #응답 모델 임포트 : API응답의 구조와 타입을 검증
from schema.request import TodoCreateRequest, TodoUpdateRequest
from fastapi import FastAPI, status, HTTPException

app = FastAPI()

# 할일 저장 임시 데이터 저장
todos = [
    {"id":1,"title":"공부하기","is_done":False},
    {"id":2,"title":"운동하기","is_done":True},
    {"id":3,"title":"책읽기","is_done":False}
]

# 전체 할 일 조회
@app.get( #GET API 정의
    "/todos",
    response_model=list[TodoResponse], #반환되는 데이터가 TodoResponse에서 정의한 필드와 타입에 맞는지 자동으로 검증
    status_code=status.HTTP_200_OK) #데이터 조회 요청이 성공했을 때
def get_todos_handler():
    return todos
# http://127.0.0.1:8000/docs 이 경로로 접속하는 것은 서버에 HTTP GET 요청을 직접 보내는 것과 같다

# 단일 할 일 조회, {경로 변수} 사용
@app.get(
    "/todos/{todo_id}", #경로로 접속하면 todo_id에 저장되고 함수의 매개변수로 전달
    response_model=TodoResponse,
    status_code=status.HTTP_200_OK)
def get_todo_handler(todo_id: int):
    for todo in todos:
        if todo["id"] == todo_id:
            return todo
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found") #예외 처리
# raise HTTPException(status_code=status.HTTP_상태코드, detail="오류 메시지")

# 할 일 생성
@app.post(
    "/todos",  #/todos 경로로 들어오는 생성 요청을 처리하기 위해 POST API정의하고 함수와 연결
    response_model=TodoResponse,
    status_code=status.HTTP_201_CREATED)
def create_todo_handler(body: TodoCreateRequest): #요청 본문을 body매개변수로 받고 타입을 지정
    new_todo = { #새 할일 데이터 생성
        "id" : len(todos) + 1, # id값 생성
        "title" : body.title,
        "is_done" : body.is_done
    }
    todos.append(new_todo) #리스트에서 새 할인 추가후 응답 반환
    return new_todo

# 할 일 수정
@app.patch(
    "/todos/{todo_id}",
    response_model=TodoResponse,
    status_code=status.HTTP_200_OK)
def update_todo_handler(todo_id: int, body: TodoUpdateRequest):
    for todo in todos: #수정 대상 데이터 탐색
        if todo["id"] == todo_id:
            if body.title is not None: #title 필드 조건부 수정
                todo["title"] = body.title
            if body.is_done is not None: #is_done 필드 조건부 수정
                todo["is_done"] = body.is_done
            return todo #수정된 데이터 반환
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found") #예외처리 존재하지 않는 데이터를 수정하려 했을 경우

# 할 일 삭제
@app.delete(
    "/todos/{todo_id}", #경로로 들어오는 삭제 요청을 처리할 DELETE API 정의하고 함수 연결
    status_code=status.HTTP_204_NO_CONTENT) #요청을 성공적으로 처리했지만 응답 본문으로 반환할 내용은 없음
def delete_todo_handler(todo_id:int):
    for todo in todos: #삭제 대상 데이터 탐색
        if todo["id"] == todo_id:
            todos.remove(todo) #데이터 삭제
            return #응답 본문 없이 함수 종료
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found") #예외 처리 존재하지 않는 데이터를 삭제처리