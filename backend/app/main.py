"""
Punto de entrada principal de la aplicación.

Medical CMS Platform API
"""

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from app.config.settings import settings
from app.database import get_db
from app.routes.clinic import router as clinic_router
from app.routes.patient import router as patient_router


app = FastAPI(
    title=settings.app_name,
    description="API principal para gestión de clínicas y consultorios médicos",
    version=settings.app_version,
    debug=settings.debug,
)

app.include_router(clinic_router)
app.include_router(patient_router)

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
