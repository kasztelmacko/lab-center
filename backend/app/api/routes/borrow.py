import uuid
from typing import Any
from datetime import datetime

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app.api.deps import CurrentUser, SessionDep
from app.models import Borrowing, BorrowItem, UserLab, Lab, Item, Message

router = APIRouter()

@router.post("/{lab_id}/items/{item_id}/borrow", response_model=Message)
def borrow_item(
    *, session: SessionDep, current_user: CurrentUser, lab_id: uuid.UUID, item_id: uuid.UUID, borrow_item_in: BorrowItem
) -> Any:
    """
    Borrow an item from a lab by providing the start and end dates.
    """
    # Check if the current user is a member of the lab
    lab = session.get(Lab, lab_id)
    if not lab:
        raise HTTPException(status_code=404, detail="Lab not found")
    
    # Check if the user is a member of the lab
    user_lab = session.exec(
        select(UserLab).where(
            UserLab.lab_id == lab_id,
            UserLab.user_id == current_user.id
        )
    ).first()
    if not user_lab:
        raise HTTPException(status_code=400, detail="User is not a member of the lab")

    # Check if the item exists in the lab
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    # Check if the item is available for the given dates
    existing_borrowings = session.exec(
        select(Borrowing).where(
            Borrowing.item_id == item_id,
            Borrowing.returned_at.is_(None)
        )
    ).all()

    start_date = datetime.fromisoformat(borrow_item_in.start_date)
    end_date = datetime.fromisoformat(borrow_item_in.end_date)

    for borrowing in existing_borrowings:
        borrowed_at = datetime.fromisoformat(borrowing.borrowed_at)
        if start_date <= borrowed_at <= end_date:
            raise HTTPException(status_code=400, detail="Item is already borrowed during the requested period")

    # Create a new Borrowing instance
    borrowing = Borrowing(
        user_id=current_user.id,
        item_id=item_id,
        borrowed_at=start_date.isoformat(),
        returned_at=end_date.isoformat()
    )
    session.add(borrowing)
    session.commit()

    return Message(message="Item borrowed successfully")

@router.put("/{lab_id}/items/{item_id}/borrow/{borrow_id}", response_model=Message)
def update_borrowing(
    *, session: SessionDep, current_user: CurrentUser, lab_id: uuid.UUID, item_id: uuid.UUID, borrow_id: uuid.UUID, update_borrow_in: BorrowItem
) -> Any:
    """
    Update the return date of a borrowing.
    """
    # Check if the current user is a member of the lab
    lab = session.get(Lab, lab_id)
    if not lab:
        raise HTTPException(status_code=404, detail="Lab not found")
    
    # Check if the user is a member of the lab
    user_lab = session.exec(
        select(UserLab).where(
            UserLab.lab_id == lab_id,
            UserLab.user_id == current_user.id
        )
    ).first()
    if not user_lab:
        raise HTTPException(status_code=400, detail="User is not a member of the lab")

    # Check if the item exists in the lab
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    # Check if the borrowing exists
    borrowing = session.get(Borrowing, borrow_id)
    if not borrowing:
        raise HTTPException(status_code=404, detail="Borrowing not found")

    # Update the return date
    end_date = datetime.fromisoformat(update_borrow_in.end_date)
    borrowing.returned_at = end_date.isoformat()
    session.add(borrowing)
    session.commit()

    return Message(message="Borrowing updated successfully")

@router.delete("/{lab_id}/items/{item_id}/borrow/{borrow_id}", response_model=Message)
def delete_borrowing(
    *, session: SessionDep, current_user: CurrentUser, lab_id: uuid.UUID, item_id: uuid.UUID, borrow_id: uuid.UUID
) -> Any:
    """
    Delete a borrowing.
    """
    # Check if the current user is a member of the lab
    lab = session.get(Lab, lab_id)
    if not lab:
        raise HTTPException(status_code=404, detail="Lab not found")
    
    # Check if the user is a member of the lab
    user_lab = session.exec(
        select(UserLab).where(
            UserLab.lab_id == lab_id,
            UserLab.user_id == current_user.id
        )
    ).first()
    if not user_lab:
        raise HTTPException(status_code=400, detail="User is not a member of the lab")

    # Check if the item exists in the lab
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    # Check if the borrowing exists
    borrowing = session.get(Borrowing, borrow_id)
    if not borrowing:
        raise HTTPException(status_code=404, detail="Borrowing not found")

    # Delete the borrowing
    session.delete(borrowing)
    session.commit()

    return Message(message="Borrowing deleted successfully")

@router.get("/{lab_id}/items/{item_id}/borrows", response_model=list[Borrowing])
def view_all_borrowings(
    *, session: SessionDep, current_user: CurrentUser, lab_id: uuid.UUID, item_id: uuid.UUID
) -> Any:
    """
    View all borrowings for a specific lab and item.
    """
    # Check if the current user is a member of the lab
    lab = session.get(Lab, lab_id)
    if not lab:
        raise HTTPException(status_code=404, detail="Lab not found")
    
    # Check if the user is a member of the lab
    user_lab = session.exec(
        select(UserLab).where(
            UserLab.lab_id == lab_id,
            UserLab.user_id == current_user.id
        )
    ).first()
    if not user_lab:
        raise HTTPException(status_code=400, detail="User is not a member of the lab")

    # Check if the item exists in the lab
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    # Get all borrowings for the item
    borrowings = session.exec(
        select(Borrowing).where(
            Borrowing.item_id == item_id
        )
    ).all()

    return borrowings

@router.get("/{lab_id}/items/{item_id}/borrow/{borrow_id}", response_model=Borrowing)
def view_borrowing(
    *, session: SessionDep, current_user: CurrentUser, lab_id: uuid.UUID, item_id: uuid.UUID, borrow_id: uuid.UUID
) -> Any:
    """
    View details of a specific borrowing.
    """
    # Check if the current user is a member of the lab
    lab = session.get(Lab, lab_id)
    if not lab:
        raise HTTPException(status_code=404, detail="Lab not found")
    
    # Check if the user is a member of the lab
    user_lab = session.exec(
        select(UserLab).where(
            UserLab.lab_id == lab_id,
            UserLab.user_id == current_user.id
        )
    ).first()
    if not user_lab:
        raise HTTPException(status_code=400, detail="User is not a member of the lab")

    # Check if the item exists in the lab
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    # Check if the borrowing exists
    borrowing = session.get(Borrowing, borrow_id)
    if not borrowing:
        raise HTTPException(status_code=404, detail="Borrowing not found")

    return borrowing