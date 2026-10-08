class PatientNotFoundError(Exception):
    pass

class PatientContactNotFoundException(Exception):
    pass

class PatientContactAlreadyExistsException(Exception):
    pass

class ClinicNotFoundError(Exception):
    pass

class ProfessionalNotFoundError(Exception):
    pass

class SpecialtyNotFoundError(Exception):
    pass

class ProfessionalAlreadyAssociatedError(Exception):
    pass

class PatientAlreadyAssociatedError(Exception):
    pass

class ProfessionalSpecialtyAlreadyAssociatedError(Exception):
    pass

class ClinicSpecialtyAlreadyAssociatedError(Exception):
    pass

class SpecialtySNOMEDAlreadyExistsError(Exception):
    pass

class AppointmentNotFoundError(Exception):
    pass

class AppointmentAvailabilityError(Exception):
    pass

class AppointmentConflictError(Exception):
    pass

class AppointmentCancelledError(Exception):
    pass

class UserClinicAlreadyAssociatedError(Exception):
    pass

class UserRoleAlreadyAssociatedError(Exception):
    pass

class RolePermissionAlreadyAssociatedError(Exception):
    pass

class RoleNotAuthorizedError(Exception):
    pass

class DepartmentMissmatchError(Exception):
    pass

class InsuranceNotFoundException(Exception):
    pass

class InsuranceAlreadyExistsException(Exception):
    pass

class InsuranceDeleteConflictException(Exception):
    pass

class PlanNotFoundException(Exception):
    pass

class InsurancePlanAlreadyExistsException(Exception):
    pass

class InsurancePlanNotFoundException(Exception):
    pass

class PatientInsurancePlanNotFoundException(Exception):
    pass

class PrescriptionNotFoundException(Exception):
    pass

class MedicalRecordNotFoundException(Exception):
    pass

class MedicalRecordAlreadyExistsException(Exception):
    pass

class StudyNotFoundException(Exception):
    pass

class MedicalDocumentNotFoundException(Exception):
    pass

class MedicalDocumentAlreadyExistsException(Exception):
    pass

class PrescriptionItemNotFoundException(Exception):
    pass

class MedicationNotFoundException(Exception):
    pass

class MedicationNotFoundException(Exception):
    pass

class MedicationPresentationNotFoundException(Exception):
    pass

class ActiveIngredientNotFoundException(Exception):
    pass

class ActiveIngredientAlreadyExistsException(Exception):
    pass

class MedicationActiveIngredientNotFoundException(Exception):
    pass

class MedicationActiveIngredientAlreadyExistsException(Exception):
    pass