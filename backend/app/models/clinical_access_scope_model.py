from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

if TYPE_CHECKING:
    from app.models.clinical_access_grant_scope_model import ClinicalAccessGrantScope

class ClinicalAccessScope(Base):
    __tablename__ = "clinical_access_scopes"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(unique=True, nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    
    clinical_access_grant_scopes: Mapped[list["ClinicalAccessGrantScope"]] = relationship(
        back_populates="scope"
    )