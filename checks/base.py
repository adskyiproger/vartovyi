from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass
class CheckResult:
    success: bool
    message: str = ""
    details: dict[str, Any] | None = None


class Check(ABC):
    check_type: str

    def __init__(self, name: str) -> None:
        self.name = name

    @classmethod
    @abstractmethod
    def from_config(cls, name: str, config: dict[str, Any]) -> "Check":
        pass

    @abstractmethod
    def run(self) -> CheckResult:
        pass