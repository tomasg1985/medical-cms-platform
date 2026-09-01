from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from sqlalchemy import ForeignKey


class ClinicSpecialty(Base):
    __tablename__ = "clinic_specialties"


    clinic_id: Mapped[int] = mapped_column(
                ForeignKey("clinics.id"),
                nullable=False,
                primary_key=True
                )


    specialty_id: Mapped[int] = mapped_column(
                    ForeignKey("specialties.id"),
                    nullable=False,
                    primary_key=True
                    )