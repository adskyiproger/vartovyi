import socket
from typing import Any

from checks.base import Check, CheckResult


class TCPCheck(Check):
    check_type = "tcp"

    def __init__(
        self,
        name: str,
        host: str,
        port: int,
        timeout: float = 3,
    ) -> None:
        super().__init__(name)
        self.host = host
        self.port = port
        self.timeout = timeout

    @classmethod
    def from_config(cls, name: str, config: dict[str, Any]) -> "TCPCheck":
        return cls(
            name=name,
            host=config["host"],
            port=int(config["port"]),
            timeout=float(config.get("timeout", 3)),
        )

    def run(self) -> CheckResult:
        try:
            with socket.create_connection(
                (self.host, self.port),
                timeout=self.timeout,
            ):
                return CheckResult(
                    success=True,
                    message=f"TCP OK: {self.host}:{self.port}",
                )
        except OSError as e:
            return CheckResult(
                success=False,
                message=f"TCP DOWN: {self.host}:{self.port} - {e}",
            )
