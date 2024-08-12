import random
import pytest


def test_create_client(client):
    global number
    number = random.randint(100, 999)
    data = {
        "email": f"testuser{number}@example.com",
        "first_name": "New",
        "last_name": "User",
        "password": "testpassword",
    }
    response = client.post(url="/user/signup", json=data)

    assert response.status_code == 201
    assert (
        response.json()["detail"]
        == "your account has been created successfully, please check your email!"
    )
    response = client.post(
        url="/login",
        data={
            "username": f"testuser{number}@example.com",
            "password": "testpassword",
        },
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    global access_token
    access_token = response.json()["access_token"]


@pytest.mark.asyncio
def test_retrieve_all_users(client, test_user):
    headers = {"Authorization": f"Bearer {test_user['access_token']}"}
    response = client.get(url="/user/all", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
def test_retrieve_my_user(client, test_user):
    headers = {"Authorization": f"Bearer {test_user['access_token']}"}
    response = client.get(url="/user/me", headers=headers)
    assert response.status_code == 200
    assert response.json()["email"] == test_user["email"]


@pytest.mark.asyncio
def test_update_user(client, test_user):
    headers = {"Authorization": f"Bearer {test_user['access_token']}"}
    response = client.put(
        "/user/1",
        json={
            "email": "updateduser@example.com",
            "first_name": "Updated",
            "last_name": "User",
        },
        headers=headers,
    )
    print(response.json())
    assert response.status_code == 201
    assert response.json()["email"] == "updateduser@example.com"


@pytest.mark.asyncio
def test_partial_update_user(client, test_user):
    headers = {"Authorization": f"Bearer {test_user['access_token']}"}
    response = client.patch(
        "/user/1",
        json={
            "email": test_user["email"],
            "first_name": "PartiallyUpdated",
            "last_name": "updated_last_name",
        },
        headers=headers,
    )
    assert response.status_code == 201
    assert response.json()["first_name"] == "PartiallyUpdated"


@pytest.mark.asyncio
def test_retrieve_user(client, test_user):
    headers = {"Authorization": f"Bearer {test_user['access_token']}"}
    response = client.get("/user/1", headers=headers)
    assert response.status_code == 200
    assert response.json()["email"] == "testuser@example.com"

@pytest.mark.asyncio
def test_delete_user(client, test_user):
    headers = {"Authorization": f"Bearer {test_user['access_token']}"}
    response = client.delete("user/delete/1", headers=headers)
    assert response.status_code == 200
    response = client.get("user/1", headers=headers)
    assert response.status_code == 404


@pytest.mark.asyncio
def test_unauthenticated_request(client):
    headers = {"Authorization": f"Bearer fake token"}
    response = client.get("/user/all", headers=headers)
    assert response.status_code == 401
    response = client.get("/user/1", headers=headers)
    assert response.status_code == 401
    response = client.get("/user/me", headers=headers)
    assert response.status_code == 401
    response = client.delete("/user/delete/1", headers=headers)
    assert response.status_code == 401
    response = client.put("/user/1", headers=headers)
    assert response.status_code == 401
    response = client.patch("/user/1", headers=headers)
    assert response.status_code == 401



@pytest.mark.asyncio
def test_invalid_input(client, test_user):
    headers = {"Authorization": f"Bearer {test_user['access_token']}"}

    response = client.post(
        "/user/signup",
        json={
            "email": "invalidemail",
            "password": "short",
        },
    )
    assert response.status_code == 422

    response = client.post(
        url="/login",
        data={
            "username": "wronguser@example.com",
            "password": "wrongpassword",
        },
    )
    assert response.status_code == 401

    response = client.put(
        "/user/1",
        json={
            "email": "updateduser@example.com",
        },
        headers=headers,
    )
    assert response.status_code == 422

    response = client.patch(
        "/user/1",
        json={
            "email": "invalidemailformat",
            "first_name": "NewName",
        },
        headers=headers,
    )
    assert response.status_code == 422


@pytest.mark.asyncio
def test_invalid_route(client, test_user):
    headers = {"Authorization": f"Bearer {test_user['access_token']}"}
    response = client.get("/ascaad", headers=headers)
    assert response.status_code == 404
