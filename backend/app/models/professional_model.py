from datetime import date

from sqlalchemy import Date
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base

class Professional(Base):
    __tablename__ = "professionals"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    gender: Mapped[str] = mapped_column(nullable=False)
    birth_date: Mapped[date] = mapped_column(Date, nullable=False)
    phone: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    credential: Mapped[str] = mapped_column(nullable=False)
    credential_expiration: Mapped[date] = mapped_column(Date, nullable=False)
    dni: Mapped[str] = mapped_column(nullable=False)
    specialty: Mapped[str] = mapped_column(nullable=False)
    address: Mapped[str] = mapped_column(nullable=False)
    medical_facility: Mapped[str] = mapped_column(nullable=False)
    working_insurance: Mapped[str] = mapped_column(nullable=False)