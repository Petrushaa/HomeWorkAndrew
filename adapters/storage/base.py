from abc import ABC, abstractmethod

class StorageAdapter(ABC):
    @abstractmethod
    async def upload_file(self, content: bytes, key: str, content_type: str) -> str:
        """Загружает файл и возвращает URL"""
        pass
        
    @abstractmethod
    async def check_connection(self) -> bool:
        """Проверяет доступность сервиса"""
        pass
