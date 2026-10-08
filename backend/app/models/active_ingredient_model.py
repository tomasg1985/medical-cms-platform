from typing import TYPE_CHECKING

from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

if TYPE_CHECKING:
    from app.models.medication_active_ingredient_model import MedicationActiveIngredient

class ActiveIngredient(Base):
    __tablename__ = "active_ingredients"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    code: Mapped[str] = mapped_column(unique=True, nullable=False)
    status: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now, nullable=False)

    medication_active_ingredients: Mapped[list["MedicationActiveIngredient"]] = relationship(
        back_populates="active_ingredient"
    )
