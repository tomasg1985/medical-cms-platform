from typing import TYPE_CHECKING

from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

if TYPE_CHECKING:
    from app.models.medication_model import Medication
    
class MedicationPresentation(Base):
    __tablename__ = "medication_presentations"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    presentation: Mapped[str] = mapped_column(nullable=False)
    concentration: Mapped[str] = mapped_column(nullable=False)
    quantity: Mapped[str] = mapped_column(nullable=False)
    unit: Mapped[str] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now, nullable=False)

    medication_id: Mapped[int] = mapped_column(
        ForeignKey("medications.id"),
        nullable=False
    )
    
    medication: Mapped["Medication"] = relationship(
        back_populates="medication_presentations"
    )