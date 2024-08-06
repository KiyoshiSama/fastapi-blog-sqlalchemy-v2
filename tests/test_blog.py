# test_blog.py

import pytest
from httpx import AsyncClient
from app.schemas.post_schema import PostCreate

@pytest.mark.asyncio
async def test_create_post(client: AsyncClient, db_session: AsyncSession):
    # Create a test user
    user_response = await client.post(
        "/api/user/create-user",
        json={"email": "testuser@example.com", "password": "password", "first_name": "Test", "last_name": "User"},
    )
    assert user_response.status_code == 200
    user_id = user_response.json()["id"]

    # Authenticate the user to get a token
    auth_response = await client.post(
        "/api/auth/login",
        data={"username": "testuser@example.com", "password": "password"},
    )
    assert auth_response.status_code == 200
    token = auth_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    # Create a new blog post
    post_data = {"title": "Test Post", "content": "This is a test post.", "is_published": True}
    response = await client.post(
        "/api/blog/create-new", json=post_data, headers=headers
    )
    assert response.status_code == 201
    assert response.json()["title"] == "Test Post"

@pytest.mark.asyncio
async def test_get_all_posts(client: AsyncClient, db_session: AsyncSession):
    # Authenticate the user to get a token
    auth_response = await client.post(
        "/api/auth/login",
        data={"username": "testuser@example.com", "password": "password"},
    )
    assert auth_response.status_code == 200
    token = auth_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    # Get all blog posts
    response = await client.get("/api/blog/all", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_update_post(client: AsyncClient, db_session: AsyncSession):
    # Authenticate the user to get a token
    auth_response = await client.post(
        "/api/auth/login",
        data={"username": "testuser@example.com", "password": "password"},
    )
    assert auth_response.status_code == 200
    token = auth_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    # Create a new blog post
    post_data = {"title": "Test Post", "content": "This is a test post.", "is_published": True}
    response = await client.post(
        "/api/blog/create-new", json=post_data, headers=headers
    )
    post_id = response.json()["id"]

    # Update the blog post
    update_data = {"title": "Updated Test Post", "content": "This is an updated test post.", "is_published": False}
    response = await client.put(
        f"/api/blog/update/{post_id}", json=update_data, headers=headers
    )
    assert response.status_code == 202
    assert response.json()["title"] == "Updated Test Post"

@pytest.mark.asyncio
async def test_delete_post(client: AsyncClient, db_session: AsyncSession):
    # Authenticate the user to get a token
    auth_response = await client.post(
        "/api/auth/login",
        data={"username": "testuser@example.com", "password": "password"},
    )
    assert auth_response.status_code == 200
    token = auth_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    # Create a new blog post
    post_data = {"title": "Test Post", "content": "This is a test post.", "is_published": True}
    response = await client.post(
        "/api/blog/create-new", json=post_data, headers=headers
    )
    post_id = response.json()["id"]

    # Delete the blog post
    response = await client.delete(f"/api/blog/delete/{post_id}", headers=headers)
    assert response.status_code == 204

@pytest.mark.asyncio
async def test_show_post(client: AsyncClient, db_session: AsyncSession):
    # Authenticate the user to get a token
    auth_response = await client.post(
        "/api/auth/login",
        data={"username": "testuser@example.com", "password": "password"},
    )
    assert auth_response.status_code == 200
    token = auth_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    # Create a new blog post
    post_data = {"title": "Test Post", "content": "This is a test post.", "is_published": True}
    response = await client.post(
        "/api/blog/create-new", json=post_data, headers=headers
    )
    post_id = response.json()["id"]

    # Show the blog post
    response = await client.get(f"/api/blog/show/{post_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Test Post"
