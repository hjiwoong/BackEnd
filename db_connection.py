from sqlalchemy import create_engine #엔진(engine): 데이터베이스와의 실제 연결을 관리하는 객체
from sqlalchemy.orm import sessionmaker #세션(session): ORM이 데이터베이스와 상호작용할 때 사용하는 작업 단위. 쿼리 요청마다 독립적인 세션 사용

# 데이터베이스 연결 정보 설정, mysql+pymysql://사용자명: 비밀번호@호스트:포트/데이터베이스명
DATABASE_URL = "mysql+pymysql://root:1234@Localhost:3306/fastapi_db"

# 엔진 생성 : 데이터베이스와 통신할 수 있는 엔진, 실행되는 sql쿼리가 로그로 출력
engine = create_engine(DATABASE_URL, echo=True)

# 세션 팩토리 생성: 세션 생성 도구
SessionFactory = sessionmaker(
    autocommit = False, # 개발자가 commit()을 호출해야 변경 사항이 확정됨
    autoflush = False, # 개발자가 flush()를 호출해야 쿼리가 실행
    expire_on_commit = False, # commit() 이후에도 세션에 있는 객체의 값을 유지
    bind = engine # 이 세션이 사용할 데이터베이스 엔진 지정
)