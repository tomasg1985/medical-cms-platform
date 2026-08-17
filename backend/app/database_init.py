from app.database import Base, engine
from app.models import Clinic, Patient, Professional

Base.metadata.create_all(bind=engine)