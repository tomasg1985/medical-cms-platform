from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase


from app.config.settings import settings

class Base(DeclarativeBase):
    pass


DATABASE_URL = (
    f"postgresql+psycopg://"
    f"{settings.db_user}:{settings.db_password}"
    f"@{settings.db_host}:{settings.db_port}"
    f"/{settings.db_name}"
)

# Infraestrucura de conexión
engine = create_engine(DATABASE_URL)

# Fabrica de sesiones
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Administracion de sesión durante la ejecución
def get_db():

    # Sesión que usa el endpoint para trabajar con la base de datos
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()