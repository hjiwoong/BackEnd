#터미널에서 가상환경 생성하기
# > python -m venv .basic_fastapi
# > .basic_fastapi\scripts\activate

# fastapi 설치
# python.exe -m pip install --upgrade pip
# pip install "fastapi[standard]==0.128.0"

from fastapi import FastAPI

app = FastAPI()

# 서버 실행
@app.get("/")
def root_handler():
    return {"message":"start fastapi"}

# 저장 후
# > fastapi dev
# http://127.0.0.1:8000 으로 이동

# http://127.0.0.1:8000/docs Swagger UI 문서
# http://127.0.0.1:8000/redoc ReDoc 문서

# 서버 종료 ctrl + c

# 경로 사용
@app.get("/login") # 엔드포인트: 클라이언트가 서버에 요청을 보내기 위해 사용하는 http메서드와 경로의 조합
        # /login 경로에서 get 요청이 들어왔을 때 함수를 실행
def login_handler(): #endpoint 함수
    return {"message":"로그인 페이지에 오신 것을 환영합니다"}

# {경로 변수} 사용
@app.get("/users/{user_id}") # 경로에 직접 표시, 클라이언트는 해당 위치에 값을 포함해서 요청
def read_user_handler(user_id: int):
    return {"user_id":user_id, "message":f"사용자 {user_id} 정보 조회"}

# 클라이언트는 엔드포인트를 통해 어떤 경로에 어떤 요청을 하는지를 서버에 전달하고
# 서버는 해당 경로에 연결된 엔드포인트 함수를 실행해 요청에 맞는 응답을 반환한다.

# 쿼리query 파라미터 사용 : http://127.0.0.1:8000/items?max_price=1000
@app.get("/items")
def read_items_handler(max_price: int | None = None): # | 또는 None, = None는 초기값
    return {"max_price": max_price}

# pydantic : 파이썬의 데이터 검증 라이브러리, 입력된 데이터가 올바른 형식인지 확인
# 파이썬 콘솔에서 테스트
"""
>>> from pydantic import BaseModel
>>> class Item(BaseModel):
        name:str
        price:int
        in_stock:bool=True
>>> data = {"name":"apple","price":1000,"in_stock":False}
>>> new_item = Item(**data) #언팩킹
>>> print(new_item)
결과 name='apple' price=1000 in_stock=False
>>> data={"name":"orange","price":"abc"}
>>> new_item = Item(**data)
결과 오류 메시지
"""

from pydantic import BaseModel
class Item(BaseModel):
    name: str
    price: int
    in_stock: bool = True

# 새 아이템 등록 : post 생성 요청과 경로 매핑 설정
@app.post("/items")
def create_item_handler(item:Item):
    return {"message":f"아이템 '{item.name}'이 추가 되었습니다","item":item}

# 경로 변수, 쿼리 파라미터, 요청 본문 혼합 사용
@app.put("/items/{item_id}")
def update_item_handler(item_id:int,assignee:str,item:Item):
    return { # 엔드포인트 함수의 매개변수에 경로 변수, 쿼리 파라미터, 요청 본문 혼합 사용
        "item_id":item_id,
        "assignee":assignee,
        "item":item
    }

# 새 아이템 등록
@app.post("/items", response_model=Item) # 응답데이터를 Item 모델로 지정
def create_item_handler(item:Item):
    return item # 엔드포인트 함수의 반환값을 pydantic 모델로 된 객체로 지정
# 반환 데이터의 구조와 타입을 명확하게 정의하여 잘못된 데이터가 클라이언트에 전달되는 것을 방지

# 새 아이템 등록
# 성공시 반환할 상태 코드 지정: 클라이언트 요청에 대해 서버가 어떤 결과를 반환했는지를 나타내는 표준 규약
from fastapi import FastAPI, status
@app.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_item_handler(item:Item):
    return item

# FastAPI 엔드포인트 작성
"""
GET /orders/{order_id}
order_id(정수형)를 매개변수
함수 이름 get_order_handler
쿼리 파라미터 pick_up(논리형)을 받고 기본값은 None
order_id와 pick_up은 응답모델을 BaseModel로 정의
response_model 옵션을 사용해서 해당 응답 모델을 반환
완성된 API 동작 예시
요청: GET /orders/5?pick_up=true
응답: {"order_id":5, "pick_up":true}
"""
class OrderResponse(BaseModel):
    order_id: int
    pick_up: bool | None=None
@app.get("/orders/{order_id}", response_model=OrderResponse)
def get_order_handler(order_id: int, pick_up:bool | None = None):
    return {"order_id":order_id, "pick_up":pick_up}
