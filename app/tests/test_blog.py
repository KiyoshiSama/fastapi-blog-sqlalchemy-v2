import random
import pytest


@pytest.mark.asyncio
def test_create_post(client, test_user):
    global number
    headers = {"Authorization": f"Bearer {test_user['access_token']}"}
    number = random.randint(10, 200)
    data = {
        "title": f"post title test {number}",
        "content": "post content test",
        "is_published": False,
    }
    response = client.post(url="/blog/create-new", json=data, headers=headers)

    assert response.status_code == 201
    assert response.json()["title"] == f"post title test {number}"


@pytest.mark.asyncio
def test_retrieve_all_posts(client, test_user):
    headers = {"Authorization": f"Bearer {test_user['access_token']}"}
    response = client.get(url="/blog/all", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
def test_update_post(client, test_user, test_post):
    headers = {"Authorization": f"Bearer {test_user['access_token']}"}
    response = client.put(
        "/blog/update/1",
        json={
            "title": "post title test updated (put)",
            "content": "post content test updated (put)",
            "is_published": False,
        },
        headers=headers,
    )
    print(response.json())
    assert response.status_code == 201
    assert response.json()["title"] == "post title test updated (put)"


@pytest.mark.asyncio
def test_partial_update_post(client, test_user, test_post):
    headers = {"Authorization": f"Bearer {test_user['access_token']}"}
    response = client.patch(
        "/blog/update/1",
        json={
            "title": "post title test updated (patch)",
            "content": "post content test updated (patch)",
            "is_published": False,
        },
        headers=headers,
    )
    assert response.status_code == 201
    assert response.json()["title"] == "post title test updated (patch)"


@pytest.mark.asyncio
def test_retrieve_post(client, test_user, test_post):
    headers = {"Authorization": f"Bearer {test_user['access_token']}"}
    response = client.get("blog/show/1", headers=headers)
    assert response.status_code == 200
    assert response.json()["title"] == "post title test original"

@pytest.mark.asyncio
def test_delete_post(client, test_user, test_post):
    headers = {"Authorization": f"Bearer {test_user['access_token']}"}
    response = client.delete("blog/delete/1", headers=headers)
    assert response.status_code == 200
    response = client.get("blog/show/1", headers=headers)
    assert response.status_code == 404

@pytest.mark.asyncio
def test_unauthenticated_request(client):
    headers = {"Authorization": f"Bearer fake token"}
    response = client.get("/blog/all", headers=headers)
    assert response.status_code == 401
    response = client.post("/blog/create-new", headers=headers)
    assert response.status_code == 401
    response = client.put("/blog/update/1", headers=headers)
    assert response.status_code == 401
    response = client.patch("/blog/update/1", headers=headers)
    assert response.status_code == 401
    response = client.get("/blog/show/1", headers=headers)
    assert response.status_code == 401
    response = client.delete("/blog/delete/1", headers=headers)
    assert response.status_code == 401


@pytest.mark.asyncio
def test_invalid_input_post(client, test_user):
    headers = {"Authorization": f"Bearer {test_user['access_token']}"}

    response = client.post(
        "/blog/create-new",
        json={
            "title": "",  
            "content": "",  
            "is_published": "not a boolean",  
        },
        headers=headers,
    )
    assert response.status_code == 422

    response = client.put(
        "/blog/update/1",
        json={
            "title": "valid title",
            "content": "valid content",
            "is_published": "not a boolean", 
        },
        headers=headers,
    )
    assert response.status_code == 422

    response = client.patch(
        "/blog/update/1",
        json={
            "title": 123, 
        },
        headers=headers,
    )
    assert response.status_code == 422