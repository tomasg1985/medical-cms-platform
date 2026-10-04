from typing import TYPE_CHECKING

from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

if TYPE_CHECKING:
    from app.models.prescription_model import Prescription
    from app.models.medication_model import Medication
    

class PrescriptionItem(Base):
    __tablename__ = "prescription_items"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    dosage: Mapped[str] = mapped_column(nullable=False)
    frequency: Mapped[str] = mapped_column(nullable=False)
    duration: Mapped[str] = mapped_column(nullable=False)
    instructions: Mapped[str] = mapped_column(nullable=False)
    
    prescription_id: Mapped[int] = mapped_column(
        ForeignKey("prescriptions.id"),
        nullable=False
    )
    
    medication_id: Mapped[int] = mapped_column(
        ForeignKey("medications.id"),
        nullable=False
    )
    
    prescription: Mapped["Prescription"] = relationship(
        back_populates="prescription_items"
    )
    
    medication: Mapped["Medication"] = relationship(
        back_populates="prescription_items"
    )