
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.professional_model import Professional
from app.schemas.professional_schema import ProfessionalCreate, ProfessionalUpdate

def create_professional(
    db: Session,
    professional_data: ProfessionalCreate
) ->Professional:
    
    professional = Professional(
        name=professional_data.name,
        last_name=professional_data.last_name,
        gender=professional_data.gender,
        birth_date=professional_data.birth_date,
        phone=professional_data.phone,
        email=professional_data.email,
        credential=professional_data.credential,
        credential_expiration=professional_data.credential_expiration,
        dni=professional_data.dni,
        specialty=professional_data.specialty,
        address=professional_data.address,
        medical_facility=professional_data.medical_facility,
        working_insurance=professional_data.working_insurance
    )

    try:
        db.add(professional)
        db.commit()
        db.refresh(professional)
        
        return professional

    except Exception:
        db.rollback()
        raise


def get_professionals(db: Session,) -> list[Professional]:
    statement = select(Professional)
    result = db.execute(statement)
    professionals = result.scalars().all()
    
    return professionals


def get_professional(db: Session, professional_id: int) -> Professional | None:
    statement = select(Professional).where(Professional.id == professional_id)
    result = db.execute(statement)
    professional = result.scalar_one_or_none()
    
    return professional


def update_professional(db: Session, professional_id: int, professional_data: ProfessionalUpdate) -> Professional | None:
    
    professional = get_professional(
            db=db,
            professional_id=professional_id,
        )
    
    if professional is None:
            return None
    
    data= professional_data.model_dump(exclude_unset=True)

    for field, value in data.items():
        setattr(professional, field, value)

    try:
        db.commit()
        db.refresh(professional)

        return professional

    except Exception:
        db.rollback()
        raise


def delete_professional(db: Session, professional_id: int) -> bool:

    professional = get_professional(
        db=db,
        professional_id=professional_id,
    )

    if professional is None:
        return False

    try:
        db.delete(professional)
        db.commit()

        return True

    except Exception:
        db.rollback()
        raise