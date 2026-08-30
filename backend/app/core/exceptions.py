class PatientNotFoundError(Exception):
    pass

class ClinicNotFoundError(Exception):
    pass

class ProfessionalNotFoundError(Exception):
    pass

class ProfessionalAlreadyAssociatedError(Exception):
    pass

class PatientAlreadyAssociatedError(Exception):
    pass
