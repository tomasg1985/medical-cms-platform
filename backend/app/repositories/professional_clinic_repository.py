from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.professional_clinic_model import ProfessionalClinic


class ProfessionalClinicRepository:

    def create(
        self,
        db: Session,
        professional_clinic: ProfessionalClinic
    ) -> ProfessionalClinic:

        try:
            db.add(professional_clinic)
            db.commit()
            db.refresh(professional_clinic)

            return professional_clinic

        except Exception:
            db.rollback()
            raise

    def get_by_professional_and_clinic(
        self,
        db: Session,
        professional_id: int,
        clinic_id: int
    ) -> ProfessionalClinic | None:

        statement = select(ProfessionalClinic).where(
            ProfessionalClinic.professional_id == professional_id,
            ProfessionalClinic.clinic_id == clinic_id
        )

        result = db.execute(statement)
        professional_clinic = result.scalar_one_or_none()

        return professional_clinic