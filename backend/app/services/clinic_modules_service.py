
from sqlalchemy.orm import Session

from app.models.clinic_modules_model import ClinicModule
from app.repositories.clinic_modules_repository import ClinicModuleRepository
from app.repositories.clinic_repository import ClinicRepository
from app.repositories.module_repository import ModuleRepository
from app.schemas.clinic_modules_schema import (
    ClinicModuleCreate,
    ClinicModuleUpdate,
)

clinic_module_repository = ClinicModuleRepository()
clinic_repository = ClinicRepository()
module_repository = ModuleRepository()


def create_clinic_module(
    db: Session,
    clinic_module_data: ClinicModuleCreate
) -> ClinicModule | None:

    clinic = clinic_repository.get_by_id(
        db=db,
        clinic_id=clinic_module_data.clinic_id
    )

    if clinic is None:
        return None

    module = module_repository.get_by_id(
        db=db,
        module_id=clinic_module_data.module_id
    )

    if module is None:
        return None

    clinic_module = ClinicModule(
        **clinic_module_data.model_dump()
    )

    return clinic_module_repository.create(
        db=db,
        clinic_module=clinic_module
    )


def get_clinic_modules(
    db: Session
) -> list[ClinicModule]:

    return clinic_module_repository.get_clinic_modules(
        db=db
    )


def get_clinic_module(
    db: Session,
    clinic_id: int,
    module_id: int
) -> ClinicModule | None:

    return clinic_module_repository.get_by_id(
        db=db,
        clinic_id=clinic_id,
        module_id=module_id
    )


def update_clinic_module(
    db: Session,
    clinic_id: int,
    module_id: int,
    clinic_module_data: ClinicModuleUpdate
) -> ClinicModule | None:

    clinic_module = get_clinic_module(
        db=db,
        clinic_id=clinic_id,
        module_id=module_id
    )

    if clinic_module is None:
        return None

    update_data = clinic_module_data.model_dump(
        exclude_unset=True
    )

    # status es obligatorio en el modelo; no permitimos actualizarlo a None.
    if "status" in update_data and update_data["status"] is None:
        raise ValueError("El estado no puede ser nulo.")

    for field, value in update_data.items():
        setattr(clinic_module, field, value)

    return clinic_module_repository.update(
        db=db,
        clinic_module=clinic_module
    )


def delete_clinic_module(
    db: Session,
    clinic_id: int,
    module_id: int
) -> bool:

    clinic_module = get_clinic_module(
        db=db,
        clinic_id=clinic_id,
        module_id=module_id
    )

    if clinic_module is None:
        return False

    return clinic_module_repository.delete(
        db=db,
        clinic_module=clinic_module
    )
