from sqlalchemy.orm import Session

from app.models.professional_model import Professional
from app.models.professional_clinic_model import ProfessionalClinic

from app.schemas.professional_schema import ProfessionalCreate, ProfessionalUpdate

from app.repositories.professional_repository import ProfessionalRepository
from app.repositories.clinic_repository import ClinicRepository
from app.repositories.professional_clinic_repository import ProfessionalClinicRepository

from app.core.exceptions import ProfessionalNotFoundError
from app.core.exceptions import ClinicNotFoundError
from app.core.exceptions import ProfessionalAlreadyAssociatedError


professional_repository = ProfessionalRepository()
clinic_repository = ClinicRepository()
professional_clinic_repository = ProfessionalClinicRepository()


def create_professional(
    db: Session,
    professional_data: ProfessionalCreate
) -> Professional:

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

    professional = professional_repository.create(
        db=db,
        professional=professional
    )

    return professional


def get_professionals(db: Session) -> list[Professional]:

    professionals = professional_repository.get_professionals(
        db=db
    )

    return professionals


def get_professional(
    db: Session,
    professional_id: int
) -> Professional | None:

    professional = professional_repository.get_by_id(
        db=db,
        professional_id=professional_id
    )

    return professional


def update_professional(
    db: Session,
    professional_id: int,
    professional_data: ProfessionalUpdate
) -> Professional | None:

    professional = get_professional(
        db=db,
        professional_id=professional_id,
    )

    if professional is None:
        return None

    data = professional_data.model_dump(exclude_unset=True)

    for field, value in data.items():
        setattr(professional, field, value)

    professional = professional_repository.update(
        db=db,
        professional=professional
    )

    return professional


def delete_professional(
    db: Session,
    professional_id: int
) -> bool:

    professional = get_professional(
        db=db,
        professional_id=professional_id,
    )

    if professional is None:
        return False

    return professional_repository.delete(
        db=db,
        professional=professional
    )


def add_clinic_to_professional(
    db: Session,
    professional_id: int,
    clinic_id: int
) -> ProfessionalClinic:

    professional = get_professional(
        db=db,
        professional_id=professional_id,
    )

    if professional is None:
        raise ProfessionalNotFoundError

    clinic = clinic_repository.get_by_id(
        db=db,
        clinic_id=clinic_id,
    )

    if clinic is None:
        raise ClinicNotFoundError

    existing = professional_clinic_repository.get_by_professional_and_clinic(
        db=db,
        professional_id=professional_id,
        clinic_id=clinic_id,
    )

    if existing is not None:
        raise ProfessionalAlreadyAssociatedError

    professional_clinic = professional_clinic_repository.create(
        db=db,
        professional_clinic=ProfessionalClinic(
            professional_id=professional_id,
            clinic_id=clinic_id,
        ),
    )

    return professional_clinic