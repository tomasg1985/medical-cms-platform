"""
Punto de entrada principal de la aplicación.

Medical CMS Platform API
"""

from fastapi import FastAPI

from app.config.settings import settings


app = FastAPI(
    title=settings.app_name,
    description="API principal para gestión de clínicas y consultorios médicos",
    version=settings.app_version,
    debug=settings.debug,
)


@app.get("/")
def root():
    """
    Endpoint inicial de prueba.

    Permite verificar que la API está funcionando.
    """

    return {
        "message": "Medical CMS API funcionando correctamente",
        "status": "online",
    }