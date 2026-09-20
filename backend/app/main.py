"""
Punto de entrada principal de la aplicación.

Medical CMS Platform API
"""

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from app.config.settings import settings
from app.database import get_db
from app.routes.clinic_routes import router as clinic_router
from app.routes.patient_routes import router as patient_router
from app.routes.professional_routes import router as professional_router
from app.routes.specialty_routes import router as specialty_router
from app.routes.professional_specialty_routes import router as professional_specialty_router
from app.routes.appointment_routes import router as appointment_router
from app.routes.user_routes import router as user_router
from app.routes.role_routes import router as role_router
from app.routes.permission_routes import router as permission_router
from app.routes.role_permission_routes import router as role_permission_router
from app.routes.user_role_routes import router as user_role_router
from app.routes.user_clinic_routes import router as user_clinic_router


app = FastAPI(
    title=settings.app_name,
    description="API principal para gestión de clínicas y consultorios médicos",
    version=settings.app_version,
    debug=settings.debug,
)

app.include_router(clinic_router)
app.include_router(patient_router)
app.include_router(professional_router)
app.include_router(specialty_router)
app.include_router(professional_specialty_router)
app.include_router(appointment_router)
app.include_router(user_router)
app.include_router(role_router)
app.include_router(permission_router)
app.include_router(role_permission_router)
app.include_router(user_role_router)
app.include_router(user_clinic_router)



@app.get("/")
def root(db: Session = Depends(get_db)):
    """
    Endpoint inicial de prueba.

    Permite verificar que la API está funcionando.
    """

    return {
        "message": "✅ Medical CMS API funcionando correctamente",
        "status": "🟢 Online",
    }
