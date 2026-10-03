from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

if TYPE_CHECKING:
    from app.models.clinical_access_grant_model import ClinicalAccessGrant
    from app.models.clinical_access_scope_model import ClinicalAccessScope
class ClinicalAccessGrantScope(Base):
    __tablename__ = "clinical_access_grant_scopes"
    
    clinical_access_grant_id: Mapped[int] = mapped_column(
        ForeignKey("clinical_access_grants.id"),
        primary_key=True,
        nullable=False
    )
    
    scope_id: Mapped[int] = mapped_column(
        ForeignKey("clinical_access_scopes.id"),
        primary_key=True,
        nullable=False
    )
    
    scope: Mapped["ClinicalAccessScope"] = relationship(
        back_populates="clinical_access_grant_scopes"
    )
    
    clinical_access_grant: Mapped["ClinicalAccessGrant"] = relationship(
        back_populates="clinical_access_grant_scopes"
    )