from abc import ABC, abstractmethod
from typing import Union


class BaseStorage(ABC):
    @abstractmethod
    async def get_from_storage(self, key: str) -> str:
        """Прочитать данные из хранилища"""

    @abstractmethod
    async def put_to_storage(self, key: str, value: str, expire: int) -> None:
        """Сохранить данные в хранилище"""
