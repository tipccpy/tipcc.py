import requests
import json


class InfoManager:
    def __init__(self, client) -> None:
        self.client = client

    def _get_api_data(self, url: str):
        """
        Helper method to send a GET request to the API and return the response data or error.
        """
        try:
            response = self.client.session.get(url)
            response.raise_for_status()  # Will raise an exception for 4xx/5xx responses
            return True, response.json()  # Parse JSON response and return
        except requests.exceptions.RequestException as e:
            return False, str(e)  # Return the error message if something goes wrong

    def local_user(self):
        success, data = self._get_api_data("https://api.tip.cc/api/v0/user")
        if not success:
            return False, f"Error fetching user data: {data}"
        return True, data

    def local_connections(self):
        success, data = self._get_api_data("https://api.tip.cc/api/v0/user/connections")
        if not success:
            return False, f"Error fetching user connections: {data}"
        return True, data

    def parse_tip_message(self, message: str):
        """
        Parses a Tip.cc message and extracts relevant data (user IDs, tip value, crypto, and USD value).
        Returns a tuple: (userIdFrom, userIdTo, value, crypto, estUSDValue)
        """
        try:
            # Split the message and extract relevant parts
            message_parts = message.split(" ")[1:]
            userIdFrom = int(message_parts[0].split("<@")[1].replace(">", ""))
            userIdTo = int(message_parts[2].split("<@")[1].replace(">", ""))
            value = float(message_parts[3])
            crypto = str(message_parts[4])
            estUSDValue = float(message_parts[6].split(")")[0].replace("$", ""))

            return userIdFrom, userIdTo, value, crypto, estUSDValue
        except (IndexError, ValueError) as e:
            return False, f"Error parsing tip message: {e}"

    async def get_memo_from_message(self, message, author_id):
        """
        Attempts to fetch the memo written by the user in a previous message.
        Returns the memo string or None if not found.
        """
        try:
            # Assuming `message` is a Discord message object, fetch previous messages from the same author
            channel = message.channel
            async for past_message in channel.history(limit=5):
                if past_message.author.id == int(author_id):
                    return past_message.content.split(" ")[4]  # Assuming memo is the 5th word
            return None  # Memo not found
        except Exception as e:
            return None  # Return None if there's an issue retrieving the memo
