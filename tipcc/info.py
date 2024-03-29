import requests
import json

class InfoManager:
    def __init__(self, token) -> None:
        self.token = token

    def local_user(self):
        x = requests.get(
            f"https://api.tip.cc/api/v0/user",
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {self.token}",
            },
        )
        if x.status_code not in [200]:
            return False, (json.loads(x.content))["error"]

        return True, json.loads(x.content)


    def local_connections(self):
        x = requests.get(
            f"https://api.tip.cc/api/v0/user/connections",
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {self.token}",
            },
        )
        if x.status_code not in [200]:
            return False, (json.loads(x.content))["error"]

        return True, json.loads(x.content)


    def parse_tip_message(self, message):
        # reads a tip.cc tip message (string) and returns the data. Does NOT check to see if the message was sent by the tip.cc bot

        message = message.split(" ")[1:]
        userIdFrom = int(message[0].split("<@")[1].replace(">", ""))
        userIdTo = int(message[2].split("<@")[1].replace(">", ""))
        value = float(message[3])
        crypto = str(message[4])
        estUSDValue = float(message[6].split(")")[0].replace("$", ""))

        # you can retrieve the memo a user wrote in its tip using a similar method to the following:

        # write a function like the following:
        """
        async def get_last_message_by_author(message, authorid):

            channel = message.channel
            messages = []

            async for message in channel.history(limit=5):
                messages.append(message)

            if messages:
                for i in range(5):
                    last_message = messages[i]
                    if last_message.author.id == int(authorid):
                        return last_message
                    else:
                        return None
        """

        # then call the function after retrieving your tip data:
        """
        try:
            memo = last_message.content.split(" ")[4] //get the memo
        except: //if there was no memo found
            //do something
        """

        # erm im not responsible for anything that goes wrong with this way of getting the memo... use at own risk.

        return userIdFrom, userIdTo, value, crypto, estUSDValue
