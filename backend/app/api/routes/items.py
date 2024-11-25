import uuid
from typing import Any

from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import func, select

from app.api.deps import CurrentUser, SessionDep
from app.models import (Item, 
                        ItemCreate, 
                        ItemPublic, 
                        ItemsPublic, 
                        ItemUpdate, 
                        Message,
                        Lab,
                        UserLab)

router = APIRouter()


@router.get("/{lab_id}/items", response_model=ItemsPublic)
def read_items(
    lab_id: uuid.UUID, session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve items for a specific lab.
    """

    # Check if the current user is the owner of the lab or has can_edit_items permission
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
        
        if not user_lab or not user_lab.can_edit_items:
            raise HTTPException(status_code=400, detail="Not enough permissions")

    # Retrieve all items for the lab
    count_statement = select(func.count()).select_from(Item).where(Item.lab_id == lab_id)
    count = session.exec(count_statement).one()
    statement = select(Item).where(Item.lab_id == lab_id).offset(skip).limit(limit)
    items = session.exec(statement).all()

    return ItemsPublic(data=items, count=count)


@router.get("/{lab_id}/items/{item_id}", response_model=ItemPublic)
def read_item(
    lab_id: uuid.UUID, session: SessionDep, current_user: CurrentUser, item_id: uuid.UUID
) -> Any:
    """
    Get item by ID for a specific lab.
    """
    item = session.get(Item, item_id)
    if not item or item.lab_id != lab_id:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Check if the current user is associated with the lab
    user_lab = session.exec(
        select(UserLab).where(
            UserLab.lab_id == lab_id,
            UserLab.user_id == current_user.user_id
        )
    ).first()
    
    if not user_lab:
        raise HTTPException(status_code=400, detail="Not enough permissions")

    return item


@router.post("/{lab_id}/items", response_model=ItemPublic)
def create_item(
    lab_id: uuid.UUID, session: SessionDep, current_user: CurrentUser, item_in: ItemCreate
) -> Any:
    """
    Create new item for a specific lab.
    """
    # Check if the current user is the owner of the lab or has can_edit_items permission
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
        
        if not user_lab or not user_lab.can_edit_items:
            raise HTTPException(status_code=400, detail="Not enough permissions")

    item = Item.model_validate(item_in, update={"owner_id": current_user.user_id, "lab_id": lab_id})
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@router.put("/{lab_id}/items/{item_id}", response_model=ItemPublic)
def update_item(
    lab_id: uuid.UUID,
    session: SessionDep,
    current_user: CurrentUser,
    item_id: uuid.UUID,
    item_in: ItemUpdate,
) -> Any:
    """
    Update an item for a specific lab.
    """
    item = session.get(Item, item_id)
    if not item or item.lab_id != lab_id:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Check if the current user is the owner of the lab or has can_edit_items permission
    if not current_user.is_superuser:
        user_lab = session.exec(
            select(UserLab).where(
                UserLab.lab_id == lab_id,
                UserLab.user_id == current_user.user_id
            )
        ).first()
        
        if not user_lab or not user_lab.can_edit_items:
            raise HTTPException(status_code=400, detail="Not enough permissions")

    update_dict = item_in.model_dump(exclude_unset=True)
    item.sqlmodel_update(update_dict)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@router.delete("/{lab_id}/items/{item_id}")
def delete_item(
    lab_id: uuid.UUID, session: SessionDep, current_user: CurrentUser, item_id: uuid.UUID
) -> Message:
    """
    Delete an item for a specific lab.
    """
    item = session.get(Item, item_id)
    if not item or item.lab_id != lab_id:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Check if the current user is the owner of the lab or has can_edit_items permission
    if not current_user.is_superuser:
        user_lab = session.exec(
            select(UserLab).where(
                UserLab.lab_id == lab_id,
                UserLab.user_id == current_user.user_id
            )
        ).first()
        
        if not user_lab or not user_lab.can_edit_items:
            raise HTTPException(status_code=400, detail="Not enough permissions")

    session.delete(item)
    session.commit()
    return Message(message="Item deleted successfully")
