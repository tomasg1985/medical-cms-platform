from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from sqlalchemy import ForeignKey

class ProfessionalClinic(Base):
    __tablename__ = "professional_clinics"
    
    professional_id: Mapped[int] = mapped_column(
        ForeignKey("professionals.id"),
        nullable=False,
        primary_key=True
        )
    
    clinic_id: Mapped[int] = mapped_column(
            ForeignKey("clinics.id"),
            nullable=False,
            primary_key=True
            )