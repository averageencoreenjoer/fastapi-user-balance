import pytest
from fastapi.testclient import TestClient
from main import app, users_db  


client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_and_teardown():
    global user_id_counter
    users_db.clear()
    import main
    main.user_id_counter = 1
    yield  
    users_db.clear()
    main.user_id_counter = 1



def test_create_user_success():
    """Тест успешного создания пользователя."""
    response = client.post(
        "/users",
        json={"name": "Alice", "email": "alice@example.com", "balance": 1000.0},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Alice"
    assert data["email"] == "alice@example.com"
    assert data["balance"] == 1000.0
    assert "id" in data


def test_create_user_duplicate_email():
    """Тест на ошибку при создании пользователя с существующим email."""
    client.post("/users", json={"name": "Bob", "email": "bob@example.com", "balance": 500})

    response = client.post("/users", json={"name": "Bobby", "email": "bob@example.com", "balance": 200})
    assert response.status_code == 400
    assert "User with this email already exists" in response.json()["detail"]


def test_get_users_list():
    """Тест получения списка пользователей."""
    client.post("/users", json={"name": "Charlie", "email": "charlie@example.com", "balance": 700})
    client.post("/users", json={"name": "David", "email": "david@example.com", "balance": 800})

    response = client.get("/users")
    assert response.status_code == 200
    users_list = response.json()
    assert len(users_list) == 2
    assert users_list[0]["name"] == "Charlie"
    assert users_list[1]["email"] == "david@example.com"


def test_transfer_success():
    """Тест успешного перевода средств."""
    user1_res = client.post("/users", json={"name": "Eve", "email": "eve@example.com", "balance": 100})
    user2_res = client.post("/users", json={"name": "Frank", "email": "frank@example.com", "balance": 50})
    user1_id = user1_res.json()["id"]
    user2_id = user2_res.json()["id"]

    response = client.post(
        "/transfer",
        json={"from_user_id": user1_id, "to_user_id": user2_id, "amount": 25.5},
    )
    assert response.status_code == 200
    assert "Transfer successful" in response.json()["message"]

    assert users_db[user1_id].balance == 74.5 
    assert users_db[user2_id].balance == 75.5  


def test_transfer_insufficient_funds():
    """Тест на ошибку при недостаточном количестве средств."""
    user1_res = client.post("/users", json={"name": "Grace", "email": "grace@example.com", "balance": 10})
    user2_res = client.post("/users", json={"name": "Heidi", "email": "heidi@example.com", "balance": 100})
    user1_id = user1_res.json()["id"]
    user2_id = user2_res.json()["id"]

    response = client.post(
        "/transfer",
        json={"from_user_id": user1_id, "to_user_id": user2_id, "amount": 20},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Insufficient funds."


def test_transfer_to_self():
    """Тест на ошибку при переводе средств самому себе."""
    user_res = client.post("/users", json={"name": "Ivan", "email": "ivan@example.com", "balance": 100})
    user_id = user_res.json()["id"]

    response = client.post(
        "/transfer",
        json={"from_user_id": user_id, "to_user_id": user_id, "amount": 50},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Cannot transfer money to yourself."


def test_transfer_sender_not_found():
    """Тест на ошибку, если отправитель не найден."""
    user_res = client.post("/users", json={"name": "Judy", "email": "judy@example.com", "balance": 100})
    user_id = user_res.json()["id"]

    response = client.post(
        "/transfer",
        json={"from_user_id": 999, "to_user_id": user_id, "amount": 50}, 
    )
    assert response.status_code == 404
    assert "Sender user with id 999 not found" in response.json()["detail"]


def test_transfer_receiver_not_found():
    """Тест на ошибку, если получатель не найден."""
    user_res = client.post("/users", json={"name": "Mallory", "email": "mallory@example.com", "balance": 100})
    user_id = user_res.json()["id"]

    response = client.post(
        "/transfer",
        json={"from_user_id": user_id, "to_user_id": 999, "amount": 50}, 
    )
    assert response.status_code == 404
    assert "Receiver user with id 999 not found" in response.json()["detail"]


def test_transfer_negative_amount():
    """Тест на ошибку при переводе отрицательной суммы."""
    user1_res = client.post("/users", json={"name": "Niaj", "email": "niaj@example.com", "balance": 100})
    user2_res = client.post("/users", json={"name": "Olivia", "email": "olivia@example.com", "balance": 100})
    user1_id = user1_res.json()["id"]
    user2_id = user2_res.json()["id"]

    response = client.post(
        "/transfer",
        json={"from_user_id": user1_id, "to_user_id": user2_id, "amount": -50},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Transfer amount must be positive."
