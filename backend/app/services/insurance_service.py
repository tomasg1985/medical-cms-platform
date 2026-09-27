from sqlalchemy.orm import Session

from app.models.insurance_model import Insurance
from app.repositories.insurance_repository import InsuranceRepository
from app.schemas.insurance_schema import InsuranceUpdate

from app.core.exceptions import InsuranceAlreadyExistsException

insurance_repository = InsuranceRepository()


def create_insurance(
    db: Session,
    name: str,
    registration: str
) -> Insurance:
    
    existing_insurance = insurance_repository.get_by_registration(
        db=db,
        registration=registration
    )
    
    if existing_insurance is not None:
        raise InsuranceAlreadyExistsException()


    insurance = Insurance(
        name=name,
        registration=registration
    )

    insurance = insurance_repository.create(
        db=db,
        insurance=insurance
    )

    return insurance


def get_insurances(db: Session) -> list[Insurance]:

    insurances = insurance_repository.get_insurances(
        db=db
    )
    
    return insurances


def get_insurance(db: Session, insurance_id: int) -> Insurance | None:
    
    insurance = insurance_repository.get_by_id(
        db=db,
        insurance_id=insurance_id
    )
    
    return insurance


def update_insurance(db: Session, insurance_id: int, insurance_data: InsuranceUpdate) -> Insurance | None:
    
    insurance = get_insurance(
        db=db,
        insurance_id=insurance_id,
    )
    
    if insurance is None:
        return None
    
    existing_insurance = insurance_repository.get_by_registration(
        db=db,
        registration=insurance_data.registration
    )
    
    if (existing_insurance is not None 
        and existing_insurance.id != insurance_id
    ):
        raise InsuranceAlreadyExistsException()
    
    insurance.name = insurance_data.name
    insurance.registration =insurance_data. registration
    
    insurance = insurance_repository.update(
        db=db,
        insurance=insurance
    )
    
    return insurance


def delete_insurance(
    db: Session,
    insurance_id: int
) -> bool:
    
    insurance = get_insurance(
        db=db,
        insurance_id=insurance_id,
    )
    
    if insurance is None:
        return False
    
    return insurance_repository.delete(
        db=db,
        insurance=insurance
    )
    