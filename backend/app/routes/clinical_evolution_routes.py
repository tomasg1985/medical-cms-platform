from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.clinical_evolution_schema import ClinicalEvolutionModelCreate, ClinicalEvolutionUpdate, ClinicalEvolutionModelResponse
from app.services.clinical_evolution_service import create_clinical_evolution