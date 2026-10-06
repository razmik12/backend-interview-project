import pytest


@pytest.mark.asyncio
async def test_create_task(client, login_user_two, created_project):
    response = await client.post(
        f"/projects/{created_project['id']}/tasks",
        headers={"Authorization": f"Bearer {login_user_two['access_token']}"},
        json={"title": "New Task", "description": "description"},
    )

    assert response.status_code == 201

    task = response.json()
    assert task["title"] == "New Task"
    assert task["project_id"] == created_project["id"]
    assert task["status"] == "todo"


@pytest.mark.asyncio
async def test_create_task_forbidden(client, login_user, created_project):
    response = await client.post(
        f"/projects/{created_project['id']}/tasks",
        headers={"Authorization": f"Bearer {login_user['access_token']}"},
        json={"title": "New Task", "description": "description"},
    )

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_create_task_project_not_found(client, login_user_two):
    response = await client.post(
        "/projects/00000000-0000-0000-0000-000000000000/tasks",
        headers={"Authorization": f"Bearer {login_user_two['access_token']}"},
        json={"title": "New Task", "description": "description"},
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_tasks(client, login_user_two, created_project, created_task):
    response = await client.get(
        f"/projects/{created_project['id']}/tasks",
        headers={"Authorization": f"Bearer {login_user_two['access_token']}"},
    )

    assert response.status_code == 200

    tasks = response.json()
    assert len(tasks) == 1
    assert tasks[0]["id"] == created_task["id"]


@pytest.mark.asyncio
async def test_get_tasks_forbidden(client, login_user, created_project):
    response = await client.get(
        f"/projects/{created_project['id']}/tasks",
        headers={"Authorization": f"Bearer {login_user['access_token']}"},
    )

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_update_task(
    client,
    login_user_two,
    created_project,
    created_task,
):
    response = await client.patch(
        f"/projects/{created_project['id']}/tasks/{created_task['id']}",
        headers={"Authorization": f"Bearer {login_user_two['access_token']}"},
        json={"title": "Updated Task"},
    )

    assert response.status_code == 202

    task = response.json()
    assert task["id"] == created_task["id"]
    assert task["title"] == "Updated Task"


@pytest.mark.asyncio
async def test_update_task_forbidden(
    client,
    login_user,
    created_project,
    created_task,
):
    response = await client.patch(
        f"/projects/{created_project['id']}/tasks/{created_task['id']}",
        headers={"Authorization": f"Bearer {login_user['access_token']}"},
        json={"title": "Updated Task"},
    )

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_update_task_not_found(
    client,
    login_user_two,
    created_project,
):
    response = await client.patch(
        f"/projects/{created_project['id']}/tasks/00000000-0000-0000-0000-000000000000",
        headers={"Authorization": f"Bearer {login_user_two['access_token']}"},
        json={"title": "Updated Task"},
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_task_status(
    client,
    login_user_two,
    created_project,
    created_task,
):
    response = await client.patch(
        f"/projects/{created_project['id']}/tasks/{created_task['id']}/status",
        headers={"Authorization": f"Bearer {login_user_two['access_token']}"},
        json={"status": "done"},
    )

    assert response.status_code == 202

    task = response.json()
    assert task["status"] == "done"


@pytest.mark.asyncio
async def test_delete_task(
    client,
    login_user_two,
    created_task,
):
    response = await client.delete(
        f"/projects/tasks/{created_task['id']}",
        headers={"Authorization": f"Bearer {login_user_two['access_token']}"},
    )

    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_task_forbidden(
    client,
    login_user,
    created_task,
):
    response = await client.delete(
        f"/projects/tasks/{created_task['id']}",
        headers={"Authorization": f"Bearer {login_user['access_token']}"},
    )

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_delete_task_not_found(client, login_user_two):
    response = await client.delete(
        "/tasks/00000000-0000-0000-0000-000000000000",
        headers={"Authorization": f"Bearer {login_user_two['access_token']}"},
    )

    assert response.status_code == 404
