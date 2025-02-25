import requests
import re
from .balances import BalancesManager
from .currencies import CurrenciesManager
from .info import InfoManager
from .user import User

class TipccClient:
    def __init__(self, token) -> None:
        if not re.match(r"^[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+$", token):
            raise ValueError("Invalid auth token provided")

        self.token = token
        self.balances = BalancesManager(self)
        self.currencies = CurrenciesManager(self)
        self.info = InfoManager(self)
        self.user = User(self)
        self.session = requests.Session()
        self.session.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}",
        }

    @classmethod
    def get_token_from_dms(cls, discord_bot_token):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bot {discord_bot_token}",
        }
        try:
            dm_channel_response = requests.post(
                "https://discord.com/api/users/@me/channels",
                json={"recipient_id": "350270174462607360"},
                headers=headers,
                timeout=15,
            )
            dm_channel_response.raise_for_status()
            dm_channel_id = dm_channel_response.json().get("id")

            if not dm_channel_id:
                raise RuntimeError("Failed to retrieve DM channel ID.")

            messages_response = requests.get(
                f"https://discord.com/api/channels/{dm_channel_id}/messages",
                headers=headers,
                timeout=15,
            )
            messages_response.raise_for_status()
            messages = messages_response.json()

            key_message = next(
                (msg for msg in reversed(messages)
                 if msg.get("content", "").startswith("eyJ") and msg.get("author", {}).get("id") == "350270174462607360"),
                None
            )

            if not key_message:
                raise RuntimeError("No valid auth token found in messages.")

            return key_message["content"]
        except requests.exceptions.RequestException as exc:
            raise RuntimeError("Failed retrieving the auth token.") from exc
