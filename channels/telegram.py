from typing import Any

import requests

from channels.base import Channel


class TelegramChannel(Channel):
    channel_type = "telegram"

    def __init__(
        self,
        name: str,
        bot_token: str,
        chat_ids: list[str],
        timeout: float = 5,
    ) -> None:
        super().__init__(name)
        self.bot_token = bot_token
        self.chat_ids = chat_ids
        self.timeout = timeout
        self.session = requests.Session()
        self.url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    @classmethod
    def from_config(cls, name: str, config: dict[str, Any]) -> "TelegramChannel":
        return cls(
            name=name,
            bot_token=config["bot_token"],
            chat_ids=config["chat_ids"],
            timeout=config.get("timeout", 5),
        )

    def send(self, message: str) -> None:
        for chat_id in self.chat_ids:
            self.session.post(
                self.url,
                data={"chat_id": chat_id, "text": message},
                timeout=self.timeout,
            )
