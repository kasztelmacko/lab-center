from sqlmodel import Session

from app import crud
from app.models import Item, ItemCreate
from app.tests.utils.user import create_random_user
from app.tests.utils.labs import create_random_lab
from app.tests.utils.utils import random_lower_string, random_int


def create_random_item(db: Session) -> Item:
    user = create_random_user(db)
    lab = create_random_lab(db)
    owner_id = user.user_id
    assert owner_id is not None
    item_name = random_lower_string()
    quantity = random_int()
    item_img_url = random_lower_string()
    item_vendor = random_lower_string()
    item_params = random_lower_string()
    item_in = ItemCreate(item_name=item_name, quantity=quantity, item_img_url=item_img_url, item_vendor=item_vendor, item_params=item_params)

    lab_id = lab.lab_id

    return crud.create_item(session=db, item_in=item_in, lab_id=lab_id, owner_id=owner_id)
