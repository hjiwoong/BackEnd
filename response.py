# pydentic이 API응답 본문을 검증하려면 응답 모델을 정의해야 한다

from pydantic import BaseModel

# 할일 응답 모델 : 클라이언트에 반환되는 데이터의 구조를 정의
class TodoResponse(BaseModel): #응답 모델 이름 정의
        id:int #응답 본문 필드 구성
        title:str
        is_done:bool
