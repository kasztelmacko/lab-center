import uuid
from datetime import datetime, timedelta

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.config import settings
from app.tests.utils.item import create_random_item
from app.tests.utils.labs import create_random_lab
from app.tests.utils.borrows import create_random_borrow



def test_borrow_item(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    lab = create_random_lab(db)
    item = create_random_item(db, lab_id=lab.lab_id)
    start_date = datetime.now().isoformat()
    end_date = (datetime.now() + timedelta(days=7)).isoformat()
    data = {
        "start_date": start_date, 
        "end_date": end_date,
        "table_name": "table_name",
        "system_name": "system_name"
        }
    response = client.post(
        f"{settings.API_V1_STR}/labs/{lab.lab_id}/items/{item.item_id}/borrow",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["message"] == "Item borrowed successfully"


def test_borrow_item_not_found(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    lab = create_random_lab(db)
    start_date = datetime.now().isoformat()
    end_date = (datetime.now() + timedelta(days=7)).isoformat()
    data = {
        "start_date": start_date, 
        "end_date": end_date,
        "table_name": "table_name",
        "system_name": "system_name"
        }
    response = client.post(
        f"{settings.API_V1_STR}/labs/{lab.lab_id}/items/{uuid.uuid4()}/borrow",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Item not found"


def test_borrow_item_not_enough_permissions(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    lab = create_random_lab(db)
    item = create_random_item(db, lab_id=lab.lab_id)
    start_date = datetime.now().isoformat()
    end_date = (datetime.now() + timedelta(days=7)).isoformat()
    data = {
        "start_date": start_date, 
        "end_date": end_date,
        "table_name": "table_name",
        "system_name": "system_name"
        }
    response = client.post(
        f"{settings.API_V1_STR}/labs/{lab.lab_id}/items/{item.item_id}/borrow",
        headers=normal_user_token_headers,
        json=data,
    )
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "User is not a member of the lab"


def test_update_borrowing(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    lab = create_random_lab(db)
    item = create_random_item(db, lab_id=lab.lab_id)
    borrow = create_random_borrow(db)
    start_date = datetime.now().isoformat()
    end_date = (datetime.now() + timedelta(days=7)).isoformat()
    data = {
        "start_date": start_date, 
        "end_date": end_date,
        "table_name": "table_name",
        "system_name": "system_name"
        }
    response = client.post(
        f"{settings.API_V1_STR}/labs/{lab.lab_id}/items/{item.item_id}/borrow",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()

    new_end_date = (datetime.now() + timedelta(days=14)).isoformat()
    update_data = {
        "start_date": start_date, 
        "end_date": end_date,
        "table_name": "update table_name",
        "system_name": "update system_name"
        }
    response = client.put(
        f"{settings.API_V1_STR}/labs/{lab.lab_id}/items/{item.item_id}/borrow/{borrow.borrow_id}",
        headers=superuser_token_headers,
        json=update_data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["message"] == "Borrowing updated successfully"


def test_update_borrowing_not_found(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    lab = create_random_lab(db)
    item = create_random_item(db, lab_id=lab.lab_id)
    new_end_date = (datetime.now() + timedelta(days=14)).isoformat()
    update_data = {"end_date": new_end_date}
    response = client.put(
        f"{settings.API_V1_STR}/labs/{lab.lab_id}/items/{item.item_id}/borrow/{uuid.uuid4()}",
        headers=superuser_token_headers,
        json=update_data,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Borrowing not found"


def test_update_borrowing_not_enough_permissions(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    lab = create_random_lab(db)
    item = create_random_item(db, lab_id=lab.lab_id)
    borrow = create_random_borrow(db)
    start_date = datetime.now().isoformat()
    end_date = (datetime.now() + timedelta(days=7)).isoformat()
    data = {
        "start_date": start_date, 
        "end_date": end_date,
        "table_name": "table_name",
        "system_name": "system_name"
        }
    response = client.post(
        f"{settings.API_V1_STR}/labs/{lab.lab_id}/items/{item.item_id}/borrow",
        headers=normal_user_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()

    new_end_date = (datetime.now() + timedelta(days=14)).isoformat()
    update_data = {
        "start_date": start_date, 
        "end_date": end_date,
        "table_name": "update table_name",
        "system_name": "update system_name"
        }
    response = client.put(
        f"{settings.API_V1_STR}/labs/{lab.lab_id}/items/{item.item_id}/borrow/{borrow.borrow_id}",
        headers=normal_user_token_headers,
        json=update_data,
    )
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "User is not a member of the lab"


def test_delete_borrowing(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    lab = create_random_lab(db)
    item = create_random_item(db, lab_id=lab.lab_id)
    borrow = create_random_borrow(db)
    start_date = datetime.now().isoformat()
    end_date = (datetime.now() + timedelta(days=7)).isoformat()
    data = {
        "start_date": start_date, 
        "end_date": end_date,
        "table_name": "table_name",
        "system_name": "system_name"
        }
    response = client.post(
        f"{settings.API_V1_STR}/labs/{lab.lab_id}/items/{item.item_id}/borrow",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()

    response = client.delete(
        f"{settings.API_V1_STR}/labs/{lab.lab_id}/items/{item.item_id}/borrow/{borrow.borrow_id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["message"] == "Borrowing deleted successfully"


def test_delete_borrowing_not_found(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    lab = create_random_lab(db)
    item = create_random_item(db, lab_id=lab.lab_id)
    response = client.delete(
        f"{settings.API_V1_STR}/labs/{lab.lab_id}/items/{item.item_id}/borrow/{uuid.uuid4()}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Borrowing not found"


def test_delete_borrowing_not_enough_permissions(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    lab = create_random_lab(db)
    item = create_random_item(db, lab_id=lab.lab_id)
    borrow = create_random_borrow(db)
    start_date = datetime.now().isoformat()
    end_date = (datetime.now() + timedelta(days=7)).isoformat()
    data = {"start_date": start_date, "end_date": end_date}
    response = client.post(
        f"{settings.API_V1_STR}/labs/{lab.lab_id}/items/{item.item_id}/borrow",
        headers=normal_user_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()

    response = client.delete(
        f"{settings.API_V1_STR}/labs/{lab.lab_id}/items/{item.item_id}/borrow/{borrow.borrow_id}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "User is not a member of the lab"


def test_view_all_borrowings(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    lab = create_random_lab(db)
    item = create_random_item(db, lab_id=lab.lab_id)
    data = create_random_borrow(db)
    response = client.post(
        f"{settings.API_V1_STR}/labs/{lab.lab_id}/items/{item.item_id}/borrow",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200

    response = client.get(
        f"{settings.API_V1_STR}/labs/{lab.lab_id}/items/{item.item_id}/borrows",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert len(content) >= 1


def test_view_all_borrowings_not_found(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    lab = create_random_lab(db)
    response = client.get(
        f"{settings.API_V1_STR}/labs/{lab.lab_id}/items/{uuid.uuid4()}/borrows",
        headers=superuser_token_headers,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Item not found"


def test_view_all_borrowings_not_enough_permissions(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    lab = create_random_lab(db)
    item = create_random_item(db, lab_id=lab.lab_id)
    response = client.get(
        f"{settings.API_V1_STR}/labs/{lab.lab_id}/items/{item.item_id}/borrows",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "User is not a member of the lab"


def test_view_borrowing(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    lab = create_random_lab(db)
    item = create_random_item(db, lab_id=lab.lab_id)
    data = create_random_borrow(db)
    response = client.post(
        f"{settings.API_V1_STR}/labs/{lab.lab_id}/items/{item.item_id}/borrow",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()

    response = client.get(
        f"{settings.API_V1_STR}/labs/{lab.lab_id}/items/{item.item_id}/borrow/{data.borrow_id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["borrow_id"] == data.borrow_id


def test_view_borrowing_not_found(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    lab = create_random_lab(db)
    item = create_random_item(db, lab_id=lab.lab_id)
    response = client.get(
        f"{settings.API_V1_STR}/labs/{lab.lab_id}/items/{item.item_id}/borrow/{uuid.uuid4()}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Borrowing not found"


def test_view_borrowing_not_enough_permissions(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    lab = create_random_lab(db)
    item = create_random_item(db, lab_id=lab.lab_id)
    data = create_random_borrow(db)
    response = client.post(
        f"{settings.API_V1_STR}/labs/{lab.lab_id}/items/{item.item_id}/borrow",
        headers=normal_user_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()

    response = client.get(
        f"{settings.API_V1_STR}/labs/{lab.lab_id}/items/{item.item_id}/borrow/{data.borrow_id}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "User is not a member of the lab"