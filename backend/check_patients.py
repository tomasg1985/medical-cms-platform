from sqlalchemy import text

from app.database import engine


with engine.connect() as connection:
    result = connection.execute(
        text("""
            SELECT id, name, last_name
            FROM patients
            ORDER BY id
        """)
    )

    for patient in result:
        print(patient)