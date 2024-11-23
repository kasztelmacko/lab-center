import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app.api.deps import CurrentUser, SessionDep
from app.models import Lab, LabCreate, LabPublic, LabsPublic, LabUpdate, Message

router = APIRouter()


@router.get("/", response_model=LabsPublic)
def read_labs(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve labs.
    """

    if current_user.is_superuser:
        count_statement = select(func.count()).select_from(Lab)
        count = session.exec(count_statement).one()
        statement = select(Lab).offset(skip).limit(limit)
        labs = session.exec(statement).all()
    else:
        count_statement = (
            select(func.count())
            .select_from(Lab)
            .where(Lab.owner_id == current_user.id)
        )
        count = session.exec(count_statement).one()
        statement = (
            select(Lab)
            .where(Lab.owner_id == current_user.id)
            .offset(skip)
            .limit(limit)
        )
        labs = session.exec(statement).all()

    return LabsPublic(data=labs, count=count)


@router.get("/{id}", response_model=LabPublic)
def read_lab(session: SessionDep, current_user: CurrentUser, id: uuid.UUID) -> Any:
    """
    Get lab by ID.
    """
    lab = session.get(Lab, id)
    if not lab:
        raise HTTPException(status_code=404, detail="Lab not found")
    if not current_user.is_superuser and (lab.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return lab


@router.post("/", response_model=LabPublic)
def create_lab(
    *, session: SessionDep, current_user: CurrentUser, lab_in: LabCreate
) -> Any:
    """
    Create new lab.
    """
    lab = Lab.model_validate(lab_in, update={"owner_id": current_user.id})
    session.add(lab)
    session.commit()
    session.refresh(lab)
    return lab


@router.put("/{id}", response_model=LabPublic)
def update_lab(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    id: uuid.UUID,
    lab_in: LabUpdate,
) -> Any:
    """
    Update a lab.
    """
    lab = session.get(Lab, id)
    if not lab:
        raise HTTPException(status_code=404, detail="Lab not found")
    if not current_user.is_superuser and (lab.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    update_dict = lab_in.model_dump(exclude_unset=True)
    lab.sqlmodel_update(update_dict)
    session.add(lab)
    session.commit()
    session.refresh(lab)
    return lab


@router.delete("/{id}")
def delete_lab(
    session: SessionDep, current_user: CurrentUser, id: uuid.UUID
) -> Message:
    """
    Delete a lab.
    """
    lab = session.get(Lab, id)
    if not lab:
        raise HTTPException(status_code=404, detail="Lab not found")
    if not current_user.is_superuser and (lab.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    session.delete(lab)
    session.commit()
    return Message(message="Lab deleted successfully")