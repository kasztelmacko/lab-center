from sqlmodel import Session

from app import crud
from app.models import Item, ItemCreate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string, random_int


def create_random_item(db: Session) -> Item:
    user = create_random_user(db)
    owner_id = user.id
    assert owner_id is not None
    item_name = random_lower_string()
    quantity = random_int()
    item_in = ItemCreate(item_name=item_name, quantity=quantity)
    return crud.create_item(session=db, item_in=item_in, owner_id=owner_id)
