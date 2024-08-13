import pytest
from faker import Faker

faker = Faker()


@pytest.mark.asyncio
def test_create_post(client, test_user):
    headers = {"Authorization": f"Bearer {test_user['access_token']}"}
    title = faker.sentence()
    content = faker.paragraph()
    data = {
        "title": title,
        "content": content,
        "is_published": False,
    }
    response = client.post(url="/posts", json=data, headers=headers)

    assert response.status_code == 201
    assert response.json()["title"] == title


@pytest.mark.asyncio
def test_retrieve_all_posts(client, test_user):
    headers = {"Authorization": f"Bearer {test_user['access_token']}"}
    response = client.get(url="/posts", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
def test_update_post(client, test_user, test_post):
    headers = {"Authorization": f"Bearer {test_user['access_token']}"}
    updated_title = faker.sentence()
    updated_content = faker.paragraph()
    response = client.put(
        "/posts/1",
        json={
            "title": updated_title,
            "content": updated_content,
            "is_published": False,
        },
        headers=headers,
    )
    assert response.status_code == 201
    assert response.json()["title"] == updated_title


@pytest.mark.asyncio
def test_partial_update_post(client, test_user, test_post):
    headers = {"Authorization": f"Bearer {test_user['access_token']}"}
    updated_title = faker.sentence()
    response = client.patch(
        "/posts/1",
        json={"title": updated_title},
        headers=headers,
    )
    assert response.status_code == 201
    assert response.json()["title"] == updated_title


@pytest.mark.asyncio
def test_retrieve_post(client, test_user, test_post):
    headers = {"Authorization": f"Bearer {test_user['access_token']}"}
    response = client.get("posts/1", headers=headers)
    assert response.status_code == 200
    assert response.json()["title"] == test_post["title"]


@pytest.mark.asyncio
def test_delete_post(client, test_user, test_post):
    headers = {"Authorization": f"Bearer {test_user['access_token']}"}
    response = client.delete("posts/1", headers=headers)
    assert response.status_code == 200
    response = client.get("posts/1", headers=headers)
    assert response.status_code == 404


@pytest.mark.asyncio
def test_unauthenticated_request(client):
    headers = {"Authorization": f"Bearer fake token"}
    response = client.get("/posts/", headers=headers)
    assert response.status_code == 401
    response = client.get("/posts/1", headers=headers)
    assert response.status_code == 401


@pytest.mark.asyncio
def test_invalid_input_post(client, test_user):
    headers = {"Authorization": f"Bearer {test_user['access_token']}"}

    response = client.post(
        "/posts",
        json={
            "title": "",
            "content": "",
            "is_published": "not a boolean",
        },
        headers=headers,
    )
    assert response.status_code == 422

    response = client.put(
        "/posts/1",
        json={
            "title": faker.sentence(),
            "content": faker.paragraph(),
            "is_published": "not a boolean",
        },
        headers=headers,
    )
    assert response.status_code == 422

    response = client.patch(
        "/posts/1",
        json={"title": 123},
        headers=headers,
    )
    assert response.status_code == 422
