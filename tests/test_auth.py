import pytest
from httpx import AsyncClient

from app.schemas.user import UserTestData


@pytest.mark.asyncio
async def test_register_user(client: AsyncClient, user_data: UserTestData):
    response = await client.post(url="/auth/register", json=user_data.model_dump())
    assert response.status_code == 201

    data = response.json()

    assert data["email"] == user_data.email
    assert data["full_name"] == user_data.full_name

    assert "password" not in data
    assert "hashed_password" not in data


@pytest.mark.asyncio
async def test__conflict_register_user(
    client: AsyncClient, user_data: UserTestData, user
):
    response = await client.post(url="/auth/register", json=user_data.model_dump())
    assert response.status_code == 409


@pytest.mark.parametrize(
    "email,password,full_name",
    [
        ("validemail", "password", "Razmik"),
        ("valid@gmail.com", "12", "Razmik"),
        ("valid@gmail.com", "validpassword", ""),
    ],
)
@pytest.mark.asyncio
async def test__invalid_register_user(
    client: AsyncClient, user_data: UserTestData, email, password, full_name
):
    response = await client.post(
        url="/auth/register",
        json={
            "email": email,
            "password": password,
            "full_name": full_name,
        },
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_login_user(
    client: AsyncClient, user, user_data: UserTestData, test_redis
):
    response = await client.post(
        url="/auth/login", json={"email": user["email"], "password": user_data.password}
    )

    assert response.status_code == 200

    data = response.json()

    assert "refresh_token" not in data
    assert "access_token" in data
    assert "refresh_token" in response.cookies


@pytest.mark.parametrize(
    "email,password,expected_status",
    [
        ("razmapian73@gmail.com", "2004klara", 401),
        ("email@gmail.com", "klara2004", 401),
    ],
)
@pytest.mark.asyncio
async def test_invalid_data_login(
    client: AsyncClient,
    email,
    password,
    expected_status,
    user,
):
    response = await client.post(
        url="/auth/login", json={"password": password, "email": email}
    )

    assert response.status_code == expected_status


@pytest.mark.asyncio
async def test_get_profile_me(auth_client, login_user, user_data: UserTestData):
    response = await auth_client.get(url="/auth/me")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == user_data.email
    assert data["full_name"] == user_data.full_name


@pytest.mark.asyncio
async def test_profile_me_without_token(client: AsyncClient):
    response = await client.get(url="/auth/me")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_refresh_token(client: AsyncClient, login_user):
    response = await client.post("/auth/refresh")
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" not in data
    assert "refresh_token" in response.cookies


@pytest.mark.asyncio
async def test_refresh_token_rotation(client: AsyncClient, login_user):
    old_refresh_token = client.cookies.get("refresh_token")

    response = await client.post("/auth/refresh")
    assert response.status_code == 200
    new_token = response.cookies.get("refresh_token")

    assert new_token is not None
    assert old_refresh_token != new_token

    client.cookies.set(
        "refresh_token",
        old_refresh_token,
    )

    response = await client.post("/auth/refresh")

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_logout(
    client: AsyncClient,
    login_user,
):

    assert client.cookies.get("refresh_token") is not None

    response = await client.post("/auth/logout")

    assert response.status_code == 204

    assert client.cookies.get("refresh_token") is None

    response = await client.post("/auth/refresh")

    assert response.status_code == 401
