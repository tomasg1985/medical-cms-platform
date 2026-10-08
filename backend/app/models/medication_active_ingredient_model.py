from typing import TYPE_CHECKING


from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

if TYPE_CHECKING:
    from app.models.medication_model import Medication
    from app.models.active_ingredient_model import ActiveIngredient

class MedicationActiveIngredient(Base):
    __tablename__ = "medication_active_ingredients"
    
    medication_id: Mapped[int] = mapped_column(
        ForeignKey("medications.id"),
        primary_key=True,
        nullable=False
    )

    active_ingredients_id: Mapped[int] = mapped_column(
        ForeignKey("active_ingredients.id"),
        primary_key=True,
        nullable=False
    )
    
    medication: Mapped["Medication"] = relationship(
        back_populates="medication_active_ingredients"
    )
    
    active_ingredient: Mapped["ActiveIngredient"] = relationship(
        back_populates="medication_active_ingredients"
    )