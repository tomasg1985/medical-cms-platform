
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.engine import URL, make_url
from sqlalchemy.orm import sessionmaker

from app.config.settings import settings
from app.database import Base, get_db
from app.main import app

from app import models  # noqa: F401 — registra todos los modelos


TEST_DB_NAME = "medical_cms_test"


def build_test_database_url() -> URL:
    url = URL.create(
        drivername="postgresql+psycopg",
        username=settings.db_user,
        password=settings.db_password,
        host=settings.db_host,
        port=settings.db_port,
        database=TEST_DB_NAME,
    )

    # Protección: no permitir una base distinta de medical_cms_test.
    if url.database != TEST_DB_NAME:
        raise RuntimeError(
            f"Base de pruebas no permitida: {url.database!r}"
        )

    return url


TEST_DATABASE_URL = build_test_database_url()

# Segunda validación antes de crear el motor de conexión.
if make_url(TEST_DATABASE_URL).database != TEST_DB_NAME:
    raise RuntimeError("Conexión bloqueada: la base no es medical_cms_test.")

test_engine = create_engine(TEST_DATABASE_URL)

# Verificar la base real antes de permitir cualquier creación de tablas.
with test_engine.connect() as connection:
    actual_database = connection.exec_driver_sql(
        "SELECT current_database()"
    ).scalar_one()

    if actual_database != TEST_DB_NAME:
        test_engine.dispose()
        raise RuntimeError(
            f"Conexión bloqueada: se esperaba {TEST_DB_NAME!r}, "
            f"pero PostgreSQL informó {actual_database!r}."
        )

@pytest.fixture(scope="session", autouse=True)
def initialize_test_schema():
    # Solo crea tablas en el motor cuya base fue validada arriba.
    Base.metadata.create_all(bind=test_engine)
    yield
    test_engine.dispose()


@pytest.fixture
def client():
    connection = test_engine.connect()
    transaction = connection.begin()

    TestSessionLocal = sessionmaker(
        bind=connection,
        autoflush=False,
        autocommit=False,
        join_transaction_mode="create_savepoint",
    )

    def override_get_db():
        db = TestSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.pop(get_db, None)
        transaction.rollback()
        connection.close()
