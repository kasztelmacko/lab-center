from fastapi.testclient import TestClient
from sqlmodel import Session
import uuid
import random

from app import crud
from app.core.config import settings
from app.models import Lab, LabCreate, LabUpdate
from app.tests.utils.utils import random_email, random_lower_string

def create_random_lab(db: Session) -> Lab:
    lab_name = random_lower_string()
    description = random_lower_string()
    lab_in = LabCreate(lab_name=lab_name, description=description)
    db_lab = Lab.model_validate(lab_in)
    db_lab.lab_id = uuid.uuid4()
    db.add(db_lab)
    db.commit()
    db.refresh(db_lab)
    return db_lab

