import pytest
from faker import Faker

faker = Faker()


@pytest.mark.asyncio
def test_create_client(client):
    email = faker.email()
    password = faker.password()
    first_name = faker.first_name()
    last_name = faker.last_name()

    data = {
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "password": password,
    }
    response = client.post(url="/users/signup", json=data)

    assert response.status_code == 201
    assert (
        response.json()["detail"]
        == "your account has been created successfully, please check your email!"
    )

    response = client.post(
        url="/login",
        data={"username": email, "password": password},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    global access_token
    access_token = response.json()["access_token"]


@pytest.mark.asyncio
def test_retrieve_all_users(client, test_user):
    headers = {"Authorization": f"Bearer {test_user['access_token']}"}
    response = client.get(url="/users", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
def test_retrieve_my_user(client, test_user):
    headers = {"Authorization": f"Bearer {test_user['access_token']}"}
    response = client.get(url="/users/profile", headers=headers)
    assert response.status_code == 200
    assert response.json()["email"] == test_user["email"]


@pytest.mark.asyncio
def test_update_user(client, test_user):
    headers = {"Authorization": f"Bearer {test_user['access_token']}"}
    new_email = faker.email()
    response = client.put(
        "/users/1",
        json={
            "email": new_email,
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
        },
        headers=headers,
    )
    assert response.status_code == 201
    assert response.json()["email"] == new_email


@pytest.mark.asyncio
def test_partial_update_user(client, test_user):
    headers = {"Authorization": f"Bearer {test_user['access_token']}"}
    new_first_name = faker.first_name()
    response = client.patch(
        "/users/1",
        json={"first_name": new_first_name},
        headers=headers,
    )
    assert response.status_code == 201
    assert response.json()["first_name"] == new_first_name


@pytest.mark.asyncio
def test_retrieve_user(client, test_user):
    headers = {"Authorization": f"Bearer {test_user['access_token']}"}
    response = client.get("/users/1", headers=headers)
    assert response.status_code == 200
    assert response.json()["email"] == test_user["email"]


@pytest.mark.asyncio
def test_delete_user(client, test_user):
    headers = {"Authorization": f"Bearer {test_user['access_token']}"}
    response = client.delete("users/1", headers=headers)
    assert response.status_code == 200
    response = client.get("user/1", headers=headers)
    assert response.status_code == 404


@pytest.mark.asyncio
def test_unauthenticated_request(client):
    headers = {"Authorization": f"Bearer fake token"}
    response = client.get("/users/", headers=headers)
    assert response.status_code == 401
    response = client.get("/users/1", headers=headers)
    assert response.status_code == 401
    response = client.get("/users/profile", headers=headers)
    assert response.status_code == 401


@pytest.mark.asyncio
def test_invalid_input(client, test_user):
    headers = {"Authorization": f"Bearer {test_user['access_token']}"}

    response = client.post(
        "/users/signup",
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
        "/users/1",
        json={"email": faker.email()},
        headers=headers,
    )
    assert response.status_code == 422

    response = client.patch(
        "/users/1",
        json={
            "email": "invalidemailformat",
            "first_name": faker.first_name(),
        },
        headers=headers,
    )
    assert response.status_code == 422


@pytest.mark.asyncio
def test_invalid_route(client, test_user):
    headers = {"Authorization": f"Bearer {test_user['access_token']}"}
    response = client.get("/ascaad", headers=headers)
    assert response.status_code == 404


@pytest.mark.asyncio
def test_refresh_instead_of_access(client, test_user):
    headers = {"Authorization": f"Bearer {test_user['refresh_token']}"}
    response = client.get("/users", headers=headers)
    assert response.json()["detail"] == "Cannot authenticate with a refresh token"
