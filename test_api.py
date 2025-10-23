import pytest
from api import app, users


@pytest.fixture
def client():
    """Fixture to create a test client for the Flask app"""
    app.config["TESTING"] = True
    with app.test_client() as client:
        # Clear simulated DB before each test
        users.clear()
        yield client


def test_add_user_success(client):
    """Test adding a new user successfully"""
    response = client.post("/users", json={"id": 1, "name": "Alice"})
    assert response.status_code == 201
    data = response.get_json()
    assert data == {"id": 1, "name": "Alice"}


def test_add_user_invalid_data(client):
    """Test adding a user with missing fields"""
    response = client.post("/users", json={"name": "NoID"})
    assert response.status_code == 400
    assert response.get_json()["error"] == "Invalid data"


def test_add_user_already_exists(client):
    """Test adding a user that already exists"""
    client.post("/users", json={"id": 1, "name": "Alice"})
    response = client.post("/users", json={"id": 1, "name": "Alice"})
    assert response.status_code == 400
    assert response.get_json()["error"] == "User already exists"


def test_get_user_success(client):
    """Test retrieving an existing user"""
    client.post("/users", json={"id": 1, "name": "Alice"})
    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.get_json() == {"id": 1, "name": "Alice"}


def test_get_user_not_found(client):
    """Test retrieving a user that does not exist"""
    response = client.get("/users/99")
    assert response.status_code == 404
    assert response.get_json()["error"] == "User not found"
