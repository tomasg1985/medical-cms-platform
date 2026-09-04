class PatientNotFoundError(Exception):
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
