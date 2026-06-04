# ORM모델 정의(데이터를 데이터베이스 테이블과 연결할 수 있는 형태)
# ORM모델을 사용하면 애플리케이션이 종료되더라도 데이터는 데이터베이스에 저장되어 사라지지 않는다

from sqlalchemy import Integer, String, Boolean # 칼럼 타입
from sqlalchemy.orm import Mapped, mapped_column #ORM 칼럼 매핑 도구
from database.orm import Base #ORM 부모 클래스

# ORM Todo 모델 정의, Base 클래스를 상속받아 할 일 데이터를 정의하는 ORM 모델, 데이터베이스 테이블과 1:1 매핑
class Todo(Base): #Base클래스를 상속받은 클래스만 SQLAlchemy가 테이블로 인식
    __tablename__ = 'todo' # 테이블 이름 지정, 테이블이 생성됨

    id: Mapped[int] = mapped_column( # 아이디 칼럼, Mapped: 이 속성이 ORM에 의해 관리되는 칼럼임을 나타내는 힌트
        Integer,
        primary_key=True,
        autoincrement=True # 값 자동 증가
    )
    title: Mapped[str] = mapped_column( #제목 칼럼, Mapped_column: 파이썬 클래스의 속성을 데이터베이스 칼럼으로 연결하는 역할
        String(255),
        nullable=False, # Not Null
    )
    is_done: Mapped[bool] = mapped_column( # 완료 여부 칼럼
        Boolean,
        nullable=False,
        default=False
    )