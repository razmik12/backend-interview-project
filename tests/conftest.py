from typing import Any

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from app.config import settings
from app.core.redis_app import get_redis
from app.database import Base, get_db
from app.main import app
from app.schemas.user import UserTestData
from redis.asyncio import Redis





@pytest_asyncio.fixture(scope="function")
async def test_redis():
    redis = Redis.from_url(
        url = settings.test_redis_url,
        decode_responses = True
    )
    async def get_test_redis():
        yield redis
        
    app.dependency_overrides[get_redis] = get_test_redis
    
    yield redis
    
    await redis.flushdb()
    await redis.aclose()
    


@pytest_asyncio.fixture()
async def test_engine():
    engine = create_async_engine(
        url=settings.test_database_url
    )

    yield engine

    await engine.dispose()



@pytest_asyncio.fixture
async def test_get_db(test_engine):
    
    connection = await test_engine.connect()
    transaction = await connection.begin()

    session = AsyncSession(
        bind=connection,
        expire_on_commit=False,
        join_transaction_mode="create_savepoint",
    )

    async def override_get_db():
        yield session

    app.dependency_overrides[get_db] = override_get_db

    try:
        yield session
    finally:
        app.dependency_overrides.clear()
        await session.close()
        await transaction.rollback()
        await connection.close()


@pytest_asyncio.fixture(autouse=True)
async def database_connect(test_engine):
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)




@pytest_asyncio.fixture
async def client(test_get_db,test_redis):
    async with AsyncClient(
        base_url="http://test",
        transport=ASGITransport(app=app),
    ) as client:
        yield client
        
   
@pytest_asyncio.fixture
async def user_data() -> UserTestData:
    return UserTestData(
        email="razmapian73@gmail.com",
        password="klara2004",
        full_name="Razmik",
    )


@pytest_asyncio.fixture
async def user(
    client: AsyncClient,
    user_data: UserTestData,
):
    response = await client.post(
        url="/auth/register",
        json=user_data.model_dump(),
    )
    return response.json()


@pytest_asyncio.fixture
async def login_user(
    client: AsyncClient,
    user: dict[str, Any],
    user_data: UserTestData,
):
    response = await client.post(
        url="/auth/login",
        json={
            "email": user_data.email,
            "password": user_data.password,
        },
    )
    return response.json()


@pytest_asyncio.fixture
async def auth_headers(login_user: dict[str, Any]):
    return {
        "Authorization": f"Bearer {login_user['access_token']}"
    }


@pytest_asyncio.fixture
async def auth_client(
    auth_headers: dict[str, str],
    client: AsyncClient,
):
    client.headers.update(auth_headers)
    return client



@pytest_asyncio.fixture
async def user_data_two():
    return UserTestData(
        email="new_razmapian73@gmail.com",
        full_name="Ramzec12",
        password="levseeva01"
    )
    
@pytest_asyncio.fixture
async def user_two(user_data_two:UserTestData,client: AsyncClient):
    response = await client.post(url="/auth/register",
                                 json=user_data_two.model_dump())
    return response.json()


    
@pytest_asyncio.fixture
async def login_user_two(
    client: AsyncClient,
    user_two: dict[str, Any],
    user_data_two: UserTestData,
):
    response = await client.post(
        url="/auth/login",
        json={
            "email": user_data_two.email,
            "password": user_data_two.password,
        },
    )
    return response.json()  



@pytest_asyncio.fixture
async def projects_data():
    return {
        "name":"projects_name",
        "description":"projects_description"
    }



@pytest_asyncio.fixture
async def created_project(
    client:AsyncClient,
    login_user_two:dict[str,Any],
    projects_data:dict[str,Any]
):
    token = login_user_two["access_token"]
    response = await client.post("/projects",
                                 headers={"Authorization": f"Bearer {token}"},
                                 json=projects_data)
    
    return response.json()








@pytest_asyncio.fixture
async def created_task(client: AsyncClient, login_user_two, created_project):
    token = login_user_two["access_token"]
    project_id = created_project["id"]
    response = await client.post(
        url=f"/projects/{project_id}/tasks",
        headers={"Authorization": f"Bearer {token}"},
        json={"title": "Test Task", "description": "task description"},
    )
    return response.json()


@pytest_asyncio.fixture
async def created_comment(client: AsyncClient, login_user_two, created_project, created_task):
    token = login_user_two["access_token"]
    task_id = created_task["id"]
    response = await client.post(
        url=f"/tasks/{task_id}/comments",
        headers={"Authorization": f"Bearer {token}"},
        json={"text": "Test comment"},
    )
    return response.json()