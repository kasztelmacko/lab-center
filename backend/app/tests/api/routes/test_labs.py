import uuid

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.config import settings
from app.tests.utils.user import create_random_user
from app.tests.utils.labs import create_random_lab


def test_create_lab(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    data = {
        "lab_place": "Test Lab",
        "lab_university": "Test University",
        "lab_num": "Test Number",
    }
    response = client.post(
        f"{settings.API_V1_STR}/labs/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["lab_place"] == data["lab_place"]
    assert content["lab_university"] == data["lab_university"]
    assert content["lab_num"] == data["lab_num"]
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
    assert content["lab_place"] == lab.lab_place
    assert content["lab_university"] == lab.lab_university
    assert content["lab_num"] == lab.lab_num
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
    data = {
        "lab_place": "Update Test Lab",
        "lab_university": "Update Test University",
        "lab_num": "Update Test Number",
    }
    response = client.put(
        f"{settings.API_V1_STR}/labs/{lab.lab_id}",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["lab_place"] == data["lab_place"]
    assert content["lab_university"] == data["lab_university"]
    assert content["lab_num"] == data["lab_num"]
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
    data = {
        "lab_place": "Update Test Lab",
        "lab_university": "Update Test University",
        "lab_num": "Update Test Number",
    }
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
    
    # Add the user to the lab first
    add_data = {"emails": [user.email]}
    client.post(
        f"{settings.API_V1_STR}/labs/{lab.lab_id}/add-users",
        headers=superuser_token_headers,
        json=add_data,
    )
    
    # Now remove the user from the lab
    response = client.delete(
        f"{settings.API_V1_STR}/labs/{lab.lab_id}/users/{user.user_id}/remove-user",
        headers=superuser_token_headers,
    )
    
    assert response.status_code == 200
    content = response.json()
    assert content["message"] == "User removed from lab successfully"


def test_remove_users_from_lab_not_found(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    user = create_random_user(db)
    random_lab_id = uuid.uuid4()
    
    response = client.delete(
        f"{settings.API_V1_STR}/labs/{random_lab_id}/users/{user.user_id}/remove-user",
        headers=superuser_token_headers,
    )
    
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Lab not found"


def test_remove_users_from_lab_not_enough_permissions(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    lab = create_random_lab(db)
    user = create_random_user(db)
    
    # Add the user to the lab first
    add_data = {"emails": [user.email]}
    client.post(
        f"{settings.API_V1_STR}/labs/{lab.lab_id}/add-users",
        headers=normal_user_token_headers,
        json=add_data,
    )
    
    # Now attempt to remove the user from the lab with normal user permissions
    response = client.delete(
        f"{settings.API_V1_STR}/labs/{lab.lab_id}/users/{user.user_id}/remove-user",
        headers=normal_user_token_headers,
    )
    
    assert response.status_code == 403
    content = response.json()
    assert content["detail"] == "Not enough permissions"


def test_view_lab_users(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    # Create a random lab and users
    lab = create_random_lab(db)
    users = [create_random_user(db) for _ in range(3)]
    
    # Add users to the lab
    for user in users:
        add_data = {"emails": [user.email]}
        client.post(
            f"{settings.API_V1_STR}/labs/{lab.lab_id}/add-users",
            headers=superuser_token_headers,
            json=add_data,
        )
    
    # View lab users
    response = client.get(
        f"{settings.API_V1_STR}/labs/{lab.lab_id}/users",
        headers=superuser_token_headers,
    )
    
    assert response.status_code == 200
    content = response.json()
    
    # Check if the response contains the correct number of users
    assert len(content) == len(users)
    
    # Check if the response contains the correct user details
    for user in content:
        assert "user_id" in user
        assert "email" in user
        assert "can_edit_lab" in user
        assert "can_edit_items" in user
        assert "can_edit_users" in user

def test_view_lab_users_not_enough_permissions(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    # Create a random lab and users
    lab = create_random_lab(db)
    users = [create_random_user(db) for _ in range(3)]
    
    # Add users to the lab
    for user in users:
        add_data = {"emails": [user.email]}
        client.post(
            f"{settings.API_V1_STR}/labs/{lab.lab_id}/add-users",
            headers=normal_user_token_headers,
            json=add_data,
        )
    
    # View lab users with normal user permissions
    response = client.get(
        f"{settings.API_V1_STR}/labs/{lab.lab_id}/users",
        headers=normal_user_token_headers,
    )
    
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Not enough permissions"

def test_view_lab_users_lab_not_found(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    # Generate a random lab ID that does not exist
    random_lab_id = uuid.uuid4()
    
    # View lab users for a non-existent lab
    response = client.get(
        f"{settings.API_V1_STR}/labs/{random_lab_id}/users",
        headers=superuser_token_headers,
    )
    
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Lab not found"