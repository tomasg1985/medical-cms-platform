from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

if TYPE_CHECKING:
    from app.models.insurance_plan_model import InsurancePlan

class Insurance(Base):
    __tablename__ = "insurances"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    registration: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(nullable=False)


    insurance_plans: Mapped[list["InsurancePlan"]] = relationship(
        back_populates="insurance"
    )