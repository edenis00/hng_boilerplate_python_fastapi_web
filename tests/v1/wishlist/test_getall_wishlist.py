import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from api.v1.models.user import User
from main import app
from api.v1.services.wishlist import wishlist_service
from api.v1.services.user import user_service


@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def auth_headers():
    return {"Authorization": "Bearer test-token"}



def mock_current_user():
    return User(
        id="test-user-id",
        email="test@example.com",
        password="@2Testpassword",
        is_active=True
    )


def test_get_all_wishlist_unauthorized(client):
    app.dependency_overrides[user_service.get_current_user] = lambda: None

    response = client.get("/api/v1/wishlist/", headers={})

    app.dependency_overrides[user_service.get_current_user] = mock_current_user

    assert response.status_code == 401
    assert response.json()["detail"] == "Unauthorized"


@patch('api.v1.services.wishlist.wishlist_service.fetch_all')
def test_get_wishlist_success(mock_fetch_all, client, auth_headers):
    mock_fetch_all.return_value = [
        {"id": "wishlist-id-1", "user_id": "test-user-id", "product_id": "test-product-id-1"},
        {"id": "wishlist-id-2", "user_id": "test-user-id", "product_id": "test-product-id-2"},
    ]

    response = client.get("/api/v1/wishlist/", headers=auth_headers)

    assert response.status_code == 200
    assert response.json()["message"] == "Wishlist retrieved successfully"
    assert len(response.json()["data"]) == 2
    assert response.json()["data"][0]["product_id"] == "test-product-id-1"
    assert response.json()["data"][1]["product_id"] == "test-product-id-2"