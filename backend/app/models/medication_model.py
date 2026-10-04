from typing import TYPE_CHECKING

from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

if TYPE_CHECKING:
    from app.models.prescription_item_model import PrescriptionItem
    from app.models.medication_presentation_model import MedicationPresentation
    from app.models.medication_active_ingredient_model import MedicationActiveIngredients

class Medication(Base):
    __tablename__ = "medications"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    laboratory: Mapped[str] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now, nullable=False)


    prescription_items: Mapped[list["PrescriptionItem"]] = relationship(
        back_populates="medication"
    )
    
    medication_presentations: Mapped[list["MedicationPresentation"]] = relationship(
        back_populates="medication"
    )
    
    medication_active_ingredients: Mapped[list["MedicationActiveIngredients"]] = relationship(
        back_populates="medication"
    )