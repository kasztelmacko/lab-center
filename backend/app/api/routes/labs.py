import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app.api.deps import CurrentUser, SessionDep
from app.models import (Lab, LabCreate, LabPublic, LabsPublic, LabUpdate, 
                        UserLab, AddUsersToLab, RemoveUsersFromLab, User,
                        Message)

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
            .where(Lab.owner_id == current_user.user_id)
        )
        count = session.exec(count_statement).one()
        statement = (
            select(Lab)
            .where(Lab.owner_id == current_user.user_id)
            .offset(skip)
            .limit(limit)
        )
        labs = session.exec(statement).all()

    return LabsPublic(data=labs, count=count)


@router.get("/{lab_id}", response_model=LabPublic)
def read_lab(session: SessionDep, current_user: CurrentUser, lab_id: uuid.UUID) -> Any:
    """
    Get lab by ID.
    """
    lab = session.get(Lab, lab_id)
    if not lab:
        raise HTTPException(status_code=404, detail="Lab not found")
    if not current_user.is_superuser and (lab.owner_id != current_user.user_id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return lab


@router.post("/", response_model=LabPublic)
def create_lab(
    *, session: SessionDep, current_user: CurrentUser, lab_in: LabCreate
) -> Any:
    """
    Create new lab.
    """
    lab = Lab.model_validate(lab_in, update={"owner_id": current_user.user_id})
    session.add(lab)
    session.commit()
    session.refresh(lab)
    return lab


@router.put("/{lab_id}", response_model=LabPublic)
def update_lab(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    lab_id: uuid.UUID,
    lab_in: LabUpdate,
) -> Any:
    """
    Update a lab.
    """
    lab = session.get(Lab, lab_id)
    if not lab:
        raise HTTPException(status_code=404, detail="Lab not found")
    if not current_user.is_superuser and (lab.owner_id != current_user.user_id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    update_dict = lab_in.model_dump(exclude_unset=True)
    lab.sqlmodel_update(update_dict)
    session.add(lab)
    session.commit()
    session.refresh(lab)
    return lab


@router.delete("/{lab_id}")
def delete_lab(
    session: SessionDep, current_user: CurrentUser, lab_id: uuid.UUID
) -> Message:
    """
    Delete a lab.
    """
    lab = session.get(Lab, lab_id)
    if not lab:
        raise HTTPException(status_code=404, detail="Lab not found")
    if not current_user.is_superuser and (lab.owner_id != current_user.user_id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    session.delete(lab)
    session.commit()
    return Message(message="Lab deleted successfully")

@router.post("/{lab_id}/add-users", response_model=Message)
def add_users_to_lab(
    *, session: SessionDep, current_user: CurrentUser, lab_id: uuid.UUID, add_users_in: AddUsersToLab
) -> Any:
    """
    Add users to a lab by providing a list of emails.
    """
    # Check if the current user is the owner of the lab
    lab = session.get(Lab, lab_id)
    if not lab:
        raise HTTPException(status_code=404, detail="Lab not found")
    if not current_user.is_superuser and (lab.owner_id != current_user.user_id):
        raise HTTPException(status_code=400, detail="Not enough permissions")

    # Find users by their emails
    emails = add_users_in.emails
    users = session.exec(select(User).where(User.email.in_(emails))).all()

    # Check if all users were found
    found_emails = {user.email for user in users}
    not_found_emails = set(emails) - found_emails
    if not_found_emails:
        raise HTTPException(status_code=404, detail=f"Users with emails {not_found_emails} not found")

    # Create UserLab instances for each user and the lab
    user_labs = []
    for user in users:
        user_lab = UserLab(user_id=user.user_id, lab_id=lab_id)
        session.add(user_lab)
        user_labs.append(user_lab)

    session.commit()
    return Message(message="Users added to lab successfully")

@router.delete("/{lab_id}/remove-user", response_model=Message)
def remove_users_from_lab(
    *, session: SessionDep, current_user: CurrentUser, lab_id: uuid.UUID, remove_user_in: RemoveUsersFromLab
) -> Any:
    """
    Remove users from a lab by providing a list of emails.
    """
    # Check if the current user is the owner of the lab
    lab = session.get(Lab, lab_id)
    if not lab:
        raise HTTPException(status_code=404, detail="Lab not found")
    if not current_user.is_superuser and (lab.owner_id != current_user.user_id):
        raise HTTPException(status_code=400, detail="Not enough permissions")

    # Find user by their emails
    emails = remove_user_in.emails
    user = session.exec(select(User).where(User.email.in_(emails))).all()

    # Check if user was found
    found_emails = {user.email for user in user}
    not_found_emails = set(emails) - found_emails
    if not_found_emails:
        raise HTTPException(status_code=404, detail=f"User with emails {not_found_emails} not found")

    # Find UserLab instances to delete
    user_labs_to_delete = session.exec(
        select(UserLab).where(
            UserLab.lab_id == lab_id,
            UserLab.user_id.in_([user.user_id for user in user])
        )
    ).all()

    if not user_labs_to_delete:
        raise HTTPException(status_code=404, detail="No matching UserLab instances found")

    # Delete UserLab instances
    for user_lab in user_labs_to_delete:
        session.delete(user_lab)

    session.commit()
    return Message(message="Users removed from lab successfully")

@router.get("/{lab_id}/users", response_model=list[User])
def view_lab_users(
    *, session: SessionDep, current_user: CurrentUser, lab_id: uuid.UUID
) -> Any:
    """
    View all users in a specific lab.
    """
    # Check if the current user is the owner of the lab or a superuser
    lab = session.get(Lab, lab_id)
    if not lab:
        raise HTTPException(status_code=404, detail="Lab not found")
    if not current_user.is_superuser and (lab.owner_id != current_user.user_id):
        raise HTTPException(status_code=400, detail="Not enough permissions")

    # Get all UserLab instances for the lab
    user_labs = session.exec(
        select(UserLab).where(
            UserLab.lab_id == lab_id
        )
    ).all()

    # Get the associated users
    user_ids = [user_lab.user_id for user_lab in user_labs]
    users = session.exec(
        select(User).where(
            User.user_id.in_(user_ids)
        )
    ).all()

    return users


