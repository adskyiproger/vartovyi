import importlib
import inspect
import pkgutil

import checks
from checks.base import Check


def load_check_types() -> dict[str, type[Check]]:
    check_types: dict[str, type[Check]] = {}

    for module_info in pkgutil.iter_modules(checks.__path__):
        module_name = module_info.name

        if module_name in {"base", "loader"}:
            continue

        module = importlib.import_module(f"checks.{module_name}")

        for _, obj in inspect.getmembers(module, inspect.isclass):
            if not issubclass(obj, Check):
                continue

            if obj is Check:
                continue

            check_type = getattr(obj, "check_type", None)

            if not check_type:
                continue

            if check_type in check_types:
                raise ValueError(f"Duplicate check type: {check_type}")

            check_types[check_type] = obj

    return check_types


CHECK_REGISTRY = load_check_types()


def create_check(name: str, config: dict) -> Check:
    check_type = config["type"]
    check_class = CHECK_REGISTRY.get(check_type)

    if check_class is None:
        raise ValueError(f"Unsupported check type: {check_type}")

    return check_class.from_config(name=name, config=config)