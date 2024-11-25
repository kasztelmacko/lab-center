import uuid

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.config import settings
from app.tests.utils import create_random_user
from app.tests.utils.labs import create_random_lab


def test_create_lab(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    data = {"lab_name": "Foo Lab", "description": "A test lab"}
    response = client.post(
        f"{settings.API_V1_STR}/labs/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["lab_name"] == data["lab_name"]
    assert content["description"] == data["description"]
    assert "lab_id" in content


def test_read_lab(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    lab = create_random_lab(db)
    response = client.get(
        f"{settings.API_V1_STR}/labs/{lab.lab_id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["lab_name"] == lab.lab_name
    assert content["description"] == lab.description
    assert content["lab_id"] == str(lab.lab_id)


def test_read_lab_not_found(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    response = client.get(
        f"{settings.API_V1_STR}/labs/{uuid.uuid4()}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Lab not found"


def test_read_lab_not_enough_permissions(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    lab = create_random_lab(db)
    response = client.get(
        f"{settings.API_V1_STR}/labs/{lab.lab_id}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Not enough permissions"


def test_read_labs(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    create_random_lab(db)
    create_random_lab(db)
    response = client.get(
        f"{settings.API_V1_STR}/labs/",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["count"] >= 2


def test_update_lab(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    lab = create_random_lab(db)
    data = {"lab_name": "Updated Lab", "description": "Updated description"}
    response = client.put(
        f"{settings.API_V1_STR}/labs/{lab.lab_id}",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["lab_name"] == data["lab_name"]
    assert content["description"] == data["description"]
    assert content["lab_id"] == str(lab.lab_id)


def test_update_lab_not_found(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    data = {"lab_name": "Updated Lab", "description": "Updated description"}
    response = client.put(
        f"{settings.API_V1_STR}/labs/{uuid.uuid4()}",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Lab not found"


def test_update_lab_not_enough_permissions(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    lab = create_random_lab(db)
    data = {"lab_name": "Updated Lab", "description": "Updated description"}
    response = client.put(
        f"{settings.API_V1_STR}/labs/{lab.lab_id}",
        headers=normal_user_token_headers,
        json=data,
    )
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Not enough permissions"


def test_delete_lab(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    lab = create_random_lab(db)
    response = client.delete(
        f"{settings.API_V1_STR}/labs/{lab.lab_id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["message"] == "Lab deleted successfully"


def test_delete_lab_not_found(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    response = client.delete(
        f"{settings.API_V1_STR}/labs/{uuid.uuid4()}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Lab not found"


def test_delete_lab_not_enough_permissions(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    lab = create_random_lab(db)
    response = client.delete(
        f"{settings.API_V1_STR}/labs/{lab.lab_id}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Not enough permissions"


def test_add_users_to_lab(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    lab = create_random_lab(db)
    user = create_random_user(db)
    data = {"emails": [user.email]}
    response = client.post(
        f"{settings.API_V1_STR}/labs/{lab.lab_id}/add-users",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["message"] == "Users added to lab successfully"


def test_add_users_to_lab_not_found(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    user = create_random_user(db)
    data = {"emails": [user.email]}
    response = client.post(
        f"{settings.API_V1_STR}/labs/{uuid.uuid4()}/add-users",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Lab not found"


def test_add_users_to_lab_not_enough_permissions(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    lab = create_random_lab(db)
    user = create_random_user(db)
    data = {"emails": [user.email]}
    response = client.post(
        f"{settings.API_V1_STR}/labs/{lab.lab_id}/add-users",
        headers=normal_user_token_headers,
        json=data,
    )
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Not enough permissions"


def test_remove_users_from_lab(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    lab = create_random_lab(db)
    user = create_random_user(db)
    data = {"emails": [user.email]}
    client.post(
        f"{settings.API_V1_STR}/labs/{lab.lab_id}/add-users",
        headers=superuser_token_headers,
        json=data,
    )
    response = client.delete(
        f"{settings.API_V1_STR}/labs/{lab.lab_id}/remove-user",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["message"] == "Users removed from lab successfully"


def test_remove_users_from_lab_not_found(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    user = create_random_user(db)
    data = {"emails": [user.email]}
    response = client.delete(
        f"{settings.API_V1_STR}/labs/{uuid.uuid4()}/remove-user",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Lab not found"


def test_remove_users_from_lab_not_enough_permissions(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    lab = create_random_lab(db)
    user = create_random_user(db)
    data = {"emails": [user.email]}
    response = client.delete(
        f"{settings.API_V1_STR}/labs/{lab.lab_id}/remove-user",
        headers=normal_user_token_headers,
        json=data,
    )
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Not enough permissions"


def test_view_lab_users(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    lab = create_random_lab(db)
    user = create_random_user(db)
    data = {"emails": [user.email]}
    client.post(
        f"{settings.API_V1_STR}/labs/{lab.lab_id}/add-users",
        headers=superuser_token_headers,
        json=data,
    )
    response = client.get(
        f"{settings.API_V1_STR}/labs/{lab.lab_id}/users",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert len(content) == 1
    assert content[0]["email"] == user.email


def test_view_lab_users_not_found(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    response = client.get(
        f"{settings.API_V1_STR}/labs/{uuid.uuid4()}/users",
        headers=superuser_token_headers,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Lab not found"


def test_view_lab_users_not_enough_permissions(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    lab = create_random_lab(db)
    response = client.get(
        f"{settings.API_V1_STR}/labs/{lab.lab_id}/users",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Not enough permissions"