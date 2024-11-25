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

def get_random_lab_id(db: Session) -> uuid.UUID:
    # Check if there are any labs in the database
    lab_count = db.query(Lab).count()
    
    if lab_count == 0:
        # If no labs exist, create a random lab
        lab = create_random_lab(db)
        return lab.lab_id
    
    # Get a random lab ID
    random_offset = random.randint(0, lab_count - 1)
    random_lab = db.query(Lab).offset(random_offset).first()
    return random_lab.lab_id
