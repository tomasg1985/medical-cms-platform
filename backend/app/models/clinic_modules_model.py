from typing import TYPE_CHECKING

from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.clinic_model import Clinic
    from app.models.module_model import Module


class ClinicModule(Base):
    __tablename__ = "clinic_modules"

    status: Mapped[str] = mapped_column(nullable=False)
    activated_at: Mapped[datetime] = mapped_column(default=datetime.now, nullable=False)
    deactivated_at: Mapped[datetime | None] = mapped_column(nullable=True)

    clinic_id: Mapped[int] = mapped_column(
        ForeignKey("clinics.id"),
        primary_key=True,
        nullable=False
    )

    module_id: Mapped[int] = mapped_column(
        ForeignKey("modules.id"),
        primary_key=True,
        nullable=False
    )

    clinic: Mapped["Clinic"] = relationship(
        back_populates="clinic_modules"
    )

    module: Mapped["Module"] = relationship(
        back_populates="clinic_modules"
    )