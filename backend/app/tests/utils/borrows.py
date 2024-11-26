from sqlmodel import Session
from datetime import datetime, timedelta


from app import crud
from app.models import Borrowing, BorrowCreate
from app.tests.utils.user import create_random_user
from app.tests.utils.labs import create_random_lab
from app.tests.utils.item import create_random_item
from app.tests.utils.utils import random_lower_string


def create_random_borrow(db: Session) -> Borrowing:
    user = create_random_user(db)
    item = create_random_item(db)
    lab = create_random_lab(db)
    borrowed_at = datetime.now().isoformat()
    returned_at = (datetime.now() + timedelta(days=7)).isoformat()
    table_name = random_lower_string()
    system_name = random_lower_string()

    borrow_item_in = BorrowCreate(
        start_date=borrowed_at,
        end_date=returned_at,
        table_name=table_name,
        system_name=system_name,
    )

    lab_id = lab.lab_id
    user_id = user.user_id
    item_id = item.item_id

    return crud.create_borrow(session=db, borrow_in=borrow_item_in, lab_id=lab_id, user_id=user_id, item_id=item_id)
