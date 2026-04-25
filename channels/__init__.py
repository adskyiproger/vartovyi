import importlib
import inspect
import pkgutil

import channels
from channels.base import Channel


def load_channel_types() -> dict[str, type[Channel]]:
    channel_types: dict[str, type[Channel]] = {}

    for module_info in pkgutil.iter_modules(channels.__path__):
        module_name = module_info.name

        if module_name in {"base", "loader"}:
            continue

        module = importlib.import_module(f"channels.{module_name}")

        for _, obj in inspect.getmembers(module, inspect.isclass):
            if not issubclass(obj, Channel):
                continue

            if obj is Channel:
                continue

            channel_type = getattr(obj, "channel_type", None)

            if not channel_type:
                continue

            if channel_type in channel_types:
                raise ValueError(f"Duplicate check type: {channel_type}")

            channel_types[channel_type] = obj

    return channel_types


CHANNEL_REGISTRY = load_channel_types()


def create_channel(name: str, config: dict) -> Channel:
    channel_type = config["type"]
    channel_class = CHANNEL_REGISTRY.get(channel_type)

    if channel_class is None:
        raise ValueError(f"Unsupported channel type: {channel_type}")
    print(config)
    return channel_class.from_config(name=name, config=config['config'])