import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from passlib.context import CryptContext

from core.database import Base, get_db
from core.adapters import get_storage
from adapters.storage.base import StorageAdapter
from main import app

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False
)
TestingSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)

async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session

class MockStorageAdapter(StorageAdapter):
    async def upload_file(self, file_data: bytes, file_name: str, content_type: str) -> str:
        return f"http://mock-minio/{file_name}"

    async def download_file(self, file_name: str) -> bytes:
        return b"mock-file-content"

    async def delete_file(self, file_name: str) -> None:
        pass

    async def check_connection(self) -> bool:
        return True

def override_get_storage():
    return MockStorageAdapter()

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_storage] = override_get_storage

@pytest_asyncio.fixture(scope="session")
def anyio_backend():
    return "asyncio"

@pytest_asyncio.fixture(scope="function", autouse=True)
async def init_db():
    # Создаем таблицы базы данных в памяти
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield
    
    # Удаляем после выполнения теста
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture(scope="function")
async def async_client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://testserver"
    ) as ac:
        yield ac

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@pytest_asyncio.fixture(scope="function")
async def authorized_client(async_client: AsyncClient):
    # Создаем пользователя через API
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword"
    }
    await async_client.post("/auth/register", json=user_data)
    
    # Логинимся
    form_data = {
        "username": "test@example.com", 
        "password": "testpassword"
    }
    response = await async_client.post("/auth/login", data=form_data)
    token = response.json()["access_token"]
    
    # Устанавливаем заголовок
    async_client.headers.update({"Authorization": f"Bearer {token}"})
    return async_client
