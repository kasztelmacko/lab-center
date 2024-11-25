import uuid

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.config import settings
from app.tests.utils.item import create_random_item
from app.tests.utils.labs import create_random_lab


def test_create_item(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    lab = create_random_lab(db)  # Ensure you have this function defined
    data = {"item_name": "Foo", "quantity": 3}
    response = client.post(
        f"{settings.API_V1_STR}/labs/{lab.lab_id}/items",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["item_name"] == data["item_name"]
    assert content["quantity"] == data["quantity"]
    assert "item_id" in content
    assert "lab_id" in content
    assert content["lab_id"] == str(lab.lab_id)


def test_read_item(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    lab = create_random_lab(db)
    item = create_random_item(db)
    response = client.get(
        f"{settings.API_V1_STR}/labs/{lab.lab_id}/items/{item.item_id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["item_name"] == item.item_name
    assert content["quantity"] == item.quantity
    assert content["item_id"] == str(item.item_id)
    assert content["lab_id"] == str(item.lab_id)


def test_read_item_not_found(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    lab = create_random_lab(db)
    response = client.get(
        f"{settings.API_V1_STR}/labs/{lab.lab_id}/items/{uuid.uuid4()}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Item not found"


def test_read_item_not_enough_permissions(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    lab = create_random_lab(db)
    item = create_random_item(db)
    response = client.get(
        f"{settings.API_V1_STR}/labs/{lab.lab_id}/items/{item.item_id}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Not enough permissions"


def test_read_items(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    lab = create_random_lab(db)
    create_random_item(db)
    create_random_item(db)
    response = client.get(
        f"{settings.API_V1_STR}/labs/{lab.lab_id}/items/",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert len(content["data"]) >= 2


def test_update_item(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    lab = create_random_lab(db)
    item = create_random_item(db)
    data = {"item_name": "Updated title", "quantity": 6}
    response = client.put(
        f"{settings.API_V1_STR}/labs/{lab.lab_id}/items/{item.item_id}",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["item_name"] == data["item_name"]
    assert content["quantity"] == data["quantity"]
    assert content["item_id"] == str(item.item_id)
    assert content["lab_id"] == str(item.lab_id)


def test_update_item_not_found(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    lab = create_random_lab(db)
    data = {"item_name": "Updated title", "quantity": 6}
    response = client.put(
        f"{settings.API_V1_STR}/labs/{lab.lab_id}/items/{uuid.uuid4()}",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Item not found"


def test_update_item_not_enough_permissions(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    lab = create_random_lab(db)
    item = create_random_item(db)
    data = {"item_name": "Updated title", "quantity": 6}
    response = client.put(
        f"{settings.API_V1_STR}/labs/{lab.lab_id}/items/{item.item_id}",
        headers=normal_user_token_headers,
        json=data,
    )
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Not enough permissions"


def test_delete_item(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    lab = create_random_lab(db)
    item = create_random_item(db)
    response = client.delete(
        f"{settings.API_V1_STR}/labs/{lab.lab_id}/items/{item.item_id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["message"] == "Item deleted successfully"


def test_delete_item_not_found(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    lab = create_random_lab(db)
    response = client.delete(
        f"{settings.API_V1_STR}/labs/{lab.lab_id}/items/{uuid.uuid4()}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Item not found"


def test_delete_item_not_enough_permissions(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    lab = create_random_lab(db)
    item = create_random_item(db)
    response = client.delete(
        f"{settings.API_V1_STR}/labs/{lab.lab_id}/items/{item.item_id}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Not enough permissions"
    