
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.module_model import Module
from app.repositories.module_repository import ModuleRepository
from app.schemas.module_schema import ModuleCreate, ModuleUpdate
from app.core.exceptions import ModuleAlreadyExistsException, ModuleNotFoundException

module_repository = ModuleRepository()


def create_module(
    db: Session,
    module_data: ModuleCreate
) -> Module:

    module = Module(
        **module_data.model_dump()
    )

    try:
        return module_repository.create(
            db=db,
            module=module
        )
    except IntegrityError as error:
        original_error = error.orig
        constraint_name = getattr(
            getattr(original_error, "diag", None),
            "constraint_name",
            None
        )

        if constraint_name == "modules_name_key":
            raise ModuleAlreadyExistsException(
                "Ya existe un módulo con ese nombre. Prueba con otro nombre."
            ) from error

        raise


def get_modules(db: Session) -> list[Module]:
    return module_repository.get_modules(db=db)


def get_module(
    db: Session,
    module_id: int
) -> Module:
    module = module_repository.get_by_id(
        db=db,
        module_id=module_id
    )

    if module is None:
        raise ModuleNotFoundException(
            "No encontramos el módulo solicitado."
        )

    return module


def update_module(
    db: Session,
    module_id: int,
    module_data: ModuleUpdate
) -> Module:

    module = get_module(
        db=db,
        module_id=module_id
    )

    update_data = module_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(module, field, value)

    try:
        return module_repository.update(
            db=db,
            module=module
        )
    except IntegrityError as error:
        original_error = error.orig
        constraint_name = getattr(
            getattr(original_error, "diag", None),
            "constraint_name",
            None
        )

        if constraint_name == "modules_name_key":
            raise ModuleAlreadyExistsException(
                "Ya existe un módulo con ese nombre. Prueba con otro nombre."
            ) from error

        raise


def delete_module(
    db: Session,
    module_id: int
) -> bool:

    module = get_module(
        db=db,
        module_id=module_id
    )

    return module_repository.delete(
        db=db,
        module=module
    )
