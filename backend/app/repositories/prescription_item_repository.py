from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.prescription_item_model import PrescriptionItem


class PrescriptionItemRepository:
    def get_by_id(self, db: Session, prescription_item_id: int) -> PrescriptionItem | None:
        statement = (
            select(PrescriptionItem)
            .where(PrescriptionItem.id == prescription_item_id)
        )
        result = db.execute(statement)
        prescription_item = result.scalar_one_or_none()
        
        return prescription_item


    def get_prescription_items(self, db: Session) -> list[PrescriptionItem]:
        statement = select(PrescriptionItem)
        result = db.execute(statement)
        prescription_items = result.scalars().all()

        return prescription_items


    def create(self, db: Session, prescription_item: PrescriptionItem) -> PrescriptionItem:
        try:
            db.add(prescription_item)
            db.commit()
            db.refresh(prescription_item)
            
            return prescription_item
        except Exception:
            db.rollback()
            raise


    def update(self, db: Session, prescription_item: PrescriptionItem) -> PrescriptionItem:
        try:
            db.commit()
            db.refresh(prescription_item)

            return prescription_item
        except Exception:
            db.rollback()
            raise


    def delete(self, db: Session, prescription_item: PrescriptionItem) -> bool:
        try:
            db.delete(prescription_item)
            db.commit()
            
            return True
        
        except Exception:
            db.rollback()
            raise