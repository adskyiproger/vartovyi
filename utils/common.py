
import logging
import os
import re
from typing import Any
from ruamel.yaml import YAML


yaml = YAML(typ='safe', pure=True)


def expand_env_vars(value: Any) -> Any:
    """Recursively expand ${VAR} in YAML values."""
    pattern = re.compile(r"\$\{([A-Z0-9_]+)\}")

    if isinstance(value, str):
        def replacer(match: re.Match[str]) -> str:
            var_name = match.group(1)
            return os.getenv(var_name, "")
        return pattern.sub(replacer, value)

    if isinstance(value, list):
        return [expand_env_vars(item) for item in value]

    if isinstance(value, dict):
        return {k: expand_env_vars(v) for k, v in value.items()}

    return value


def load_config(path: str) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        raw = yaml.load(f) or {}
    return expand_env_vars(raw)


def setup_logging(config: dict[str, Any]) -> logging.Logger:
    log_level = config.get("logging", {}).get("level", "INFO").upper()
    logging.basicConfig(
        level=getattr(logging, log_level, logging.INFO),
        format="%(asctime)s [%(levelname)s] %(message)s",
    )
    return logging.getLogger()