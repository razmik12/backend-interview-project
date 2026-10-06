import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_comment(
    client: AsyncClient,
    login_user_two,
    user_two,
    created_task,
):
    task_id = created_task["id"]
    response = await client.post(
        f"/tasks/{task_id}/comments",
        headers={"Authorization": f"Bearer {login_user_two['access_token']}"},
        json={"text": "Test comment"},
    )

    assert response.status_code == 201

    comment = response.json()

    assert comment["task_id"] == created_task["id"]
    assert comment["text"] == "Test comment"
    assert comment["author_id"] == user_two["id"]


@pytest.mark.asyncio
async def test_create_comment_forbidden(
    client: AsyncClient,
    login_user,
    created_task,
):
    task_id = created_task["id"]
    response = await client.post(
        f"/tasks/{task_id}/comments",
        headers={"Authorization": f"Bearer {login_user['access_token']}"},
        json={"text": "Test comment"},
    )

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_create_comment_not_found(client, login_user_two):
    response = await client.post(
        "/tasks/00000000-0000-0000-0000-000000000000/comments",
        headers={"Authorization": f"Bearer {login_user_two['access_token']}"},
        json={"text": "Test comment"},
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_comments(
    client: AsyncClient,
    login_user_two,
    created_task,
    created_comment,
):
    response = await client.get(
        f"/tasks/{created_task['id']}/comments",
        headers={"Authorization": f"Bearer {login_user_two['access_token']}"},
    )

    assert response.status_code == 200

    comments = response.json()

    assert len(comments) == 1
    assert comments[0]["id"] == created_comment["id"]
    assert comments[0]["text"] == "Test comment"


@pytest.mark.asyncio
async def test_get_comments_forbidden(
    client: AsyncClient,
    login_user,
    created_task,
):
    response = await client.get(
        f"/tasks/{created_task['id']}/comments",
        headers={"Authorization": f"Bearer {login_user['access_token']}"},
    )

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_get_comments_not_found(client, login_user_two):
    response = await client.get(
        "/tasks/00000000-0000-0000-0000-000000000000/comments",
        headers={"Authorization": f"Bearer {login_user_two['access_token']}"},
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_comment(
    client: AsyncClient,
    login_user_two,
    created_comment,
):
    response = await client.delete(
        f"/comments/{created_comment['id']}",
        headers={"Authorization": f"Bearer {login_user_two['access_token']}"},
    )

    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_comment_not_found(client: AsyncClient, login_user_two):
    response = await client.delete(
        "/comments/00000000-0000-0000-0000-000000000000",
        headers={"Authorization": f"Bearer {login_user_two['access_token']}"},
    )

    assert response.status_code == 404
