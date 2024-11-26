from fastapi.testclient import TestClient
from sqlmodel import Session
import uuid
import random

from app import crud
from app.core.config import settings
from app.models import Lab, LabCreate, LabUpdate
from app.tests.utils.utils import random_lower_string

def create_random_lab(db: Session) -> Lab:
    lab_place = random_lower_string()
    lab_university = random_lower_string()
    lab_num = random_lower_string()
    lab_in = LabCreate(lab_place=lab_place, lab_university=lab_university, lab_num=lab_num)
    db_lab = Lab.model_validate(lab_in)
    db_lab.lab_id = uuid.uuid4()
    db.add(db_lab)
    db.commit()
    db.refresh(db_lab)
    return db_lab

