from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class UserClinic(Base):
    __tablename__ = "user_clinics"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        primary_key=True
        )

    clinic_id: Mapped[int] = mapped_column(
        ForeignKey("clinics.id"),
        nullable=False,
        primary_key=True
        )