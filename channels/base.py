from abc import ABC, abstractmethod
from typing import Any


class Channel(ABC):
    channel_type: str

    def __init__(self, name: str) -> None:
        self.name = name

    @classmethod
    @abstractmethod
    def from_config(cls, name: str, config: dict[str, Any]) -> "Channel":
        pass

    @abstractmethod
    def send(self, message: str) -> None:
        pass
