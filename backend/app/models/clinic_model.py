from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

if TYPE_CHECKING:
    from app.models.patient_model import Patient
    from app.models.professional_model import Professional

class Clinic(Base):
    __tablename__ = "clinics"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    
    patients: Mapped[list["Patient"]] = relationship(
        back_populates="clinic"
    )
    
    professionals: Mapped[list["Professional"]] = relationship(
        secondary="professional_clinics",
        back_populates="clinics"
    )