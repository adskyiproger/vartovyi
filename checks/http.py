from typing import Any

import requests

from checks.base import Check, CheckResult


class HTTPCheck(Check):
    check_type = "http"

    def __init__(
        self,
        name: str,
        url: str,
        expected_status: int = 200,
        timeout: float = 5,
    ) -> None:
        super().__init__(name)
        self.url = url
        self.expected_status = expected_status
        self.timeout = timeout
        self.session = requests.Session()

    @classmethod
    def from_config(cls, name: str, config: dict[str, Any]) -> "HTTPCheck":
        return cls(
            name=name,
            url=config["url"],
            expected_status=int(config.get("expected_status", 200)),
            timeout=float(config.get("timeout", 5)),
        )

    def run(self) -> CheckResult:
        try:
            response = self.session.get(self.url, timeout=self.timeout)
            if response.status_code == self.expected_status:
                return CheckResult(
                    success=True,
                    message=f"HTTP OK: {self.url} [{response.status_code}]",
                    details={"status_code": response.status_code},
                )

            return CheckResult(
                success=False,
                message=(
                    f"HTTP DOWN: {self.url} "
                    f"expected={self.expected_status} actual={response.status_code}"
                ),
                details={"status_code": response.status_code},
            )

        except requests.RequestException as e:
            return CheckResult(
                success=False,
                message=f"HTTP DOWN: {self.url} - {e}",
            )