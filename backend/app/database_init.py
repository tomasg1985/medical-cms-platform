from app.database import Base, engine
from app.models import Clinic

Base.metadata.create_all(bind=engine)