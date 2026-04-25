import platform
import subprocess
from typing import Any

from checks.base import Check, CheckResult


class ICMPCheck(Check):
    check_type = "icmp"

    def __init__(
        self,
        name: str,
        host: str,
        timeout: float = 3,
    ) -> None:
        super().__init__(name)
        self.host = host
        self.timeout = timeout

    @classmethod
    def from_config(cls, name: str, config: dict[str, Any]) -> "ICMPCheck":
        return cls(
            name=name,
            host=config["host"],
            timeout=float(config.get("timeout", 3)),
        )

    def run(self) -> CheckResult:
        system = platform.system().lower()

        if system == "windows":
            cmd = [
                "ping",
                "-n",
                "1",
                "-w",
                str(int(self.timeout * 1000)),
                self.host,
            ]
        else:
            cmd = [
                "ping",
                "-c",
                "1",
                "-W",
                str(int(self.timeout)),
                self.host,
            ]

        try:
            completed = subprocess.run(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=self.timeout + 1,
                check=False,
            )

            if completed.returncode == 0:
                return CheckResult(
                    success=True,
                    message=f"ICMP OK: {self.host}",
                )

            return CheckResult(
                success=False,
                message=f"ICMP DOWN: {self.host}",
            )

        except subprocess.TimeoutExpired:
            return CheckResult(
                success=False,
                message=f"ICMP DOWN: {self.host} - timeout",
            )