from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.clinic_model import Clinic
    from app.models.professional_model import Professional

class Specialty(Base):
    __tablename__ = "specialties"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    official_name: Mapped[str] = mapped_column(nullable=False)
    alternative_name: Mapped[str] = mapped_column(nullable=False)
    short_description: Mapped[str] = mapped_column(nullable=False)
    snomed_code: Mapped[str] = mapped_column(nullable=False, unique=True)
    medical_exercise: Mapped[str] = mapped_column(nullable=False)


    clinics: Mapped[list["Clinic"]] = relationship(
            secondary="clinic_specialties",
            back_populates="specialties"
        )


    professionals: Mapped[list["Professional"]] = relationship(
            secondary="professional_specialties",
            back_populates="specialties"
        )