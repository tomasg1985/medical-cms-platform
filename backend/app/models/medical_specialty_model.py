from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from sqlalchemy import ForeignKey

class ProfessionalSpecialty(Base):
    __tablename__ = "professional_specialties"

    professional_id: Mapped[int] = mapped_column(
                ForeignKey("professionals.id"),
                nullable=False,
                primary_key=True
                )
    
    specialty_id: Mapped[int] = mapped_column(
                    ForeignKey("specialties.id"),
                    nullable=False,
                    primary_key=True
                    )