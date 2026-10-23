from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase


from app.config.settings import settings

class Base(DeclarativeBase):
    pass


DATABASE_URL = URL.create(
    drivername="postgresql+psycopg",
    username=settings.db_user,
    password=settings.db_password,
    host=settings.db_host,
    port=settings.db_port,
    database=settings.db_name,
)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

def get_db():

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()