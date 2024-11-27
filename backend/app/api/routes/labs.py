import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select, delete, col

from app.api.deps import CurrentUser, SessionDep
from app.models import (Lab, LabCreate, LabPublic, LabsPublic, LabUpdate, 
                        UserLab, AddUsersToLab, RemoveUsersFromLab, UpdateUserLab,
                        User,
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

    print(lab)

    # Create a new UserLab entry
    user_lab = UserLab(
        user_id=current_user.user_id,
        lab_id=lab.lab_id,
        can_edit_lab=True,
        can_edit_items=True,
        can_edit_users=True
    )

    print(user_lab)

    session.add(user_lab)
    session.commit()
    session.refresh(user_lab)

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
    
    if not current_user.is_superuser:
        user_lab = session.exec(
            select(UserLab).where(
                UserLab.lab_id == lab.lab_id,
                UserLab.user_id == current_user.user_id
            )
        ).first()

        print(user_lab)
        
        if not user_lab or not user_lab.can_edit_lab:
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
    
    if not current_user.is_superuser:
        user_lab = session.exec(
            select(UserLab).where(
                UserLab.lab_id == lab.lab_id,
                UserLab.user_id == current_user.user_id
            )
        ).first()

        if not user_lab or not user_lab.can_edit_lab:
            raise HTTPException(status_code=400, detail="Not enough permissions")
    
    # Delete the lab
    statement = delete(UserLab).where(col(UserLab.lab_id) == lab.lab_id)
    session.exec(statement)
    session.delete(lab)
    session.commit()
    
    return Message(message="Lab deleted successfully")

@router.post("/{lab_id}/add-users", response_model=Message)
def add_users_to_lab(
    *, session: SessionDep, current_user: CurrentUser, lab_id: uuid.UUID, add_users_in: AddUsersToLab
) -> Any:
    """
    Add users to a lab by providing a list of emails and their permissions.
    """
    # Check if the current user is the owner of the lab or has can_edit_users permission
    lab = session.get(Lab, lab_id)
    if not lab:
        raise HTTPException(status_code=404, detail="Lab not found")
    
    if not current_user.is_superuser:
        user_lab = session.exec(
            select(UserLab).where(
                UserLab.lab_id == lab_id,
                UserLab.user_id == current_user.user_id
            )
        ).first()
        
        if not user_lab or not user_lab.can_edit_users:
            raise HTTPException(status_code=400, detail="Not enough permissions")

    # Find users by their emails
    emails = add_users_in.emails
    users = session.exec(select(User).where(User.email.in_(emails))).all()

    # Check if all users were found
    found_emails = {user.email for user in users}
    not_found_emails = set(emails) - found_emails
    if not_found_emails:
        raise HTTPException(status_code=404, detail=f"Users with emails {not_found_emails} not found")

    # Create UserLab instances for each user and the lab with specified permissions
    user_labs = []
    for user in users:
        user_lab = UserLab(
            user_id=user.user_id,
            lab_id=lab_id,
            can_edit_lab=add_users_in.can_edit_lab,
            can_edit_items=add_users_in.can_edit_items,
            can_edit_users=add_users_in.can_edit_users
        )
        session.add(user_lab)
        user_labs.append(user_lab)

    session.commit()
    return Message(message="Users added to lab successfully with specified permissions")

@router.get("/{lab_id}/users", response_model=list[User])
def view_lab_users(
    *, session: SessionDep, current_user: CurrentUser, lab_id: uuid.UUID
) -> Any:
    """
    View all users in a specific lab with their permissions.
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

    # Include permissions in the response
    users_with_permissions = []
    for user in users:
        user_lab = next((ul for ul in user_labs if ul.user_id == user.user_id), None)
        if user_lab:
            user_with_permissions = user.copy()
            user_with_permissions.can_edit_lab = user_lab.can_edit_lab
            user_with_permissions.can_edit_items = user_lab.can_edit_items
            user_with_permissions.can_edit_users = user_lab.can_edit_users
            users_with_permissions.append(user_with_permissions)

    return users_with_permissions

@router.get("/{lab_id}/users/{user_id}", response_model=User)
def view_user_in_lab(
    *, session: SessionDep, current_user: CurrentUser, lab_id: uuid.UUID, user_id: uuid.UUID
) -> Any:
    """
    View a specific user in a lab.
    """
    # Check if the current user is part of the lab
    lab = session.get(Lab, lab_id)
    if not lab:
        raise HTTPException(status_code=404, detail="Lab not found")

    # Check if the current user is part of the lab
    current_user_lab = session.exec(
        select(UserLab).where(
            UserLab.lab_id == lab_id,
            UserLab.user_id == current_user.user_id
        )
    ).first()

    if not current_user_lab:
        raise HTTPException(status_code=403, detail="You are not part of this lab")

    # Find the user by their user ID
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")

    # Check if the user is part of the lab
    user_lab = session.exec(
        select(UserLab).where(
            UserLab.lab_id == lab_id,
            UserLab.user_id == user.user_id
        )
    ).first()

    if not user_lab:
        raise HTTPException(status_code=404, detail=f"User with ID {user.user_id} is not associated with this lab")

    # Include permissions in the response
    user_with_permissions = user.copy()
    user_with_permissions.can_edit_lab = user_lab.can_edit_lab
    user_with_permissions.can_edit_items = user_lab.can_edit_items
    user_with_permissions.can_edit_users = user_lab.can_edit_users

    return user_with_permissions


@router.delete("/{lab_id}/users/{user_id}/remove-user", response_model=Message)
def remove_users_from_lab(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    lab_id: uuid.UUID,
    user_id: uuid.UUID
) -> Any:
    """
    Remove a user from a lab by providing the user ID.
    """
    # Check if the current user is the owner of the lab or has can_edit_users permission
    lab = session.get(Lab, lab_id)
    if not lab:
        raise HTTPException(status_code=404, detail="Lab not found")
    
    if not current_user.is_superuser:
        user_lab = session.exec(
            select(UserLab).where(
                UserLab.lab_id == lab_id,
                UserLab.user_id == current_user.user_id
            )
        ).first()
        
        if not user_lab or not user_lab.can_edit_users:
            raise HTTPException(status_code=403, detail="Not enough permissions")

    # Find the user by their user ID
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")

    # Find UserLab instance to delete
    user_lab_to_delete = session.exec(
        select(UserLab).where(
            UserLab.lab_id == lab_id,
            UserLab.user_id == user.user_id
        )
    ).first()

    if not user_lab_to_delete:
        raise HTTPException(status_code=404, detail=f"User with ID {user.user_id} is not associated with this lab")

    # Delete UserLab instance
    session.delete(user_lab_to_delete)

    session.commit()
    return Message(message="User removed from lab successfully")

@router.put("/{lab_id}/users/{user_id}/update-user-permissions", response_model=Message)
def update_user_permissions(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    lab_id: uuid.UUID,
    user_id: uuid.UUID,
    update_permissions_in: UpdateUserLab
) -> Any:
    """
    Update user permissions in a lab by providing a list of user IDs and their new permissions.
    """
    # Check if the current user is the owner of the lab or has can_edit_users permission
    lab = session.get(Lab, lab_id)
    if not lab:
        raise HTTPException(status_code=404, detail="Lab not found")
    
    if not current_user.is_superuser:
        user_lab = session.exec(
            select(UserLab).where(
                UserLab.lab_id == lab_id,
                UserLab.user_id == current_user.user_id
            )
        ).first()
        
        if not user_lab or not user_lab.can_edit_users:
            raise HTTPException(status_code=403, detail="Not enough permissions")

    # Find the user by their user ID
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")

    # Update UserLab instance for the user and the lab with new permissions
    user_lab = session.exec(
        select(UserLab).where(
            UserLab.lab_id == lab_id,
            UserLab.user_id == user.user_id
        )
    ).first()
    
    if not user_lab:
        raise HTTPException(status_code=404, detail=f"User with ID {user.user_id} is not associated with this lab")
    
    user_lab.can_edit_lab = update_permissions_in.can_edit_lab
    user_lab.can_edit_items = update_permissions_in.can_edit_items
    user_lab.can_edit_users = update_permissions_in.can_edit_users
    session.add(user_lab)

    session.commit()
    return Message(message="User permissions updated successfully")
