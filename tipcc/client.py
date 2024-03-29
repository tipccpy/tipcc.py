import requests
import re
from .balances import BalancesManager
from .currencies import CurrenciesManager
from .info import InfoManager
from .user import User

class TipccClient:
    def __init__(self, token) -> None:
        if not re.match(r"(^[A-Za-z0-9-_]*\.[A-Za-z0-9-_]*\.[A-Za-z0-9-_]*$)", token):
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
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bot {discord_bot_token}",
            }
            dm_channel = requests.post(
                "https://discord.com/api/users/@me/channels",
                data='{"recipient_id":"350270174462607360"}',
                headers=headers,
                timeout=15,
            )
            dm_channel_id = dm_channel.json()["id"]
            messages_response = requests.get(
                f"https://discord.com/api/channels/{dm_channel_id}/messages",
                headers=headers,
                timeout=15,
            )
            messages = messages_response.json()
            key = [
                msg
                for msg in messages
                if msg["content"].startswith("eyJ")
                and msg["author"]["id"] == "350270174462607360"
            ][-1]
            return key["content"]
        except requests.exceptions.RequestException as exc:
            raise RuntimeError("Failed retriving the auth token.") from exc
