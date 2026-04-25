import logging
import time

from channels import create_channel
from checks import create_check
from utils.common import load_config, setup_logging



import signal

def handle_exit(signum, frame):
    log.info("Stopping monitor...")
    exit(0)

signal.signal(signal.SIGINT, handle_exit)
signal.signal(signal.SIGTERM, handle_exit)

config = load_config("bot.yaml")
log = setup_logging(config)

def build_channels(config: dict):
    return {
        name: create_channel(name, item)
        for name, item in config["channels"].items()
    }


def build_services(config: dict):
    services = {}

    for service in config["services"]:
        name = service["name"]
        services[name] = {
            "name": name,
            "interval": int(service.get("interval", config.get("check_interval", 60))),
            "channels": service.get("channels", [config["default_channel"]]),
            "up_message": service.get("up_message", f"✅ {name} is UP"),
            "down_message": service.get("down_message", f"❌ {name} is DOWN"),
            "check": create_check(name, service["check"]),
            "last_check_at": 0,
            "last_status": None,
        }

    return services


def send_to_channels(channels: dict, channel_names: list[str], message: str) -> None:
    for channel_name in channel_names:
        channel = channels.get(channel_name)

        if channel is None:
            log.error("Channel '%s' not found", channel_name)
            continue

        channel.send(message)


def main():
    log_level = config.get("log_level", "info").upper()
    log.info(f"Log level set to {log_level}")

    log.info("Starting monitor...")

    channels = build_channels(config)
    services = build_services(config)

    send_to_channels(
        channels,
        [config["default_channel"]],
        "🚀 Monitor started.",
    )

    while True:
        now = time.monotonic()

        for service_name, service in services.items():
            if now - service["last_check_at"] < service["interval"]:
                continue
            
            service["last_check_at"] = now

            result = service["check"].run()
            log.debug("Checking %s... Last check: %s Interval: %s Result: %s",
                      service_name,
                      service["last_check_at"],
                      service["interval"],
                      result)
            previous_status = service["last_status"]
            current_status = result.success

            if previous_status is None:
                service["last_status"] = current_status
                log.info(
                    "Initial status for %s: %s",
                    service_name,
                    "UP" if current_status else "DOWN",
                )
                continue

            if previous_status != current_status:
                if current_status:
                    message = service["up_message"]
                    log.info("%s recovered: %s", service_name, result.message)
                else:
                    message = service["down_message"]
                    log.warning("%s failed: %s", service_name, result.message)

                send_to_channels(
                    channels,
                    service["channels"],
                    message,
                )

            service["last_status"] = current_status

        time.sleep(1)


if __name__ == "__main__":
    main()
