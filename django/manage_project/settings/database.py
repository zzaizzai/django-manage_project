from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLAlchemy 데이터베이스 연결 설정
engine = create_engine('postgresql://admin:admin@localhost:5432/manage_project', connect_args={'options': '-c timezone=UTC'})

Base = declarative_base()

# SQLAlchemy 세션 설정
Session = sessionmaker(bind=engine)
session = Session()